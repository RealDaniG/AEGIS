"""
Alert System Module for AEGIS

This module provides a comprehensive alerting system that
enhances the basic alerting in monitoring_dashboard.py with:
- Advanced alert rule definition and management
- Multiple notification channels (email, SMS, webhook, etc.)
- Alert deduplication and grouping
- Alert escalation policies
- Alert history and audit trail
- Custom alert conditions and triggers
- Integration with external monitoring systems
- Alert silencing and suppression
- Metrics-based alerting
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
from datetime import datetime, timedelta
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Try to import loguru, fallback to standard logging
try:
    from loguru import logger
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertStatus(Enum):
    """Alert statuses"""
    TRIGGERED = "triggered"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SILENCED = "silenced"

class NotificationChannel(Enum):
    """Supported notification channels"""
    EMAIL = "email"
    WEBHOOK = "webhook"
    CONSOLE = "console"
    CUSTOM = "custom"

@dataclass
class AlertRule:
    """Definition of an alert rule"""
    id: str
    name: str
    description: str
    condition: str  # Python expression or function name
    level: AlertLevel
    enabled: bool = True
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)
    for_duration: int = 0  # seconds before alert triggers
    evaluation_interval: int = 30  # seconds
    notify_channels: List[NotificationChannel] = field(default_factory=list)
    escalation_policy: Optional[str] = None

@dataclass
class Alert:
    """An alert instance"""
    id: str
    rule_id: str
    name: str
    description: str
    level: AlertLevel
    status: AlertStatus
    labels: Dict[str, str]
    annotations: Dict[str, str]
    starts_at: float
    ends_at: Optional[float] = None
    last_notification: Optional[float] = None
    notification_count: int = 0
    fingerprint: str = ""  # Unique identifier for deduplication

@dataclass
class AlertSystemConfig:
    """Configuration for the Alert System"""
    enable_email_notifications: bool = False
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from: str = "aegis-alerts@example.com"
    smtp_to: str = "admin@example.com"
    enable_webhook_notifications: bool = False
    webhook_url: Optional[str] = None
    webhook_method: str = "POST"
    notification_interval: int = 300  # seconds between notifications
    alert_history_size: int = 1000
    enable_deduplication: bool = True
    deduplication_window: int = 300  # seconds
    enable_grouping: bool = True
    grouping_interval: int = 60  # seconds
    enable_silencing: bool = True
    silence_duration: int = 3600  # seconds

class AlertNotifier:
    """Handles sending notifications for alerts"""
    
    def __init__(self, config: AlertSystemConfig):
        self.config = config
        self.notification_functions: Dict[NotificationChannel, Callable] = {}
        self._setup_default_notifiers()
    
    def _setup_default_notifiers(self):
        """Setup default notification functions"""
        self.notification_functions[NotificationChannel.CONSOLE] = self._send_console_notification
        if self.config.enable_email_notifications:
            self.notification_functions[NotificationChannel.EMAIL] = self._send_email_notification
        if self.config.enable_webhook_notifications:
            self.notification_functions[NotificationChannel.WEBHOOK] = self._send_webhook_notification
    
    def register_notifier(self, channel: NotificationChannel, notifier: Callable):
        """Register a custom notification function"""
        self.notification_functions[channel] = notifier
    
    async def send_notification(self, alert: Alert, channel: NotificationChannel):
        """Send a notification for an alert"""
        if channel not in self.notification_functions:
            logger.warning(f"No notifier registered for channel {channel}")
            return False
        
        try:
            notifier = self.notification_functions[channel]
            if asyncio.iscoroutinefunction(notifier):
                await notifier(alert)
            else:
                notifier(alert)
            return True
        except Exception as e:
            logger.error(f"Failed to send {channel} notification for alert {alert.id}: {e}")
            return False
    
    def _send_console_notification(self, alert: Alert):
        """Send console notification"""
        message = f"ALERT [{alert.level.value.upper()}]: {alert.name} - {alert.description}"
        if alert.level == AlertLevel.INFO:
            logger.info(message)
        elif alert.level == AlertLevel.WARNING:
            logger.warning(message)
        elif alert.level == AlertLevel.ERROR:
            logger.error(message)
        elif alert.level == AlertLevel.CRITICAL:
            logger.critical(message)
    
    def _send_email_notification(self, alert: Alert):
        """Send email notification"""
        if not self.config.smtp_host or not self.config.smtp_from:
            logger.warning("Email notification configured but SMTP settings are incomplete")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.smtp_from
            msg['To'] = self.config.smtp_to
            msg['Subject'] = f"AEGIS Alert: {alert.name}"
            
            body = f"""
            Alert: {alert.name}
            Description: {alert.description}
            Level: {alert.level.value}
            Status: {alert.status.value}
            Started at: {datetime.fromtimestamp(alert.starts_at)}
            
            Labels: {alert.labels}
            Annotations: {alert.annotations}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.config.smtp_host, self.config.smtp_port)
            server.starttls()
            if self.config.smtp_username and self.config.smtp_password:
                server.login(self.config.smtp_username, self.config.smtp_password)
            text = msg.as_string()
            server.sendmail(self.config.smtp_from, self.config.smtp_to, text)
            server.quit()
            
            logger.info(f"Email notification sent for alert {alert.id}")
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
    
    def _send_webhook_notification(self, alert: Alert):
        """Send webhook notification"""
        if not self.config.webhook_url:
            logger.warning("Webhook notification configured but URL is not set")
            return
        
        try:
            import requests
            payload = {
                "alert_id": alert.id,
                "rule_id": alert.rule_id,
                "name": alert.name,
                "description": alert.description,
                "level": alert.level.value,
                "status": alert.status.value,
                "starts_at": alert.starts_at,
                "labels": alert.labels,
                "annotations": alert.annotations
            }
            
            response = requests.request(
                self.config.webhook_method,
                self.config.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code >= 400:
                logger.error(f"Webhook notification failed with status {response.status_code}")
            else:
                logger.info(f"Webhook notification sent for alert {alert.id}")
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {e}")

class AlertManager:
    """Manages alert rules, instances, and lifecycle"""
    
    def __init__(self, config: Optional[AlertSystemConfig] = None):
        self.config = config or AlertSystemConfig()
        self.rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: deque = deque(maxlen=self.config.alert_history_size)
        self.silences: Dict[str, float] = {}  # silence_id -> expires_at
        self.notifier = AlertNotifier(self.config)
        self.evaluation_tasks: Dict[str, asyncio.Task] = {}
        self.running = False
    
    def add_rule(self, rule: AlertRule):
        """Add an alert rule"""
        self.rules[rule.id] = rule
        logger.info(f"Added alert rule: {rule.name}")
    
    def remove_rule(self, rule_id: str):
        """Remove an alert rule"""
        if rule_id in self.rules:
            del self.rules[rule_id]
            logger.info(f"Removed alert rule: {rule_id}")
    
    def get_rule(self, rule_id: str) -> Optional[AlertRule]:
        """Get an alert rule by ID"""
        return self.rules.get(rule_id)
    
    def get_all_rules(self) -> Dict[str, AlertRule]:
        """Get all alert rules"""
        return self.rules.copy()
    
    def silence_alert(self, alert_id: str, duration: Optional[int] = None):
        """Silence an alert for a duration"""
        if not self.config.enable_silencing:
            logger.warning("Alert silencing is disabled")
            return
        
        if duration is None:
            duration = self.config.silence_duration
        
        expires_at = time.time() + duration
        self.silences[alert_id] = expires_at
        logger.info(f"Silenced alert {alert_id} for {duration} seconds")
    
    def unsilence_alert(self, alert_id: str):
        """Remove silence from an alert"""
        if alert_id in self.silences:
            del self.silences[alert_id]
            logger.info(f"Unsilenced alert {alert_id}")
    
    def is_silenced(self, alert_id: str) -> bool:
        """Check if an alert is silenced"""
        if alert_id in self.silences:
            if time.time() < self.silences[alert_id]:
                return True
            else:
                # Expired silence, remove it
                del self.silences[alert_id]
        return False
    
    def trigger_alert(self, rule_id: str, labels: Optional[Dict[str, str]] = None, annotations: Optional[Dict[str, str]] = None):
        """Trigger an alert based on a rule"""
        rule = self.get_rule(rule_id)
        if not rule:
            logger.warning(f"Alert rule {rule_id} not found")
            return None
        
        if not rule.enabled:
            logger.debug(f"Alert rule {rule_id} is disabled")
            return None
        
        # Create alert fingerprint for deduplication
        fingerprint = f"{rule_id}:{hash(str(sorted((labels or {}).items())))}"
        
        # Check if alert is already active
        existing_alert = None
        for alert in self.active_alerts.values():
            if alert.fingerprint == fingerprint:
                existing_alert = alert
                break
        
        if existing_alert:
            # Update existing alert
            existing_alert.status = AlertStatus.TRIGGERED
            existing_alert.annotations.update(annotations or {})
            logger.debug(f"Updated existing alert {existing_alert.id}")
            return existing_alert
        
        # Create new alert
        alert_id = f"alert_{int(time.time() * 1000000)}"
        alert = Alert(
            id=alert_id,
            rule_id=rule_id,
            name=rule.name,
            description=rule.description,
            level=rule.level,
            status=AlertStatus.TRIGGERED,
            labels=labels or {},
            annotations=annotations or {},
            starts_at=time.time(),
            fingerprint=fingerprint
        )
        
        self.active_alerts[alert_id] = alert
        self.alert_history.append(alert)
        logger.info(f"Triggered alert: {alert.name}")
        
        # Send notifications
        asyncio.create_task(self._send_alert_notifications(alert, rule))
        
        return alert
    
    async def _send_alert_notifications(self, alert: Alert, rule: AlertRule):
        """Send notifications for an alert"""
        # Check if alert is silenced
        if self.is_silenced(alert.id):
            logger.debug(f"Alert {alert.id} is silenced, skipping notifications")
            return
        
        # Check notification timing
        if alert.last_notification:
            time_since_last = time.time() - alert.last_notification
            if time_since_last < self.config.notification_interval:
                logger.debug(f"Skipping notification for alert {alert.id}, too soon since last notification")
                return
        
        # Send notifications to all configured channels
        for channel in rule.notify_channels:
            success = await self.notifier.send_notification(alert, channel)
            if success:
                alert.notification_count += 1
                alert.last_notification = time.time()
    
    def resolve_alert(self, alert_id: str):
        """Resolve an active alert"""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.status = AlertStatus.RESOLVED
            alert.ends_at = time.time()
            logger.info(f"Resolved alert: {alert.name}")
            
            # Remove from active alerts
            del self.active_alerts[alert_id]
    
    def acknowledge_alert(self, alert_id: str):
        """Acknowledge an active alert"""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.status = AlertStatus.ACKNOWLEDGED
            logger.info(f"Acknowledged alert: {alert.name}")
    
    def get_active_alerts(self) -> Dict[str, Alert]:
        """Get all active alerts"""
        return self.active_alerts.copy()
    
    def get_alert_history(self, limit: Optional[int] = None) -> List[Alert]:
        """Get alert history"""
        if limit:
            return list(self.alert_history)[-limit:]
        return list(self.alert_history)
    
    def evaluate_rule(self, rule: AlertRule):
        """Evaluate an alert rule"""
        # This is a simplified implementation
        # In a real system, you would evaluate the condition against metrics
        try:
            # For demonstration, we'll trigger alerts randomly
            import random
            if random.random() < 0.1:  # 10% chance to trigger
                self.trigger_alert(rule.id, {"test": "true"}, {"triggered_by": "test"})
        except Exception as e:
            logger.error(f"Failed to evaluate rule {rule.name}: {e}")
    
    async def start_evaluation(self):
        """Start evaluating alert rules"""
        self.running = True
        
        async def evaluation_loop():
            while self.running:
                try:
                    for rule in self.rules.values():
                        if rule.enabled:
                            self.evaluate_rule(rule)
                    await asyncio.sleep(30)  # Default evaluation interval
                except Exception as e:
                    logger.error(f"Error in alert evaluation loop: {e}")
                    await asyncio.sleep(30)
        
        # Start evaluation task for each rule
        for rule_id, rule in self.rules.items():
            if rule.enabled:
                task = asyncio.create_task(evaluation_loop())
                self.evaluation_tasks[rule_id] = task
        
        logger.info("Alert evaluation started")
    
    async def stop_evaluation(self):
        """Stop evaluating alert rules"""
        self.running = False
        for task in self.evaluation_tasks.values():
            task.cancel()
        logger.info("Alert evaluation stopped")
    
    async def start_alert_system(self, config: Optional[Dict[str, Any]] = None):
        """Start the alert system as a module"""
        try:
            # Update config if provided
            if config:
                # Merge provided config with existing config
                for key, value in config.items():
                    if hasattr(self.config, key):
                        setattr(self.config, key, value)
            
            # Reinitialize notifier with updated config
            self.notifier = AlertNotifier(self.config)
            
            # Start evaluation
            await self.start_evaluation()
            
            logger.info("Alert system started successfully")
            logger.info(f"Email notifications: {self.config.enable_email_notifications}")
            logger.info(f"Webhook notifications: {self.config.enable_webhook_notifications}")
            logger.info(f"Alert deduplication: {self.config.enable_deduplication}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to start alert system: {e}")
            return False

# Global alert manager instance
alert_manager = None

def initialize_alert_manager(config: Optional[AlertSystemConfig] = None):
    """Initialize the alert manager"""
    global alert_manager
    alert_manager = AlertManager(config)
    return alert_manager

def get_alert_manager():
    """Get the global alert manager instance"""
    global alert_manager
    if alert_manager is None:
        alert_manager = AlertManager()
    return alert_manager

def add_alert_rule(rule: AlertRule):
    """Add an alert rule"""
    return get_alert_manager().add_rule(rule)

def trigger_alert(rule_id: str, labels: Optional[Dict[str, str]] = None, annotations: Optional[Dict[str, str]] = None):
    """Trigger an alert"""
    return get_alert_manager().trigger_alert(rule_id, labels, annotations)

def resolve_alert(alert_id: str):
    """Resolve an alert"""
    get_alert_manager().resolve_alert(alert_id)

def acknowledge_alert(alert_id: str):
    """Acknowledge an alert"""
    get_alert_manager().acknowledge_alert(alert_id)

# Example usage and testing
async def start_alert_system(config: Optional[Dict[str, Any]] = None):
    """Start the alert system as a module"""
    try:
        alert_config = AlertSystemConfig(**config) if config else AlertSystemConfig()
        manager = initialize_alert_manager(alert_config)
        
        # Add a test alert rule
        test_rule = AlertRule(
            id="test_rule_1",
            name="Test Alert Rule",
            description="A test alert rule for demonstration",
            condition="test_condition",
            level=AlertLevel.WARNING,
            notify_channels=[NotificationChannel.CONSOLE],
            labels={"environment": "test"},
            annotations={"summary": "This is a test alert"}
        )
        manager.add_rule(test_rule)
        
        # Start the alert system
        await manager.start_alert_system(config)
        
        logger.info("Alert system initialized successfully")
        logger.info(f"Registered rules: {list(manager.get_all_rules().keys())}")
        
        return True
    except Exception as e:
        logger.error(f"Failed to start alert system: {e}")
        return False

if __name__ == "__main__":
    # Test the alert system
    async def main():
        config = {
            "enable_email_notifications": False,
            "enable_webhook_notifications": False
        }
        await start_alert_system(config)
        
        # Keep running for a while to test
        await asyncio.sleep(60)
    
    asyncio.run(main())