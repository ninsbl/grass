#!/usr/bin/env python3

############################################################################
#
# MODULE:	    t.copy
# AUTHOR(S):	Markus Metz
#
# PURPOSE:	    Create a copy of a space time dataset
# SPDX-FileCopyrightText: 2021 GRASS Development Team
# SPDX-License-Identifier: GPL-2.0-or-later
#
#############################################################################

# %module
# % description: Creates a copy of a space time raster dataset.
# % keyword: temporal
# % keyword: copy
# % keyword: time
# %end

# %option G_OPT_STDS_INPUT
# %end

# %option G_OPT_STDS_TYPE
# % guidependency: input
# % guisection: Required
# % options: strds, str3ds, stvds
# %end

# %option G_OPT_STDS_OUTPUT
# %end

# %flag
# % key: c
# % label: Also copy maps of the space-time dataset
# % description: By default the old maps are only registered in the new dataset.
# %end


import grass.script as gs
from grass.tools import Tools

############################################################################


def copy_maps_and_register(output_stds, old_maps, maptype, element, copy_maps):
    """Copy the maps if requested and register them in the new dataset."""
    import grass.temporal as tgis

    tools = Tools()

    dbif = output_stds.dbif
    mapset = output_stds.get_mapset()
    overwrite = gs.overwrite()

    new_maps = None
    if copy_maps:
        gs.verbose(_("Copying %s maps to the current mapset...") % maptype)
        new_maps = []
        num_maps = len(old_maps)
        count = 0

        for map in old_maps:
            count += 1
            map_id = map.get_id()
            map_name = map_id
            map_mapset = mapset
            if "@" in map_id:
                map_name, map_mapset = map_id.split("@")

            if map_mapset != mapset:
                found = gs.find_file(name=map_name, element=element, mapset=mapset)
                if found["name"] is not None and len(found["name"]) > 0:
                    gs.fatal(
                        _("A %s map <%s> exists already in the current mapset <%s>.")
                        % (maptype, map_name, mapset)
                    )

                kwargs = {maptype: f"{map_id},{map_name}"}
                tools.g_copy(**kwargs)
            else:
                # the map is already in the current mapset
                gs.message(
                    _("The %s map <%s> is already in the current mapset, not copying")
                    % (maptype, map_name)
                )

            if count % 10 == 0:
                gs.percent(count, num_maps, 1)

            new_map = tgis.open_new_map_dataset(
                map_name,
                None,
                type=maptype,
                temporal_extent=map.get_temporal_extent(),
                overwrite=overwrite,
                dbif=dbif,
            )
            # semantic label
            semantic_label = map.metadata.get_semantic_label()
            if semantic_label is not None and semantic_label != "None":
                new_map.metadata.set_semantic_label(semantic_label)

            new_maps.append(new_map)
    else:
        # don't copy maps, use old maps
        new_maps = old_maps

    # Register the maps in the database
    for map in new_maps:
        # Insert map in temporal database
        if not map.is_in_db(dbif, mapset):
            semantic_label = map.metadata.get_semantic_label()
            map.load()
            # semantic labels are not yet properly implemented in TGIS
            if semantic_label is not None and semantic_label != "None":
                map.metadata.set_semantic_label(semantic_label)
            map.insert(dbif)
        output_stds.register_map(map, dbif)

    # Update the spatio-temporal extent and the metadata table entries
    output_stds.update_from_registered_maps(dbif)


def main():
    # lazy imports
    import grass.temporal as tgis

    # Get the options
    input = options["input"]
    output = options["output"]
    stdstype = options["type"]

    type_mapping = {
        "strds": {"maptype": "raster", "element": "cell"},
        "str3ds": {"maptype": "raster_3d", "element": "g3dcell"},
        "stvds": {"maptype": "vector", "element": "vector"},
    }
    maptype = type_mapping[stdstype]["maptype"]
    element = type_mapping[stdstype]["element"]

    try:
        input_stds = tgis.open(options["input"], "r", stds_type=stdstype)
    except (ValueError, OSError) as error:
        gs.fatal(str(error))

    with input_stds:
        old_maps = input_stds.get_registered_maps_as_objects(dbif=input_stds.dbif)

        if not old_maps:
            gs.warning(
                _("Empty space-time %s dataset <%s>, nothing to copy")
                % (maptype, input)
            )
            return

        temporal_type, semantic_type, title, description = (
            input_stds.get_initial_values()
        )
        # The new dataset is created first, so that an existing dataset or
        # another mapset than the current one is detected before maps are copied
        try:
            output_stds = tgis.open(
                output,
                "w",
                stds_type=stdstype,
                temporal_type=temporal_type,
                semantic_type=semantic_type,
                title=title,
                description=description,
                dbif=input_stds.dbif,
            )
        except (ValueError, OSError) as error:
            gs.fatal(str(error))

        with output_stds:
            try:
                copy_maps_and_register(
                    output_stds, old_maps, maptype, element, flags["c"]
                )
            except BaseException:
                # Do not leave an empty dataset behind
                output_stds.delete(output_stds.dbif)
                raise


###############################################################################

if __name__ == "__main__":
    options, flags = gs.parser()
    main()
