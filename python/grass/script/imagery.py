"""
Imagery related functions to be used in Python scripts.

:Usage:
  .. code-block:: python

    import grass.script as gs

    gs.imagery.group_to_dict(imagery_group)
    ...

SPDX-FileCopyrightText: 2024 Stefan Blumentrath
SPDX-FileCopyrightText: GRASS Development Team
SPDX-License-Identifier: GPL-2.0-or-later

.. sectionauthor:: Stefan Blumentrath
"""

import json

from .core import read_command, warning, fatal
from .raster import raster_info

# Combinations of (dict_keys, dict_values) that i.group can return directly
_I_GROUP_STRUCTURES = {
    ("indices", "map_names"): "index-mapname",
    ("semantic_labels", "map_names"): "semantic_label-mapname",
    ("map_names", "semantic_labels"): "mapname-semantic_label",
    ("map_names", "indices"): "mapname-index",
}


def group_to_dict(
    imagery_group_name,
    subgroup=None,
    dict_keys="semantic_labels",
    dict_values="map_names",
    fill_semantic_label=True,
    env=None,
):
    """Create a dictionary to represent an imagery group with metadata.

    Depending on the dict_keys option, the returned dictionary uses either
    the names of the raster maps ("map_names"), their row indices in the group
    ("indices") or their associated semantic_labels ("semantic_labels") as keys.
    The default is to use semantic_labels. Note that map metadata
    of the maps in the group have to be read to get the semantic label,
    in addition to the group file. The same metadata is read when the
    "metadata" is requested as dict_values. Other supported dict_values
    are "map_names" (default), "semantic_labels", or "indices".

    The function wraps the structure option of i.group. Combinations
    of dict_keys and dict_values supported by i.group are returned from
    a single call. Other combinations, fill_semantic_label=False, and
    "metadata" are built from the map names and semantic labels
    reported by i.group; only "metadata" requires additional calls
    (raster_info() for each map).

    The function can also operate on the level of subgroups. In case a
    non-existing (or empty sub-group) is requested a warning is printed
    and an empty dictionary is returned (following the behavior of i.group).

    :Example:
      .. code-block:: pycon

        >>> run_command("g.copy", raster="lsat7_2000_10,lsat7_2000_10")
        >>> run_command("r.support", raster="lsat7_2000_10", semantic_label="L8_1")
        >>> run_command("g.copy", raster="lsat7_2000_20,lsat7_2000_20")
        >>> run_command("r.support", raster="lsat7_2000_20", semantic_label="L8_2")
        >>> run_command("g.copy", raster="lsat7_2000_30,lsat7_2000_30")
        >>> run_command("r.support", raster="lsat7_2000_30", semantic_label="L8_3")
        >>> run_command("i.group", group="L8_group",
        >>>             input="lsat7_2000_10,lsat7_2000_20,lsat7_2000_30")
        >>> group_to_dict("L8_group")  # doctest: +ELLIPSIS
        {"L8_1": "lsat7_2000_10", ... "L8_3": "lsat7_2000_30"}
        >>> run_command("g.remove", flags="f", type="group", name="L8_group")
        >>> run_command("g.remove", flags="f", type="raster",
        >>>             name="lsat7_2000_10,lsat7_2000_20,lsat7_2000_30")

    :param str imagery_group_name: Name of the imagery group to process (or None)
    :param str subgroup: Name of the imagery sub-group to process (or None)
    :param str dict_keys: What to use as key for dictionary. It can be either
                         "semantic_labels" (default), "map_names" or "indices"
    :param str dict_values: What to use as values for dictionary. It can be either
                           "map_names" (default), "semanic_labels", "indices" or
                           "metadata" (to return dictionaries with full map metadata)
    :param bool fill_semantic_label: If maps in a group do not have a semantic
                                     label, their index in the group is used
                                     instead (default). Otherwise None / "none"
                                     is used.
    :param dict env: Environment to use when parsing the imagery group

    :return: dictionary representing an imagery group with it's maps and their
             semantic labels, row indices in the group, or metadata
    :rtype: dict
    """
    if dict_keys not in {"indices", "map_names", "semantic_labels"}:
        msg = f"Invalid dictionary keys <{dict_keys}> requested"
        raise ValueError(msg)

    if dict_values not in {"indices", "map_names", "semantic_labels", "metadata"}:
        msg = f"Invalid dictionary values <{dict_values}> requested"
        raise ValueError(msg)

    structure = _I_GROUP_STRUCTURES.get((dict_keys, dict_values))
    if dict_keys == "semantic_labels" and not fill_semantic_label:
        structure = None
    # Maps with their semantic labels (None if missing) are enough for any
    # combination except metadata
    maps_in_group = json.loads(
        read_command(
            "i.group",
            group=imagery_group_name,
            subgroup=subgroup,
            format="json",
            structure=structure or "mapname-semantic_label",
            quiet=True,
            env=env,
        )
    )

    if subgroup and not maps_in_group:
        warning(
            _("Empty result returned for subgroup <{sg}> in group <{g}>").format(
                sg=subgroup, g=imagery_group_name
            ),
            env=env,
        )

    if structure:
        if structure == "mapname-semantic_label":
            # Keep the literal reported by r.info for a missing semantic label
            return {
                raster_map: '"none"' if label is None else label
                for raster_map, label in maps_in_group.items()
            }
        return maps_in_group

    group_dict = {}
    for idx, (raster_map, label) in enumerate(maps_in_group.items(), start=1):
        fields = {
            "map_names": raster_map,
            "indices": str(idx),
            "semantic_labels": '"none"' if label is None else label,
        }

        if dict_keys == "semantic_labels" and label is None:
            if not fill_semantic_label:
                fatal(
                    _(
                        "Semantic label missing for raster map {m} in group <{g}>."
                    ).format(m=raster_map, g=imagery_group_name),
                    env=env,
                )
            key = str(idx)
        else:
            key = fields[dict_keys]

        if dict_values == "metadata":
            val = raster_info(raster_map, env=env)
        else:
            val = fields[dict_values]
        if key in group_dict:
            warning(
                _(
                    "Key {k} from raster map {m} already present in group dictionary."
                    "Overwriting existing entry..."
                ).format(k=key, m=raster_map),
                env=env,
            )
        group_dict[key] = val
    return group_dict
