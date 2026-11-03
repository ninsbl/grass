"""Open or create space time datasets with a file-like interface

The :func:`open` function replaces the functions of the ``open_stds`` module
(``open_old_stds()``, ``open_new_stds()`` and ``check_new_stds()``). It
initializes the temporal framework and the database connection when needed
and supports the modes ``"r"`` (read), ``"w"`` (create) and ``"a"`` (append).

Usage:

.. code-block:: python

    import grass.temporal as tgis

    # Open an existing space time dataset for reading
    with tgis.open("precip@PERMANENT", "r", stds_type="strds") as stds:
        maps = stds.get_registered_maps("id,start_time")

    # Open a new space time dataset for writing
    with tgis.open(
        "precip_new",
        "w",
        stds_type="strds",
        title="Precipitation",
        description="Monthly precipitation",
        temporal_type="absolute",
    ) as stds:
        stds.register_map(raster_map, dbif=stds.dbif)

    # Open an existing space time dataset for reading with error handling
    try:
        stds = tgis.open(name, "r", stds_type=type)
    except (ValueError, OSError) as error:
        gs.fatal(str(error))

    with stds:
        maps = stds.get_registered_maps("id,start_time")

SPDX-FileCopyrightText: 2026 GRASS Development Team
SPDX-License-Identifier: GPL-2.0-or-later
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import grass.script as gs

from .core import get_current_mapset, init_dbif, init_if_needed
from .factory import dataset_factory
from .utils import normalize_stds_type, parse_stds_name

if TYPE_CHECKING:
    from collections.abc import Mapping

    from .abstract_space_time_dataset import AbstractSpaceTimeDataset
    from .core import SQLDatabaseInterfaceConnection

__all__ = ["open"]

_TEMPORAL_TYPES = {"absolute", "relative"}


def _not_found(name: str, stds_type: str) -> FileNotFoundError:
    msg = _("Space time dataset <{name}> of type <{stds_type}> not found").format(
        name=name, stds_type=stds_type
    )
    return FileNotFoundError(msg)


def _find_stds(
    stds_type: str,
    name: str,
    mapset: str | None,
    semantic_label: str | None,
    dbif: SQLDatabaseInterfaceConnection,
) -> AbstractSpaceTimeDataset:
    """Find a space time dataset for reading and select it from the database

    Without a mapset, the current mapset is searched first, then the
    other mapsets of the connection.
    """
    current_mapset = get_current_mapset()
    if mapset:
        dbif.add_mapset(mapset)
        candidates = [mapset]
    else:
        candidates = [current_mapset] + [
            tgis_mapset
            for tgis_mapset in dbif.tgis_mapsets
            if tgis_mapset != current_mapset
        ]
    for candidate in candidates:
        # The current mapset has no temporal database if it was never needed
        if candidate not in dbif.tgis_mapsets:
            continue
        stds = dataset_factory(stds_type, f"{name}@{candidate}")
        if semantic_label:
            stds.set_semantic_label(semantic_label)
        if stds.is_in_db(dbif):
            stds.select(dbif)
            return stds
    raise _not_found(f"{name}@{mapset}" if mapset else name, stds_type)


def _open_for_writing(
    stds_type: str,
    name: str,
    mapset: str | None,
    dbif: SQLDatabaseInterfaceConnection,
    *,
    replace: bool,
    overwrite: bool,
    create: bool,
    temporal_type: str,
    semantic_type: str,
    title: str | None,
    description: str | None,
    env: Mapping[str, str],
) -> AbstractSpaceTimeDataset:
    """Open a dataset in the current mapset and create it if requested

    :param replace: Replace the dataset if it exists, fail unless
                    ``overwrite`` is true
    :param overwrite: Allow replacing
    :param create: Create the dataset if it does not exist
    :param env: The session environment
    """
    stds = dataset_factory(stds_type, f"{name}@{mapset or get_current_mapset()}")
    if stds.get_readonly():
        msg = _(
            "Space time datasets can only be created or modified in the "
            "current mapset, not in <{mapset}>"
        ).format(mapset=stds.get_mapset())
        raise PermissionError(msg)
    stds_id = stds.get_id()
    # A connection which was created before the temporal database of the
    # current mapset existed, e.g., for reading, does not know the database
    dbif.add_mapset(stds.get_mapset())
    exists = stds.is_in_db(dbif)
    if exists and replace:
        if not overwrite:
            msg = _(
                "Space time dataset <{name}> is already in the database. "
                "Use overwrite=True to replace it."
            ).format(name=stds_id)
            raise FileExistsError(msg)
        gs.warning(
            _(
                "Overwriting space time dataset <{name}> and unregistering all maps"
            ).format(name=stds_id),
            env=env,
        )
        stds.delete(dbif)
        # delete() resets the object
        stds = dataset_factory(stds_type, stds_id)
        exists = False
    if exists:
        stds.select(dbif)
    elif create:
        stds.set_initial_values(
            temporal_type=temporal_type,
            semantic_type=semantic_type,
            title=title,
            description=description,
        )
        stds.insert(dbif)
    else:
        raise _not_found(stds_id, stds_type)
    return stds


def open(  # noqa: A001
    name: str,
    mode: str = "r",
    stds_type: str = "strds",
    *,
    dbif: SQLDatabaseInterfaceConnection | None = None,
    overwrite: bool | None = None,
    temporal_type: str | None = None,
    semantic_type: str | None = None,
    title: str | None = None,
    description: str | None = None,
    env: Mapping[str, str] | None = None,
) -> AbstractSpaceTimeDataset:
    """Open or create a space time dataset

    The temporal framework is initialized if needed and a database connection
    is opened. The returned object is the space time dataset (a
    SpaceTimeRasterDataset, SpaceTimeRaster3DDataset or
    SpaceTimeVectorDataset) which can be used as a context manager to close
    the connection. The connection is available as the ``dbif`` attribute
    of the dataset.

    The modes are:

    - ``"r"``: Open an existing dataset for reading. The dataset is
      read-only: Methods which modify it raise :class:`PermissionError`.
      No temporal database is created in the current mapset.
    - ``"w"``: Create a new dataset in the current mapset. An existing
      dataset is only replaced if ``overwrite`` is true.
    - ``"a"``: Open an existing dataset in the current mapset for modification,
      e.g., to register maps or to update the metadata (call ``update()``).
      If the dataset does not exist, it is created when at least one of
      ``temporal_type``, ``semantic_type``, ``title`` or ``description``
      is given. These options are ignored for an existing dataset.

    :param name: Name of the dataset. For reading, ``name@mapset`` can
                 reference other mapsets. Without mapset, the current mapset
                 is searched first, then the search path. The other modes
                 only use the current mapset. For ``strds``, reading accepts
                 a semantic label filter (``name.label``).
    :param mode: ``"r"``, ``"w"`` or ``"a"``
    :param stds_type: Type of the dataset: strds, str3ds or stvds. The names
                      raster, raster3d and vector are accepted as well.
    :param dbif: Database connection to use. It is not closed by the
                 returned object. A new connection is created by default.
    :param overwrite: Allow replacing an existing dataset in mode ``"w"``.
                      By default, the GRASS overwrite environment setting
                      (``GRASS_OVERWRITE``) is used.
    :param temporal_type: ``"absolute"`` (default) or ``"relative"``, to
                          create a dataset
    :param semantic_type: Semantic type of the dataset (default is ``"mean"``),
                          to create a dataset
    :param title: Title of the dataset, to create a dataset
    :param description: Description of the dataset, to create a dataset
    :param env: Environment of the GRASS session to open the dataset in, the
                environment of the process by default. A copy of the
                environment at the time of the call is available as the ``env``
                attribute of the dataset. The temporal framework is set up for
                one session at a time: opening a dataset in another session
                switches it, and datasets opened earlier cannot be modified
                afterwards (a :class:`RuntimeError` is raised). Reading
                still works if the ``dbif`` of the dataset is passed to the
                methods, otherwise they connect to the current session of the
                framework. Other functions of the framework still use the
                environment of the process.

    :return: The opened space time dataset

    :raises ValueError: for invalid arguments
    :raises FileNotFoundError: if the dataset to read or append to does not
                               exist and cannot be created
    :raises FileExistsError: if the dataset to create exists and ``overwrite``
                             is not set
    :raises PermissionError: if creating or modifying a dataset of
                             another mapset is requested
    """
    if mode not in {"r", "w", "a"}:
        msg = _("Invalid mode <{}>, use 'r', 'w' or 'a'").format(mode)
        raise ValueError(msg)
    stds_type = normalize_stds_type(stds_type)
    has_creation_options = any(
        option is not None
        for option in (temporal_type, semantic_type, title, description)
    )
    if mode == "r" and has_creation_options:
        msg = _(
            "The options temporal_type, semantic_type, title and "
            "description are not valid in mode 'r'"
        )
        raise ValueError(msg)
    temporal_type = temporal_type or "absolute"
    if temporal_type not in _TEMPORAL_TYPES:
        msg = _("Unknown temporal type <{}>").format(temporal_type)
        raise ValueError(msg)

    ident, mapset, semantic_label = parse_stds_name(name, stds_type)
    create = mode == "w" or (mode == "a" and has_creation_options)
    if mode != "r" and semantic_label:
        msg = _("Illegal dataset name <{}>. Character '.' not allowed.").format(name)
        raise ValueError(msg)
    if create and not gs.legal_name(ident):
        msg = _("Illegal dataset name <{}>").format(name)
        raise ValueError(msg)

    # Reading does not need a temporal database in the current mapset
    init_if_needed(raise_fatal_error=True, skip_db_init=mode == "r", env=env)
    session_env = dict(os.environ if env is None else env)
    if overwrite is None:
        overwrite = session_env.get("GRASS_OVERWRITE", "0") != "0"
    dbif, close_dbif = init_dbif(dbif)
    try:
        if mode == "r":
            stds = _find_stds(stds_type, ident, mapset, semantic_label, dbif)
            stds.set_readonly(True)
        else:
            stds = _open_for_writing(
                stds_type,
                ident,
                mapset,
                dbif,
                replace=mode == "w",
                overwrite=overwrite,
                create=create,
                temporal_type=temporal_type,
                semantic_type=semantic_type or "mean",
                title=title,
                description=description,
                env=session_env,
            )
    except BaseException:
        if close_dbif:
            dbif.close()
        raise
    stds.set_dbif(dbif, close_on_exit=close_dbif)
    stds.pin_session(session_env)
    return stds
