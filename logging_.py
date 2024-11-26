import logging.config

# Custom logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Keep other loggers intact
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {  # Console output
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        }
    },
    "loggers": {
        "similarity": {  # Your app's logger
            "handlers": ["console"],
            "level": "INFO",  # Log level for your app
            "propagate": False,  # Prevent messages from propagating to root logger
        },
    },
}

# Apply the logging configuration
logging.config.dictConfig(LOGGING_CONFIG)


logger = logging.getLogger("similarity")
