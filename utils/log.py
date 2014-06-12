import logging
import os


def _get_formatter():
    """Return a nice common log formatter"""

    return logging.Formatter('%(asctime)s [%(levelname)8s] %(message)s')


def _expand_path(path):
    """Expands ~ and variables like $HOME from paths"""

    return os.path.expanduser(
        os.path.expandvars(
            path
        )
    )


def _get_log():
    """Set up a basic logger"""

    logger = logging.getLogger('PyWebStatMon')
    logger.setLevel(logging.CRITICAL)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(_get_formatter())

    logger.addHandler(ch)

    return logger

log = _get_log()


def enable():
    """
    Actually make the log output be visible.

    Exists so tests' log output will get discarded.
    """

    log.setLevel(logging.DEBUG)


def set_log_file(log_file):
    """Configure the logger above to log to a file"""

    log_file = _expand_path(log_file)

    fh = logging.FileHandler(log_file)

    fh.setLevel(logging.DEBUG)
    fh.setFormatter(_get_formatter())

    log.addHandler(fh)
