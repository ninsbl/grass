"""Utility functions and classes for the temporal framework.

(C) 2026 by the GRASS Development Team
This program is free software under the GNU General Public
License (>=v2). Read the file COPYING that comes with GRASS
for details.

:authors: GRASS Development Team
"""

from __future__ import annotations

import contextlib
import json
import os
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping

# Accepted names of space time dataset types and the type they stand for.
# The map type names are accepted since several tools pass the type of the
# registered maps instead of the type of the space time dataset.
STDS_TYPES = {
    "strds": "strds",
    "raster": "strds",
    "rast": "strds",
    "str3ds": "str3ds",
    "raster3d": "str3ds",
    "rast3d": "str3ds",
    "raster_3d": "str3ds",
    "stvds": "stvds",
    "vector": "stvds",
    "vect": "stvds",
}


@contextlib.contextmanager
def applied_environment(env: Mapping[str, str] | None) -> Iterator[None]:
    """Temporarily make a session environment the environment of the process

    Subprocesses started in the context, e.g., with the ``fork`` start method of
    :mod:`multiprocessing`, inherit this environment. The environment of the
    process is restored when leaving the context, so the context must not be
    used while other threads depend on the environment.

    :param env: The environment to apply, None or the environment of the
                process to leave everything as it is
    """
    if env is None or env is os.environ:
        yield
        return
    saved = dict(os.environ)
    os.environ.clear()
    os.environ.update(env)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(saved)


def normalize_stds_type(stds_type: str) -> str:
    """Return the space time dataset type (strds, str3ds or stvds) for a type name

    :param stds_type: A space time dataset type (strds, str3ds, stvds) or the
                      name of the corresponding map type (raster, rast,
                      raster3d, rast3d, raster_3d, vector, vect)

    :raises ValueError: if the type is unknown
    """
    try:
        return STDS_TYPES[stds_type]
    except KeyError:
        msg = _("Unknown space time dataset type <{}>").format(stds_type)
        raise ValueError(msg) from None


def split_name_mapset(ident: str) -> tuple[str, str | None]:
    """Split a dataset name of the form name or name@mapset

    :param ident: The name of a dataset with or without mapset

    :return: Tuple of the name and the mapset, the mapset is None if
             the name has none

    :raises ValueError: if the name or the given mapset is empty
    """
    name, separator, mapset = ident.partition("@")
    if not name or (separator and not mapset):
        msg = _("Invalid dataset name <{}>").format(ident)
        raise ValueError(msg)
    return name, mapset if separator else None


def parse_stds_name(
    ident: str, stds_type: str = "strds"
) -> tuple[str, str | None, str | None]:
    """Parse the name of a space time dataset given by a user

    The name can contain the mapset (name@mapset). For space time raster
    datasets it can in addition contain a semantic label that selects the
    maps with this label (name.label or name.label@mapset). Space time
    3D raster and vector datasets have no semantic labels, so a dot is
    part of their names.

    :param ident: The name of a space time dataset
    :param stds_type: The type of the space time dataset, see
                      :func:`normalize_stds_type`

    :return: Tuple of the name, the mapset and the semantic label, the latter
             two are None if the name has none

    :raises ValueError: if the type is unknown or the name is invalid
    """
    stds_type = normalize_stds_type(stds_type)
    name, mapset = split_name_mapset(ident)
    semantic_label = None
    if stds_type == "strds" and "." in name:
        name, semantic_label = name.split(".", 1)
        if not name or not semantic_label or "." in semantic_label:
            msg = _("Invalid semantic label in <{}>").format(ident)
            raise ValueError(msg)
    return name, mapset, semantic_label


class TemporalJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder with datetime support for GRASS GIS.

    Handles serialization of datetime objects to a ISO 8601-like string,
    that can be handled by SQLite3 and temporal modules.
    Can be used across GRASS modules that need JSON output with temporal data.

    Example:

    .. code-block:: pycon

        >>> import json
        >>> from datetime import datetime
        >>> data = {"timestamp": datetime(2024, 1, 15, 10, 30)}
        >>> json.dumps(data, cls=TemporalJSONEncoder)
        '{"timestamp": "2024-01-15 10:30:00"}'
    """

    def default(self, obj):
        """Override default JSON encoding for datetime objects.

        :param obj: Object to encode
        :return: ISO 8601-like formatted string for datetime objects,
                 or calls parent encoder for other types
        """
        if isinstance(obj, datetime):
            if obj.microsecond > 0:
                return obj.strftime("%Y-%m-%d %H:%M:%S.%f")
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)
