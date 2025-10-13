import sys
import importlib
import asyncio
import json
import os
from typing import Optional, Tuple, Dict, Any

# Configure Unicode logging
try:
    from logging_config import logger as configured_logger
    logger = configured_logger
except Exception:
    # Fallback to default loguru if config fails
    try:
        from loguru import logger
    except Exception:
        # Fallback mínimo si loguru no está disponible
        class _L:
            def info(self, *a, **k): print(*a)
            def warning(self, *a, **k): print(*a)
            def error(self, *a, **k): print(*a)
            def success(self, *a, **k): print(*a)
        logger = _L()

import click
from dotenv import load_dotenv


def safe_import(module_name: str) -> Tuple[Optional[object], Optional[Exception]]:
    """Importa un módulo de forma segura, devolviendo (módulo, error)."""
    try:
        mod = importlib.import_module(module_name)
        return mod, None
    except Exception as e:
        return None, e


async def module_call(mod: object, func_name: str, *args, **kwargs):
    """Llama a una función de un módulo si existe y es callable."""
    if not mod:
        return False
    fn = getattr(mod, func_name, None)
    if callable(fn):
        try:
            result = fn(*args, **kwargs)
            # If it's a coroutine, await it
            if asyncio.iscoroutine(result):
                return await result
            return result
        except Exception as e:
            module_name = getattr(mod, '__name__', str(mod))
            logger.error(f"Error ejecutando {module_name}.{func_name}: {e}")
            return False
    return False


DEFAULT_CONFIG: Dict[str, Any] = {
    "app": {
        "log_level": "INFO",
        "enable": {
            "tor": True,
            "p2p": True,
            "crypto": True,
            "consensus": True,
            "monitoring": True,
            "resource_manager": True,
            "performance_optimizer": True,
            "logging_system": True,
            "config_manager": True,
            "api_server": True,
            "metrics_collector": True,
            "alert_system": True,
            "web_dashboard": True,
            "backup_system": True,
            "test_framework": True,
        },
    },
    "tor": {
        "enabled": True,
        "socks_port": 9050,
        "control_port": 9051,
        "onion_routing": True,
    },
    "p2p": {
        "discovery": "zeroconf",
        "heartbeat_interval_sec": 30,
    },
    "crypto": {
        "rotate_interval_hours": 24,
        "hash": "blake3",
        "symmetric": "chacha20-poly1305",
    },
    "consensus": {
        "algorithm": "PoC+PBFT",
    },
    "monitoring": {
        "dashboard_port": 8080,
        "enable_socketio": True,
    },
    "security": {
        "rate_limit_per_minute": 120,
        "validate_peer_input": True,
    },
    "config_manager": {
        "auto_reload": True,
        "reload_interval": 30,
    },
    "api_server": {
        "port": 8000,
        "host": "0.0.0.0",
        "enable_cors": True,
    },
    "web_dashboard": {
        "port": 8080,
        "host": "0.0.0.0",
    },
    "backup_system": {
        "enabled": True,
        "interval_hours": 24,
        "retention_days": 30,
    },
    "test_framework": {
        "enabled": True,
        "parallel_tests": True,
    },
}


def load_config(config_path: Optional[str]) -> Dict[str, Any]:
    """Carga configuración desde JSON y aplica overrides desde .env."""
    load_dotenv()
    cfg: Dict[str, Any] = DEFAULT_CONFIG.copy()
    path = config_path or os.environ.get("AEGIS_CONFIG", "app_config.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            # merge superficial (solo primer nivel y 'app.enable')
            for k, v in user_cfg.items():
                if k == "app" and isinstance(v, dict):
                    cfg["app"].update(v)
                    if "enable" in v and isinstance(v["enable"], dict):
                        cfg["app"]["enable"].update(v["enable"])
                else:
                    cfg[k] = v
        except Exception as e:
            logger.warning(f"No se pudo cargar {path}, usando valores por defecto: {e}")
    else:
        logger.info(f"Config por defecto: no se encontró {path}")

    # Overrides por entorno
    log_level = os.environ.get("AEGIS_LOG_LEVEL")
    if log_level:
        cfg["app"]["log_level"] = log_level

    dash_port = os.environ.get("AEGIS_DASHBOARD_PORT")
    if dash_port and dash_port.isdigit():
        cfg["monitoring"]["dashboard_port"] = int(dash_port)

    return cfg


def health_summary() -> dict:
    summary = {
        "python": sys.version,
        "modules": {},
    }

    for m in [
        "aiohttp",
        "websockets",
        "asyncio",
        "cryptography",
        "pydantic",
        "torch",
    ]:
        mod, err = safe_import(m)
        summary["modules"][m] = {
            "available": mod is not None,
            "error": str(err) if err else None,
        }

    # Comprobación rápida de CUDA (si torch está disponible)
    try:
        import torch  # type: ignore
        summary["cuda"] = {
            "available": bool(torch.cuda.is_available()),
            "device_count": int(torch.cuda.device_count()) if torch.cuda.is_available() else 0,
        }
    except Exception:
        summary["cuda"] = {"available": False, "device_count": 0}

    return summary


async def start_node(dry_run: bool = False, config_path: Optional[str] = None):
    cfg = load_config(config_path)
    logger.info("Iniciando nodo AEGIS distribuido...")
    logger.info(f"Config aplicada: enable={cfg['app']['enable']}")

    tor_mod, tor_err = safe_import("tor_integration")
    p2p_mod, p2p_err = safe_import("p2p_network")
    crypto_mod, crypto_err = safe_import("crypto_framework")
    consensus_mod, cons_err = safe_import("consensus_algorithm")
    monitor_mod, mon_err = safe_import("monitoring_dashboard")
    resource_mod, res_err = safe_import("resource_manager")
    perf_mod, perf_err = safe_import("performance_optimizer")
    logging_mod, logging_err = safe_import("logging_system")
    config_mod, config_err = safe_import("config_manager")
    api_mod, api_err = safe_import("api_server")
    metrics_mod, metrics_err = safe_import("metrics_collector")
    alert_mod, alert_err = safe_import("alert_system")
    dashboard_mod, dashboard_err = safe_import("web_dashboard")
    backup_mod, backup_err = safe_import("backup_system")
    test_mod, test_err = safe_import("test_framework")

    if tor_err:
        logger.warning(f"TOR no disponible: {tor_err}")
    if p2p_err:
        logger.warning(f"P2P no disponible: {p2p_err}")
    if crypto_err:
        logger.warning(f"Crypto no disponible: {crypto_err}")
    if cons_err:
        logger.warning(f"Consenso no disponible: {cons_err}")
    if mon_err:
        logger.warning(f"Monitoreo no disponible: {mon_err}")
    if res_err:
        logger.warning(f"Gestión de recursos no disponible: {res_err}")
    if perf_err:
        logger.warning(f"Optimizador de rendimiento no disponible: {perf_err}")
    if logging_err:
        logger.warning(f"Sistema de logging no disponible: {logging_err}")
    if config_err:
        logger.warning(f"Gestor de configuración no disponible: {config_err}")
    if api_err:
        logger.warning(f"Servidor API no disponible: {api_err}")
    if metrics_err:
        logger.warning(f"Colector de métricas no disponible: {metrics_err}")
    if alert_err:
        logger.warning(f"Sistema de alertas no disponible: {alert_err}")
    if dashboard_err:
        logger.warning(f"Dashboard web no disponible: {dashboard_err}")
    if backup_err:
        logger.warning(f"Sistema de backup no disponible: {backup_err}")
    if test_err:
        logger.warning(f"Framework de tests no disponible: {test_err}")

    if dry_run:
        logger.info("Dry-run activado: verificando módulos y saliendo.")
        return

    # Inicializaciones seguras (solo si existen)
    # Inicializar Gestor de Configuración
    if cfg["app"]["enable"].get("config_manager") and config_mod:
        try:
            logger.info("🚀 Iniciando gestor de configuración...")
            await module_call(config_mod, "start_config_system", cfg.get("config_manager", {}))
            logger.info("✅ Gestor de configuración iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando gestor de configuración: {e}")

    # Inicializar Sistema de Logging
    if cfg["app"]["enable"].get("logging_system") and logging_mod:
        try:
            logger.info("🚀 Iniciando sistema de logging...")
            await module_call(logging_mod, "start_logging_system", cfg.get("logging_system", {}))
            logger.info("✅ Sistema de logging iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando sistema de logging: {e}")

    # Inicializar TOR
    if cfg["app"]["enable"].get("tor") and tor_mod:
        try:
            logger.info("🚀 Iniciando gateway TOR...")
            await module_call(tor_mod, "start_gateway", cfg.get("tor", {}))
            logger.info("✅ Gateway TOR iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando TOR: {e}")

    # Inicializar Gestión de Recursos
    if cfg["app"]["enable"].get("resource_manager") and resource_mod:
        try:
            logger.info("🚀 Iniciando gestión de recursos...")
            await module_call(resource_mod, "init_pool", cfg.get("p2p", {}))
            logger.info("✅ Gestión de recursos iniciada")
        except Exception as e:
            logger.error(f"❌ Error iniciando gestión de recursos: {e}")

    # Inicializar Crypto
    if cfg["app"]["enable"].get("crypto") and crypto_mod:
        try:
            logger.info("🚀 Iniciando framework criptográfico...")
            await module_call(crypto_mod, "initialize_crypto", cfg.get("crypto", {}))
            logger.info("✅ Framework criptográfico iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando crypto: {e}")

    # Inicializar P2P
    if cfg["app"]["enable"].get("p2p") and p2p_mod:
        try:
            logger.info("🚀 Iniciando red P2P...")
            await module_call(p2p_mod, "start_network", cfg.get("p2p", {}))
            logger.info("✅ Red P2P iniciada")
        except Exception as e:
            logger.error(f"❌ Error iniciando P2P: {e}")

    # Inicializar Consenso
    if cfg["app"]["enable"].get("consensus") and consensus_mod:
        try:
            logger.info("🚀 Iniciando algoritmo de consenso...")
            await module_call(consensus_mod, "start_consensus_loop", cfg.get("consensus", {}))
            logger.info("✅ Algoritmo de consenso iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando consenso: {e}")

    # Inicializar Optimizador de Rendimiento
    if cfg["app"]["enable"].get("performance_optimizer") and perf_mod:
        try:
            logger.info("🚀 Iniciando optimizador de rendimiento...")
            await module_call(perf_mod, "start_optimizer", cfg.get("performance_optimizer", {}))
            logger.info("✅ Optimizador de rendimiento iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando optimizador de rendimiento: {e}")

    # Inicializar Monitoreo
    if cfg["app"]["enable"].get("monitoring") and monitor_mod:
        try:
            logger.info("🚀 Iniciando dashboard de monitoreo...")
            await module_call(monitor_mod, "start_dashboard", cfg.get("monitoring", {}))
            logger.info("✅ Dashboard de monitoreo iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando monitoreo: {e}")

    # Inicializar Servidor API
    if cfg["app"]["enable"].get("api_server") and api_mod:
        try:
            logger.info("🚀 Iniciando servidor API...")
            await module_call(api_mod, "start_api_server", cfg.get("api_server", {}))
            logger.info("✅ Servidor API iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando servidor API: {e}")

    # Inicializar Colector de Métricas
    if cfg["app"]["enable"].get("metrics_collector") and metrics_mod:
        try:
            logger.info("🚀 Iniciando colector de métricas...")
            await module_call(metrics_mod, "start_metrics_collector", cfg.get("metrics", {}))
            logger.info("✅ Colector de métricas iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando colector de métricas: {e}")

    # Inicializar Sistema de Alertas
    if cfg["app"]["enable"].get("alert_system") and alert_mod:
        try:
            logger.info("🚀 Iniciando sistema de alertas...")
            await module_call(alert_mod, "start_alert_system", cfg.get("alerts", {}))
            logger.info("✅ Sistema de alertas iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando sistema de alertas: {e}")

    # Inicializar Dashboard Web
    if cfg["app"]["enable"].get("web_dashboard") and dashboard_mod:
        try:
            logger.info("🚀 Iniciando dashboard web...")
            await module_call(dashboard_mod, "start_web_dashboard", cfg.get("web_dashboard", {}))
            logger.info("✅ Dashboard web iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando dashboard web: {e}")

    # Inicializar Sistema de Backup
    if cfg["app"]["enable"].get("backup_system") and backup_mod:
        try:
            logger.info("🚀 Iniciando sistema de backup...")
            await module_call(backup_mod, "start_backup_system", cfg.get("backup_system", {}))
            logger.info("✅ Sistema de backup iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando sistema de backup: {e}")

    # Inicializar Framework de Tests
    if cfg["app"]["enable"].get("test_framework") and test_mod:
        try:
            logger.info("🚀 Iniciando framework de tests...")
            await module_call(test_mod, "start_test_framework", cfg.get("test_framework", {}))
            logger.info("✅ Framework de tests iniciado")
        except Exception as e:
            logger.error(f"❌ Error iniciando framework de tests: {e}")

    logger.info("🎯 Nodo AEGIS completamente iniciado")
    logger.info("Presiona Ctrl+C para detener el nodo")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Deteniendo nodo AEGIS...")

        logger.info("✅ Nodo AEGIS detenido correctamente")


@click.group()
def cli():
    """CLI AEGIS - IA Distribuida y Colaborativa."""
    pass


@cli.command()
@click.option("--dry-run", is_flag=True, help="No ejecutar procesos, solo validar módulos.")
@click.option("--config", type=click.Path(exists=False), help="Ruta del archivo de configuración JSON.")
def start_node_cmd(dry_run: bool, config: Optional[str]):
    """Inicia el nodo distribuido (TOR, P2P, Crypto, Consenso, Monitoreo)."""
    try:
        asyncio.run(start_node(dry_run=dry_run, config_path=config))
    except Exception as e:
        logger.error(f"Fallo al iniciar el nodo: {e}")
        raise RuntimeError(f"Failed to start node: {e}")


@cli.command()
@click.option("--config", type=click.Path(exists=False), help="Ruta del archivo de configuración JSON.")
def health_check(config: Optional[str]):
    """Muestra un resumen de salud del entorno y módulos clave."""
    summary = health_summary()
    logger.info("Resumen de salud:")
    for k, v in summary.items():
        logger.info(f"- {k}: {v}")


@cli.command()
def list_modules():
    """Lista el estado de importación de módulos principales."""
    mods = [
        "tor_integration",
        "p2p_network",
        "crypto_framework",
        "consensus_algorithm",
        "monitoring_dashboard",
        "resource_manager",
        "performance_optimizer",
        "logging_system",
        "config_manager",
        "api_server",
        "metrics_collector",
        "alert_system",
        "web_dashboard",
        "backup_system",
        "test_framework",
    ]
    for m in mods:
        mod, err = safe_import(m)
        if mod:
            logger.success(f"{m}: disponible")
        else:
            logger.warning(f"{m}: no disponible ({err})")


if __name__ == "__main__":
    cli()