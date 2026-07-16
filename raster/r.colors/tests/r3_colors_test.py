"""pytest tests for r3.colors, ported from test.r.colors.sh."""

from conftest import TESTS_DIR, assert_colors_match

MAP = "volume_double_null"


def test_volume_example1(tools, color_refs):
    """Set color from rules file example1 on a 3D raster."""
    tools.r3_colors(map=MAP, rules=str(TESTS_DIR / "example1"), overwrite=True)
    assert_colors_match(
        tools, MAP, color_refs["test_volume_double_example1"], is_3d=True
    )


def test_volume_example1_hist(tools, color_refs):
    """Set color from example1 with histogram equalization on a 3D raster."""
    tools.r3_colors(
        map=MAP, rules=str(TESTS_DIR / "example1"), flags="e", overwrite=True
    )
    assert_colors_match(
        tools, MAP, color_refs["test_volume_double_example1_hist"], is_3d=True
    )


def test_volume_example2(tools, color_refs):
    """Set color from rules file example2 on a 3D raster."""
    tools.r3_colors(map=MAP, rules=str(TESTS_DIR / "example2"), overwrite=True)
    assert_colors_match(
        tools, MAP, color_refs["test_volume_double_example2"], is_3d=True
    )


def test_volume_example2_log(tools, color_refs):
    """Set color from example2 with logarithmic scaling on a 3D raster."""
    tools.r3_colors(
        map=MAP, rules=str(TESTS_DIR / "example2"), flags="g", overwrite=True
    )
    assert_colors_match(
        tools, MAP, color_refs["test_volume_double_example2_log"], is_3d=True
    )


def test_volume_example3(tools, color_refs):
    """Set color from rules file example3 on a 3D raster."""
    tools.r3_colors(map=MAP, rules=str(TESTS_DIR / "example3"), overwrite=True)
    assert_colors_match(
        tools, MAP, color_refs["test_volume_double_example3"], is_3d=True
    )


def test_volume_example3_logabs(tools, color_refs):
    """Set color from example3 with logarithmic-absolute scaling on a 3D raster."""
    tools.r3_colors(
        map=MAP, rules=str(TESTS_DIR / "example3"), flags="a", overwrite=True
    )
    assert_colors_match(
        tools, MAP, color_refs["test_volume_double_example3_logabs"], is_3d=True
    )


def test_volume_example4(tools, color_refs):
    """Set color from rules file example4 on a 3D raster."""
    tools.r3_colors(map=MAP, rules=str(TESTS_DIR / "example4"), overwrite=True)
    assert_colors_match(
        tools, MAP, color_refs["test_volume_double_example4"], is_3d=True
    )


def test_volume_example4_inv(tools, color_refs):
    """Copy the color table from the same 3D raster and invert it.

    The shell test used 'volume=' which is not a valid parameter (correct name
    is raster_3d=). The reference file may therefore need regeneration.
    """
    tools.r3_colors(map=MAP, rules=str(TESTS_DIR / "example4"), overwrite=True)
    tools.r3_colors(map=MAP, raster_3d=MAP, flags="n", overwrite=True)
    assert_colors_match(
        tools, MAP, color_refs["test_volume_double_example4_inv"], is_3d=True
    )


def test_volume_copy_from_raster(tools, color_refs):
    """Copy the color table from a 2D raster map to a 3D raster."""
    tools.r_colors(
        map="test_elev_double", rules=str(TESTS_DIR / "example4"), overwrite=True
    )
    tools.r3_colors(map=MAP, raster="test_elev_double", overwrite=True)
    assert_colors_match(
        tools, MAP, color_refs["test_volume_double_example5"], is_3d=True
    )


def test_volume_remove(tools, color_refs):
    """Removing the color table with -r results in the GRASS-generated default."""
    tools.r3_colors(map=MAP, flags="r")
    assert_colors_match(
        tools, MAP, color_refs["test_volume_double_default"], is_3d=True
    )
