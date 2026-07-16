"""Shared fixtures and helpers for r.colors and r3.colors pytest tests."""

import os
import tempfile
from pathlib import Path

import pytest

import grass.script as gs
from grass.tools import Tools

TESTS_DIR = Path(__file__).parent


@pytest.fixture(scope="module")
def colors_session(tmp_path_factory):
    """Module-scoped GRASS session with raster and 3D raster maps for color tests.

    Matches the setup from the legacy test.r.colors.sh preprocess step.
    """
    project = tmp_path_factory.mktemp("r_colors") / "test_project"
    gs.create_project(project)
    with gs.setup.init(project, env=os.environ.copy()) as session:
        with Tools(session=session) as tools:
            tools.g_region(s=0, n=90, w=0, e=100, b=0, t=50, res=10, res3=10)
            tools.r_mapcalc(
                expression="test_elev_int = int(if(row() == 2, null(), row()))"
            )
            tools.r_mapcalc(
                expression="test_elev_double = double(if(row() == 2, null(), row() + 0.5))"
            )
            tools.r_mapcalc(
                expression="test_elev_float = float(if(row() == 2, null(), row() + 0.5))"
            )
            tools.r3_mapcalc(
                expression="volume_double = double(col() + row() + depth())"
            )
            tools.r3_mapcalc(
                expression="volume_double_null = if(row() == 1 || row() == 5, null(), volume_double)"
            )
        yield session


@pytest.fixture(scope="module")
def tools(colors_session):
    """Module-scoped Tools wrapper for the colors session."""
    return Tools(session=colors_session)


@pytest.fixture(scope="module")
def color_refs():
    """Dictionary mapping each reference stem to its expected color table text.

    Loads all *.ref files in the tests directory once per test session.
    Keys are the file stems (e.g. "test_elev_int_example1"), values are the
    file contents stripped of leading/trailing whitespace.
    """
    return {
        path.stem: path.read_text().strip() for path in sorted(TESTS_DIR.glob("*.ref"))
    }


def assert_colors_match(tools_obj, map_name, expected, out_flags=None, is_3d=False):
    """Export the color table of map_name and compare it against expected.

    Parameters
    ----------
    tools_obj:
        Active GRASS Tools instance.
    map_name:
        Name of the raster or 3D raster map whose color table to check.
    expected:
        Expected color table text (e.g. from the color_refs fixture).
    out_flags:
        Flags to pass to r.colors.out / r3.colors.out (e.g. "p" for percent).
    is_3d:
        Use r3.colors.out when True, r.colors.out when False.
    """
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        tmp_path = Path(f.name)
    try:
        kw = {"map": map_name, "rules": str(tmp_path), "overwrite": True}
        if out_flags:
            kw["flags"] = out_flags
        if is_3d:
            tools_obj.r3_colors_out(**kw)
        else:
            tools_obj.r_colors_out(**kw)
        actual = tmp_path.read_text(encoding="utf8").strip()
        assert actual == expected, (
            f"Color table for {map_name!r} does not match expected"
        )
    finally:
        tmp_path.unlink(missing_ok=True)
