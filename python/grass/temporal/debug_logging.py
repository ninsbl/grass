"""Debug messages of the temporal framework based on the logging module

Debug messages are sent to the ``grass.temporal`` logger. They use the debug
levels of GRASS (1 to 5, see ``G_debug()``), which are mapped to the logging
levels 10 (debug level 1) to 6 (debug level 5), so enabling a higher GRASS
debug level enables more detailed messages.

By default, messages are shown the same way as the debug messages of the GRASS
libraries: if the GRASS debug level (``g.gisenv set="DEBUG=3"``) is at least the
level of the message, ``D<level>/<debug level>: <message>`` is written to
stderr or appended to the file given by ``GRASS_DEBUG_FILE``. This is set up by
:func:`grass.temporal.init`. Applications that configure the ``grass.temporal``
logger themselves, for example by adding a handler, are left alone.

The messages are formatted lazily, so disabled messages cost almost nothing:

.. code-block:: python

    log_debug(2, "Gathering information of map <%s>", map_id)

SPDX-FileCopyrightText: 2026 GRASS Development Team
SPDX-License-Identifier: GPL-2.0-or-later
"""

from __future__ import annotations

import logging
import os
import sys

__all__ = ["configure_debug_logging", "log_debug", "logger"]

logger = logging.getLogger("grass.temporal")
# Keeps the logging module from printing unrelated records to stderr when
# the application did not configure logging
logger.addHandler(logging.NullHandler())

MAX_DEBUG_LEVEL = 5
# GRASS debug level n has the logging level _LEVEL_OFFSET - n
_LEVEL_OFFSET = logging.DEBUG + 1


class GrassDebugHandler(logging.Handler):
    """Write debug records in the format of G_debug()

    :param debug_level: The GRASS debug level, shown in every message
    """

    def __init__(self, debug_level: int) -> None:
        super().__init__()
        self.debug_level = debug_level

    def emit(self, record: logging.LogRecord) -> None:
        try:
            line = f"D{_LEVEL_OFFSET - record.levelno}/{self.debug_level}: "
            line += record.getMessage() + "\n"
            debug_file = os.environ.get("GRASS_DEBUG_FILE")
            if debug_file:
                with open(debug_file, "a", encoding="utf-8") as stream:
                    stream.write(line)
            else:
                sys.stderr.write(line)
                sys.stderr.flush()
        except Exception:
            self.handleError(record)


_grass_handler: GrassDebugHandler | None = None


def log_debug(level: int, msg: str, *args) -> None:
    """Log a debug message

    :param level: The GRASS debug level of the message (1 to 5)
    :param msg: The message, a format string if arguments are given
    :param args: Arguments of the message, formatted only if the message is shown
    """
    # logger.log() checks the level first and the call stack is only
    # inspected for enabled messages
    logger.log(_LEVEL_OFFSET - level, msg, *args, stacklevel=2)


def configure_debug_logging(debug_level: int) -> None:
    """Show debug messages up to a GRASS debug level

    The logger is left unchanged if the application added handlers to it.
    Calling the function again replaces the previous configuration.

    :param debug_level: The GRASS debug level, 0 (no messages) to 5. Values
                        out of this range are limited to it.
    """
    global _grass_handler
    if _grass_handler is not None:
        logger.removeHandler(_grass_handler)
        _grass_handler = None
        logger.setLevel(logging.NOTSET)
        logger.propagate = True
    if any(not isinstance(handler, logging.NullHandler) for handler in logger.handlers):
        return
    debug_level = max(0, min(debug_level, MAX_DEBUG_LEVEL))
    if debug_level == 0:
        return
    _grass_handler = GrassDebugHandler(debug_level)
    logger.addHandler(_grass_handler)
    logger.setLevel(_LEVEL_OFFSET - debug_level)
    # The records are shown by the handler above
    logger.propagate = False
