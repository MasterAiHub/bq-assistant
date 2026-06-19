import logging
from logging.handlers import RotatingFileHandler
import os

class AuditLogger:
    """Centralized audit logging for security-related events"""

    def __init__(self, log_file=".logs/security.log", max_bytes=10*1024*1024, backup_count=5):
        self.logger = logging.getLogger("audit_logger")
        self.logger.setLevel(logging.INFO)

        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # File handler for audit logs
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console handler for immediate feedback during development
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_event(self, event_type: str, user_id: str = "N/A", ip_address: str = "N/A", details: str = ""):
        """Logs a security event."""
        self.logger.info(f"Event Type: {event_type}, User ID: {user_id}, IP Address: {ip_address}, Details: {details}")

    def log_warning(self, event_type: str, user_id: str = "N/A", ip_address: str = "N/A", details: str = ""):
        """Logs a security warning."""
        self.logger.warning(f"Event Type: {event_type}, User ID: {user_id}, IP Address: {ip_address}, Details: {details}")

    def log_error(self, event_type: str, user_id: str = "N/A", ip_address: str = "N/A", details: str = ""):
        """Logs a security error."""
        self.logger.error(f"Event Type: {event_type}, User ID: {user_id}, IP Address: {ip_address}, Details: {details}")
