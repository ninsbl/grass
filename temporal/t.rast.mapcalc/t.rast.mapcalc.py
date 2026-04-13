#!/usr/bin/env python3

############################################################################
#
# MODULE:	t.rast.mapcalc
# AUTHOR(S):	Soeren Gebbert
#
# PURPOSE:	Perform spatio-temporal mapcalc expressions on temporal sampled maps of space time raster datasets
# COPYRIGHT:	(C) 2012-2017 by the GRASS Development Team
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#############################################################################

# %module
# % description: Performs spatio-temporal mapcalc expressions on temporally sampled maps of space time raster datasets.
# % keyword: temporal
# % keyword: algebra
# % keyword: raster
# % keyword: time
# %end

# %option G_OPT_STRDS_INPUTS
# %end

# %option
# % key: expression
# % type: string
# % description: Spatio-temporal mapcalc expression
# % required: yes
# % multiple: no
# %end

# %option G_OPT_T_SAMPLE
# % key: method
# % answer: equal
# %end

# %option G_OPT_STRDS_OUTPUT
# %end

# %option G_OPT_R_BASENAME_OUTPUT
# % key: basename
# % label: Basename for output raster maps
# % description: A suffix separated by an underscore will be attached to create a unique identifier
# % required: yes
# %end

# %option G_OPT_T_SUFFIX
# % key: suffix
# % description: Type of suffix to be attached the base name to create a unique identifier
# % required: yes
# % multiple: no
# % answer: num%03
# %end

# %option
# % key: offset
# % type: integer
# % description: Offset added to numeric suffix of produced maps
# % required: no
# % multiple: no
# % answer: 0
# %end

# %option
# % key: nprocs
# % type: integer
# % description: Number of r.mapcalc processes to run in parallel
# % required: no
# % multiple: no
# % answer: 1
# %end

# %flag
# % key: n
# % description: Register Null maps
# %end

# %flag
# % key: s
# % description: Check the spatial topology of temporally related maps and process only spatially related maps
# %end

import grass.script as gs


def main() -> None:
    """Run dataset_mapcalculator with options and flags."""
    # lazy imports
    import grass.temporal as tgis  # noqa: PLC0415

    # Make sure the temporal database exists
    tgis.init()

    tgis.dataset_mapcalculator(
        options["inputs"],
        options["output"],
        "raster",
        options["expression"],
        options["basename"],
        method=options["method"].split(","),
        suffix=options["suffix"],
        offset=int(options["offset"]),
        nprocs=int(options["nprocs"]),
        register_null=flags["n"],
        spatial=flags["s"],
    )


if __name__ == "__main__":
    options, flags = gs.parser()
    main()
