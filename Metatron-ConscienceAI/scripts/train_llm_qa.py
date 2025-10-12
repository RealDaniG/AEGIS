import os
import json
import argparse
from typing import Dict, Any
import torch

from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

# PEFT (LoRA) opcional
_HAS_PEFT = True
try:
    from peft import LoraConfig, get_peft_model, TaskType
except Exception:
    _HAS_PEFT = False


def build_prompt(example: Dict[str, Any]) -> str:
    instr = example.get("instruction") or example.get("question") or ""
    inp = example.get("input") or ""
    resp = example.get("response") or example.get("answer") or ""
    if inp:
        instr = f"{instr}\n{inp}" if instr else inp
    # Plantilla simple estilo diálogo
    prompt = f"Usuario: {instr}\nAsistente: {resp}"
    return prompt


def main():
    parser = argparse.ArgumentParser(description="Fine-tuning SFT para QA en español (física y matemáticas)")
    parser.add_argument("--model", type=str, required=True, help="Modelo base (ruta local o ID de HF)")
    parser.add_argument("--train-file", type=str, required=True, help="Ruta a JSONL de entrenamiento")
    parser.add_argument("--eval-file", type=str, default=None, help="Ruta a JSONL de validación (opcional)")
    parser.add_argument("--out-dir", type=str, required=True, help="Directorio de salida del modelo")
    parser.add_argument("--epochs", type=int, default=1, help="Épocas de entrenamiento")
    parser.add_argument("--batch-size", type=int, default=1, help="Batch size por dispositivo")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--max-seq-len", type=int, default=512, help="Longitud máxima de secuencia")
    parser.add_argument("--lora", action="store_true", help="Usar LoRA si está disponible")
    # Soporte GPU / precisión mixta
    parser.add_argument("--fp16", action="store_true", help="Activar entrenamiento en FP16 (requiere GPU)")
    parser.add_argument("--bf16", action="store_true", help="Activar entrenamiento en BF16 (requiere GPU)")
    parser.add_argument("--tf32", action="store_true", help="Permitir TF32 en CUDA (si está disponible)")
    parser.add_argument("--pin-memory", dest="pin_memory", type=str, default="auto", choices=["auto", "true", "false"], help="Pinned memory para DataLoader (auto: true si hay GPU)")

    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    print(f"[INFO] Cargando tokenizer y modelo base: {args.model}")
    # Algunas arquitecturas (p.ej. Qwen) requieren trust_remote_code
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(args.model, trust_remote_code=True)

    # Asegurar pad_token_id para el collator si el tokenizer no lo define
    if getattr(tokenizer, "pad_token_id", None) is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
        print(f"[INFO] tokenizer.pad_token_id no definido. Usando eos_token_id={tokenizer.eos_token_id} como pad_token_id.")

    # Configurar LoRA si procede
    if args.lora:
        if not _HAS_PEFT:
            print("[WARN] PEFT/LoRA no disponible. Continúo sin LoRA.")
        else:
            print("[INFO] Activando LoRA (r=8, alpha=16, dropout=0.05)")
            lconf = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                r=8,
                lora_alpha=16,
                lora_dropout=0.05,
                target_modules=["c_attn", "q_proj", "v_proj", "k_proj"],
            )
            model = get_peft_model(model, lconf)

    # Cargar datasets desde JSONL
    print(f"[INFO] Cargando datos: train={args.train_file}")
    data_files = {"train": args.train_file}
    if args.eval_file:
        data_files["validation"] = args.eval_file
    ds = load_dataset("json", data_files=data_files)

    def preprocess_single(example):
        prompt = build_prompt(example)
        enc = tokenizer(
            prompt,
            max_length=args.max_seq_len,
            truncation=True,
            padding="max_length",
            return_tensors=None,
        )
        # Usar input_ids como labels para LM
        enc["labels"] = enc["input_ids"].copy()
        return enc

    # Mapear
    ds = ds.map(preprocess_single, batched=False, remove_columns=ds["train"].column_names)

    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Configurar opciones de precisión y pinned memory
    has_cuda = torch.cuda.is_available()
    if args.tf32:
        if not has_cuda:
            print("[WARN] --tf32 requiere GPU. Deshabilitado automáticamente.")
            args.tf32 = False
        else:
            # Verificar capacidad de la GPU (Ampere: compute capability >= 8.x)
            try:
                major, minor = torch.cuda.get_device_capability(0)
                if major < 8:
                    print(f"[WARN] --tf32 requiere Ampere o superior (cap {major}.{minor}). Deshabilitado.")
                    args.tf32 = False
                else:
                    torch.backends.cuda.matmul.allow_tf32 = True
                    print("[INFO] TF32 habilitado en CUDA.")
            except Exception as e:
                print(f"[WARN] No se pudo verificar/habilitar TF32: {e}. Deshabilitado.")
                args.tf32 = False

    if args.fp16 and not has_cuda:
        print("[WARN] --fp16 requiere GPU. Deshabilitado automáticamente.")
        args.fp16 = False
    if args.bf16 and not has_cuda:
        print("[WARN] --bf16 requiere GPU. Deshabilitado automáticamente.")
        args.bf16 = False

    use_pin_memory = True if args.pin_memory == "true" else False if args.pin_memory == "false" else has_cuda
    if use_pin_memory and not has_cuda:
        print("[WARN] pin_memory=true sin GPU. Se ignorará en DataLoader.")

    training_args = TrainingArguments(
        output_dir=args.out_dir,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        fp16=args.fp16,
        bf16=args.bf16,
        tf32=args.tf32,
        dataloader_pin_memory=use_pin_memory,
        logging_steps=10,
        save_steps=100,
        save_total_limit=2,
        report_to=[],
    )

    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        data_collator=collator,
        train_dataset=ds["train"],
        eval_dataset=ds.get("validation"),
    )

    print("[INFO] Comenzando entrenamiento...")
    trainer.train()
    print("[INFO] Entrenamiento finalizado. Guardando modelo...")
    trainer.save_model(args.out_dir)
    tokenizer.save_pretrained(args.out_dir)
    print(f"[OK] Modelo guardado en: {args.out_dir}")


if __name__ == "__main__":
    main()