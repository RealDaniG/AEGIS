import argparse
import json
import os
from typing import List

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)

try:
    from peft import LoraConfig, get_peft_model
    PEFT_AVAILABLE = True
except Exception:
    PEFT_AVAILABLE = False


def read_jsonl_texts(path: str) -> List[str]:
    texts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                t = obj.get("text")
                if isinstance(t, str) and t.strip():
                    texts.append(t.strip())
            except Exception:
                # skip malformed lines
                continue
    return texts


def main():
    parser = argparse.ArgumentParser(description="Causal LM training on JSONL {text} data")
    parser.add_argument("--model", required=True, help="Base model name or path (e.g., datificate/gpt2-small-spanish)")
    parser.add_argument("--data", required=True, help="Path to JSONL file with {text} field")
    parser.add_argument("--out", required=True, help="Output directory for trained/adapters model")
    parser.add_argument("--epochs", type=int, default=1, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=2, help="Per-device train batch size")
    parser.add_argument("--lr", type=float, default=5e-5, help="Learning rate")
    parser.add_argument("--seq-len", type=int, default=1024, help="Max sequence length")
    parser.add_argument("--limit-samples", type=int, default=0, help="Limit number of training samples (0 = no limit)")
    parser.add_argument("--use-lora", action="store_true", help="Use LoRA adapters (if peft is available)")
    parser.add_argument("--lora-r", type=int, default=8)
    parser.add_argument("--lora-alpha", type=int, default=16)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    parser.add_argument(
        "--target-modules",
        type=str,
        default="c_attn,c_proj,c_fc",
        help="Comma-separated target modules for LoRA",
    )
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    print(f"[INFO] Loading tokenizer: {args.model}")
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    # Ensure pad token exists for batching
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"[INFO] Loading base model: {args.model}")
    model = GPT2LMHeadModel.from_pretrained(args.model)
    model.config.pad_token_id = tokenizer.pad_token_id
    # For trainer speed/compat
    model.config.use_cache = False

    if args.use_lora:
        if not PEFT_AVAILABLE:
            print("[WARN] peft not available, continuing without LoRA")
        else:
            target_modules = [m.strip() for m in args.target_modules.split(",") if m.strip()]
            lora_config = LoraConfig(
                r=args.lora_r,
                lora_alpha=args.lora_alpha,
                lora_dropout=args.lora_dropout,
                bias="none",
                task_type="CAUSAL_LM",
                target_modules=target_modules,
            )
            model = get_peft_model(model, lora_config)
            print("[INFO] LoRA activated with target modules:", target_modules)

    print(f"[INFO] Reading dataset: {args.data}")
    texts = read_jsonl_texts(args.data)
    if not texts:
        raise RuntimeError("No valid texts found in dataset")
    if args.limit_samples and args.limit_samples > 0:
        texts = texts[: args.limit_samples]
        print(f"[INFO] Limiting dataset to {len(texts)} samples")
    dataset = Dataset.from_dict({"text": texts})

    def tokenize_fn(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=args.seq_len,
            padding="max_length",
        )

    print("[INFO] Tokenizing dataset...")
    tokenized = dataset.map(tokenize_fn, batched=True, remove_columns=["text"])

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    print("[INFO] Preparing training arguments...")
    training_args = TrainingArguments(
        output_dir=args.out,
        overwrite_output_dir=True,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        learning_rate=args.lr,
        logging_steps=50,
        save_steps=200,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    print("[INFO] Starting training...")
    trainer.train()
    print("[OK] Training finished. Saving model to:", args.out)
    trainer.save_model(args.out)
    tokenizer.save_pretrained(args.out)
    print("[DONE] Saved.")


if __name__ == "__main__":
    main()