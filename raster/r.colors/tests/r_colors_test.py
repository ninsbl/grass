"""pytest tests for r.colors, ported from test.r.colors.sh."""

import pytest

from conftest import TESTS_DIR, assert_colors_match


# ---------------------------------------------------------------------------
# Smoke test (original r_colors_test.py)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("color", ["viridis", "grey", "srtm_percent"])
def test_set_color_table(session_tools, color):
    """Check that a predefined color table can be set (smoke test)."""
    session_tools.r_mapcalc(expression="raster = row() + col()")
    session_tools.r_colors(map="raster", color=color)


# ---------------------------------------------------------------------------
# Integer map
# ---------------------------------------------------------------------------


def test_int_example1(tools, color_refs):
    """Set color from rules file example1."""
    tools.r_colors(
        map="test_elev_int", rules=str(TESTS_DIR / "example1"), overwrite=True
    )
    assert_colors_match(tools, "test_elev_int", color_refs["test_elev_int_example1"])


def test_int_example1_hist(tools, color_refs):
    """Set color from example1 with histogram equalization (-e)."""
    tools.r_colors(
        map="test_elev_int",
        rules=str(TESTS_DIR / "example1"),
        flags="e",
        overwrite=True,
    )
    assert_colors_match(
        tools, "test_elev_int", color_refs["test_elev_int_example1_hist"]
    )


def test_int_example2(tools, color_refs):
    """Set color from rules file example2."""
    tools.r_colors(
        map="test_elev_int", rules=str(TESTS_DIR / "example2"), overwrite=True
    )
    assert_colors_match(tools, "test_elev_int", color_refs["test_elev_int_example2"])


def test_int_example2_log(tools, color_refs):
    """Set color from example2 with logarithmic scaling (-g)."""
    tools.r_colors(
        map="test_elev_int",
        rules=str(TESTS_DIR / "example2"),
        flags="g",
        overwrite=True,
    )
    assert_colors_match(
        tools, "test_elev_int", color_refs["test_elev_int_example2_log"]
    )


def test_int_example3(tools, color_refs):
    """Set color from rules file example3."""
    tools.r_colors(
        map="test_elev_int", rules=str(TESTS_DIR / "example3"), overwrite=True
    )
    assert_colors_match(tools, "test_elev_int", color_refs["test_elev_int_example3"])


def test_int_example3_logabs(tools, color_refs):
    """Set color from example3 with logarithmic-absolute scaling (-a)."""
    tools.r_colors(
        map="test_elev_int",
        rules=str(TESTS_DIR / "example3"),
        flags="a",
        overwrite=True,
    )
    assert_colors_match(
        tools, "test_elev_int", color_refs["test_elev_int_example3_logabs"]
    )


def test_int_example4(tools, color_refs):
    """Set color from rules file example4."""
    tools.r_colors(
        map="test_elev_int", rules=str(TESTS_DIR / "example4"), overwrite=True
    )
    assert_colors_match(tools, "test_elev_int", color_refs["test_elev_int_example4"])


def test_int_example4_inv(tools, color_refs):
    """Copy color table from the same map and invert it (-n)."""
    tools.r_colors(
        map="test_elev_int", rules=str(TESTS_DIR / "example4"), overwrite=True
    )
    tools.r_colors(
        map="test_elev_int", raster="test_elev_int", flags="n", overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_int", color_refs["test_elev_int_example4_inv"]
    )


# Integer map — percentage export via r.colors.out -p


def test_int_example1_perc(tools, color_refs):
    """Export color table of example1 as percentage ranges."""
    tools.r_colors(
        map="test_elev_int", rules=str(TESTS_DIR / "example1"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_int", color_refs["test_elev_int_example1_perc"], out_flags="p"
    )


def test_int_example2_perc(tools, color_refs):
    """Export color table of example2 as percentage ranges."""
    tools.r_colors(
        map="test_elev_int", rules=str(TESTS_DIR / "example2"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_int", color_refs["test_elev_int_example2_perc"], out_flags="p"
    )


def test_int_example3_perc(tools, color_refs):
    """Export color table of example3 as percentage ranges."""
    tools.r_colors(
        map="test_elev_int", rules=str(TESTS_DIR / "example3"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_int", color_refs["test_elev_int_example3_perc"], out_flags="p"
    )


def test_int_example4_perc(tools, color_refs):
    """Export color table of example4 as percentage ranges."""
    tools.r_colors(
        map="test_elev_int", rules=str(TESTS_DIR / "example4"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_int", color_refs["test_elev_int_example4_perc"], out_flags="p"
    )


# ---------------------------------------------------------------------------
# Float map
# ---------------------------------------------------------------------------


def test_float_example1(tools, color_refs):
    """Set color from rules file example1 on a float map."""
    tools.r_colors(
        map="test_elev_float", rules=str(TESTS_DIR / "example1"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_float", color_refs["test_elev_float_example1"]
    )


def test_float_example1_hist(tools, color_refs):
    """Set color from example1 with histogram equalization on a float map."""
    tools.r_colors(
        map="test_elev_float",
        rules=str(TESTS_DIR / "example1"),
        flags="e",
        overwrite=True,
    )
    assert_colors_match(
        tools, "test_elev_float", color_refs["test_elev_float_example1_hist"]
    )


def test_float_example2(tools, color_refs):
    """Set color from rules file example2 on a float map."""
    tools.r_colors(
        map="test_elev_float", rules=str(TESTS_DIR / "example2"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_float", color_refs["test_elev_float_example2"]
    )


def test_float_example2_log(tools, color_refs):
    """Set color from example2 with logarithmic scaling on a float map."""
    tools.r_colors(
        map="test_elev_float",
        rules=str(TESTS_DIR / "example2"),
        flags="g",
        overwrite=True,
    )
    assert_colors_match(
        tools, "test_elev_float", color_refs["test_elev_float_example2_log"]
    )


def test_float_example3(tools, color_refs):
    """Set color from rules file example3 on a float map."""
    tools.r_colors(
        map="test_elev_float", rules=str(TESTS_DIR / "example3"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_float", color_refs["test_elev_float_example3"]
    )


def test_float_example3_logabs(tools, color_refs):
    """Set color from example3 with logarithmic-absolute scaling on a float map."""
    tools.r_colors(
        map="test_elev_float",
        rules=str(TESTS_DIR / "example3"),
        flags="a",
        overwrite=True,
    )
    assert_colors_match(
        tools, "test_elev_float", color_refs["test_elev_float_example3_logabs"]
    )


def test_float_example4(tools, color_refs):
    """Set color from rules file example4 on a float map."""
    tools.r_colors(
        map="test_elev_float", rules=str(TESTS_DIR / "example4"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_float", color_refs["test_elev_float_example4"]
    )


def test_float_example4_inv(tools, color_refs):
    """Copy color table from the same float map and invert it."""
    tools.r_colors(
        map="test_elev_float", rules=str(TESTS_DIR / "example4"), overwrite=True
    )
    tools.r_colors(
        map="test_elev_float", raster="test_elev_float", flags="n", overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_float", color_refs["test_elev_float_example4_inv"]
    )


# ---------------------------------------------------------------------------
# Double map
# ---------------------------------------------------------------------------


def test_double_example1(tools, color_refs):
    """Set color from rules file example1 on a double map."""
    tools.r_colors(
        map="test_elev_double", rules=str(TESTS_DIR / "example1"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_double", color_refs["test_elev_double_example1"]
    )


def test_double_example1_hist(tools, color_refs):
    """Set color from example1 with histogram equalization on a double map."""
    tools.r_colors(
        map="test_elev_double",
        rules=str(TESTS_DIR / "example1"),
        flags="e",
        overwrite=True,
    )
    assert_colors_match(
        tools, "test_elev_double", color_refs["test_elev_double_example1_hist"]
    )


def test_double_example2(tools, color_refs):
    """Set color from rules file example2 on a double map."""
    tools.r_colors(
        map="test_elev_double", rules=str(TESTS_DIR / "example2"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_double", color_refs["test_elev_double_example2"]
    )


def test_double_example2_log(tools, color_refs):
    """Set color from example2 with logarithmic scaling on a double map."""
    tools.r_colors(
        map="test_elev_double",
        rules=str(TESTS_DIR / "example2"),
        flags="g",
        overwrite=True,
    )
    assert_colors_match(
        tools, "test_elev_double", color_refs["test_elev_double_example2_log"]
    )


def test_double_example3(tools, color_refs):
    """Set color from rules file example3 on a double map."""
    tools.r_colors(
        map="test_elev_double", rules=str(TESTS_DIR / "example3"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_double", color_refs["test_elev_double_example3"]
    )


def test_double_example3_logabs(tools, color_refs):
    """Set color from example3 with logarithmic-absolute scaling on a double map."""
    tools.r_colors(
        map="test_elev_double",
        rules=str(TESTS_DIR / "example3"),
        flags="a",
        overwrite=True,
    )
    assert_colors_match(
        tools, "test_elev_double", color_refs["test_elev_double_example3_logabs"]
    )


def test_double_example4(tools, color_refs):
    """Set color from rules file example4 on a double map."""
    tools.r_colors(
        map="test_elev_double", rules=str(TESTS_DIR / "example4"), overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_double", color_refs["test_elev_double_example4"]
    )


def test_double_example4_inv(tools, color_refs):
    """Copy color table from the same double map and invert it."""
    tools.r_colors(
        map="test_elev_double", rules=str(TESTS_DIR / "example4"), overwrite=True
    )
    tools.r_colors(
        map="test_elev_double", raster="test_elev_double", flags="n", overwrite=True
    )
    assert_colors_match(
        tools, "test_elev_double", color_refs["test_elev_double_example4_inv"]
    )


# ---------------------------------------------------------------------------
# -w flag: write only when no color table exists
# ---------------------------------------------------------------------------


def test_write_only_if_no_color_table(tools, color_refs):
    """-w writes only to maps without a color table, skipping maps that have one.

    This also exercises the mixed cell-type case (integer vs. double): with
    -w the skipped map must be excluded from the range computation, otherwise
    GRASS would fatal-error due to mixing integer and floating-point maps.
    """
    # Give test_elev_int (integer) a known color table.
    tools.r_colors(
        map="test_elev_int", rules=str(TESTS_DIR / "example1"), overwrite=True
    )
    # Strip any color table from test_elev_double (floating-point).
    tools.r_colors(map="test_elev_double", flags="r")
    # -w must write to test_elev_double (no color) and skip test_elev_int (has one).
    tools.r_colors(
        map="test_elev_int,test_elev_double",
        rules=str(TESTS_DIR / "example1"),
        flags="w",
    )
    # test_elev_int was skipped: color table is unchanged.
    assert_colors_match(tools, "test_elev_int", color_refs["test_elev_int_example1"])
    # test_elev_double received the new color table.
    assert_colors_match(
        tools, "test_elev_double", color_refs["test_elev_double_example1"]
    )


# ---------------------------------------------------------------------------
# Remove color table
# ---------------------------------------------------------------------------


def test_double_remove(tools, color_refs):
    """Removing the color table with -r results in the GRASS-generated default."""
    tools.r_colors(map="test_elev_double", flags="r")
    assert_colors_match(
        tools, "test_elev_double", color_refs["test_elev_double_default"]
    )
