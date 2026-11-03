"""Tests of t.copy

The source dataset "src" is in PERMANENT. Every test copies it to a new
mapset which has no temporal database yet.
"""

import os
from types import SimpleNamespace

import pytest

import grass.script as gs
from grass.grassdb.create import create_mapset
from grass.tools import ToolError, Tools

MAPS = ["map_a", "map_b", "map_c"]


@pytest.fixture(scope="module")
def project(tmp_path_factory):
    """Project with the dataset "src" in PERMANENT"""
    project = tmp_path_factory.mktemp("t_copy") / "project"
    gs.create_project(project)
    with gs.setup.init(project, env=os.environ.copy()) as session:
        tools = Tools(session=session)
        tools.g_region(s=0, n=80, w=0, e=120, res=10)
        for value, name in enumerate(MAPS, start=1):
            tools.r_mapcalc(expression=f"{name} = {value}")
        tools.t_create(
            type="strds",
            temporaltype="absolute",
            output="src",
            title="Source title",
            description="Source description",
        )
        tools.t_register(
            type="raster",
            input="src",
            maps=",".join(MAPS),
            start="2001-01-01",
            increment="1 month",
            flags="i",
        )
    return project


@pytest.fixture
def work(project, request):
    """A new mapset without temporal database"""
    name = "work_" + request.node.name.replace("[", "_").replace("]", "")
    create_mapset(project / name)
    with gs.setup.init(project / name, env=os.environ.copy()) as session:
        yield SimpleNamespace(
            tools=Tools(session=session),
            mapset=name,
            database=project / name / "tgis" / "sqlite.db",
        )


def registered_ids(tools, name):
    result = tools.t_rast_list(input=name, columns="id", format="line")
    return result.text_split(",")


def datasets(work):
    """Names of the datasets of the work mapset"""
    result = work.tools.t_list(
        type="strds", columns="name", where=f"mapset = '{work.mapset}'"
    )
    return [] if result is None else result.text_split("\n")


def test_copy_registers_the_maps_of_the_input(work):
    assert not work.database.exists()
    work.tools.t_copy(input="src@PERMANENT", output="dst")
    assert work.database.exists()
    assert registered_ids(work.tools, "dst") == [f"{m}@PERMANENT" for m in MAPS]
    info = work.tools.t_info(input="dst", format="json")
    assert info["title"] == "Source title"
    assert info["description"] == "Source description"
    assert info["temporal_type"] == "absolute"


def test_copy_maps(work):
    work.tools.t_copy(input="src@PERMANENT", output="dst", flags="c")
    assert registered_ids(work.tools, "dst") == [f"{m}@{work.mapset}" for m in MAPS]
    copied = work.tools.g_list(type="raster", mapset=work.mapset).text_split("\n")
    assert copied == MAPS


def test_existing_output_requires_overwrite(work):
    work.tools.t_copy(input="src@PERMANENT", output="dst")
    with pytest.raises(ToolError):
        work.tools.t_copy(input="src@PERMANENT", output="dst")
    work.tools.t_copy(input="src@PERMANENT", output="dst", overwrite=True)
    assert registered_ids(work.tools, "dst") == [f"{m}@PERMANENT" for m in MAPS]


def test_output_in_other_mapset_fails(work):
    with pytest.raises(ToolError):
        work.tools.t_copy(input="src@PERMANENT", output="dst@PERMANENT")
    assert datasets(work) == []


def test_missing_input_fails(work):
    with pytest.raises(ToolError):
        work.tools.t_copy(input="missing", output="dst")
    assert datasets(work) == []


def test_empty_input_creates_nothing(work):
    work.tools.t_create(type="strds", output="empty", title="Empty", description="x")
    work.tools.t_copy(input="empty", output="dst")
    assert datasets(work) == ["empty"]


def test_failed_copy_leaves_no_dataset(work):
    """An existing map is detected while copying, the new dataset is removed"""
    work.tools.g_region(s=0, n=80, w=0, e=120, res=10)
    work.tools.r_mapcalc(expression="map_b = 1")
    with pytest.raises(ToolError, match="exists already"):
        work.tools.t_copy(input="src@PERMANENT", output="dst", flags="c")
    assert datasets(work) == []
