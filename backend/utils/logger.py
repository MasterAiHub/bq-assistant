import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Root logger configuration
    logging.basicConfig(
        level=logging.INFO,
        format=
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(os.path.join(log_dir, "app.log"), maxBytes=10485760, backupCount=5),
            logging.StreamHandler()
        ]
    )

    # Specific logger for security events
    security_logger = logging.getLogger("audit_logger")
    security_logger.setLevel(logging.INFO)
    security_handler = RotatingFileHandler(os.path.join(log_dir, "security.log"), maxBytes=10485760, backupCount=5)
    security_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    security_handler.setFormatter(security_formatter)
    security_logger.addHandler(security_handler)
    security_logger.propagate = False # Prevent security logs from going to root logger twice

    # Suppress verbose loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    logging.info("Logging setup complete.")
