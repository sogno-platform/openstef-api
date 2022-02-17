import logging
import logging.config

import structlog
import ecs_logging
import elasticapm.handlers.structlog

from app.core.settings import Settings


def add_application_metadata(logger, method_name, event_dict):
    """Add additional API metadata to the passed event dictionary.

    Note:
        The unused arguments are still passed by the caller and need to be caught.

    Args:
        logger: wrapped logger object
        method_name: name of the wrapper method
        event_dict: current context and event

    Returns:
        Dictionary with possibly extra fields
    """
    if "app_version" not in event_dict:
        event_dict["app_version"] = Settings.app_version

    return event_dict


def get_shared_processors():
    """Get shared processors.

    These processors are indented to be usef for both the standard logging dict config
    as well as the structlog configure processors.

    Returns:
        list: Shared processors
    """
    return [
        structlog.processors.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso")
    ]


def get_dict_config():
    """Get dict config.

    Get logging dict config to be used to configure the standard logger by:
    logging.config.dictConfig(dict_config). Depending on whether the `log_json_output`
    variable is set the formatter of the default handler will be set to `structlog_ecs`
    or `structlog_plain`. The `structlog_ecs` formatter will format log messages
    produced by the standard logger in ECS format. The `structlog_plain` formatter will
    format log messages produced by the standard logger in default human readable
    structlog format.

    Returns:
        dict: logging dict config
    """

    pre_chain_plain = get_shared_processors()

    if Settings.log_json_output:
        default_formatter = "structlog_ecs"
    else:
        default_formatter = "structlog_plain"

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structlog_ecs": {
                "()": ecs_logging.StdlibFormatter,
                # This is passed as an argument to ecs_logging.StdlibFormatter
                # Make the ECS logger a bit less verbose
                # extra fields are only shown for levels info or below
                "exclude_fields": [
                    "log.original",
                    "process",
                    "log.origin",
                ],
            },
            "structlog_plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=False),
                "foreign_pre_chain": pre_chain_plain,
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": default_formatter,
                "level": Settings.log_level,
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": Settings.log_level,
                "propagate": True,
            },
        }
    }


def initialize_logging():
    # configure stdlib logging
    dict_config = get_dict_config()
    logging.config.dictConfig(dict_config)

    # configure json (ecs) structlog
    if Settings.log_json_output:
        # Convert log level string to int
        log_level = getattr(logging, Settings.log_level.upper())
        structlog.configure(
            processors=[
                  elasticapm.handlers.structlog.structlog_processor,
                  ecs_logging.StructlogFormatter(),
            ],
            # Only log messages above log level
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
        )
        return

    # configure default structlog
    shared_processors = get_shared_processors()

    processors = (
        [
            structlog.stdlib.filter_by_level
        ] +
        shared_processors +
        [
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ]
    )

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
