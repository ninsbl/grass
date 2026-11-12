"""Tests for i.group: creating, editing, and listing (sub)groups and their maps"""

import os

import pytest

import grass.script as gs
from grass.exceptions import CalledModuleError
from grass.tools import Tools


@pytest.fixture(scope="module")
def i_group_session(tmp_path_factory):
    """Session with raster1/raster2/raster3, plus a group in another mapset.

    raster1/raster2/raster3 live in the current (PERMANENT) mapset, like
    the groups the general i.group tests below create from them. A
    separate raster and group ("other_group", with subgroup "sub1") live
    in "other_mapset", which is added to the search path before leaving
    the session in PERMANENT; these back the cross-mapset tests. The two
    are kept apart because i.group's raster removal matching (-r flag)
    does not resolve unqualified raster names across the search path
    either, so a group mixing rasters from both mapsets could not have
    its search-path-visible rasters removed by their unqualified name.
    """
    tmp_path = tmp_path_factory.mktemp("i_group_test")
    project = tmp_path / "test_project"
    gs.create_project(project)
    with (
        gs.setup.init(project, env=os.environ.copy()) as session,
        Tools(session=session) as tools,
    ):
        tools.g_region(n=10, s=0, e=10, w=0, rows=10, cols=10)
        tools.r_mapcalc(expression="raster1 = row()")
        tools.r_mapcalc(expression="raster2 = col()")
        tools.r_mapcalc(expression="raster3 = row() + col()")

        tools.g_mapset(flags="c", mapset="other_mapset")
        tools.g_region(n=10, s=0, e=10, w=0, rows=10, cols=10)
        tools.r_mapcalc(expression="other_raster = 1")
        tools.i_group(group="other_group", input="other_raster")
        tools.i_group(group="other_group", subgroup="sub1", input="other_raster")

        tools.g_mapset(mapset="PERMANENT")
        tools.g_mapsets(mapset="other_mapset", operation="add")
        yield session


def test_group_creation(i_group_session):
    """A raster group can be created and is correctly listed (-l flag)"""
    tools = Tools(session=i_group_session)
    group = "creation_group"
    tools.i_group(group=group, input="raster1,raster2,raster3")
    groups = tools.i_group(group=group, flags="l").text
    assert group in groups


def test_add_remove_maps(i_group_session):
    """Rasters can be added to and removed from a group (-r and -g flags)"""
    tools = Tools(session=i_group_session)
    group = "add_remove_group"
    tools.i_group(group=group, input="raster1,raster2")
    tools.i_group(group=group, input="raster3")

    groups = tools.i_group(group=group, flags="g").text
    assert "raster1" in groups
    assert "raster2" in groups
    assert "raster3" in groups

    groups_shell = tools.i_group(group=group, format="shell").text
    assert groups_shell == groups

    tools.i_group(group=group, input="raster2", flags="r")
    groups = tools.i_group(group=group, flags="g").text
    assert "raster2" not in groups

    groups_shell = tools.i_group(group=group, format="shell").text
    assert groups_shell == groups


def test_subgroup_handling(i_group_session):
    """Subgroups can be created and their members listed (-s flag)"""
    tools = Tools(session=i_group_session)
    group = "subgroup_handling_group"
    tools.i_group(group=group, subgroup="sub1", input="raster1,raster2")
    tools.i_group(group=group, subgroup="sub2", input="raster3")

    subgroup1 = tools.i_group(group=group, subgroup="sub1", flags="s").text
    subgroup2 = tools.i_group(group=group, subgroup="sub2", flags="s").text

    assert "raster1" in subgroup1
    assert "raster2" in subgroup1
    assert "raster3" not in subgroup1
    assert "raster1" not in subgroup2
    assert "raster2" not in subgroup2
    assert "raster3" in subgroup2


def test_list_files_shell(i_group_session):
    """(Sub)group files are listed correctly in shell format"""
    tools = Tools(session=i_group_session)
    group = "list_files_shell_group"
    tools.i_group(group=group, subgroup="sub1", input="raster1,raster2")
    tools.i_group(group=group, subgroup="sub2", input="raster3")

    subgroup = tools.i_group(
        group=group, subgroup="sub1", flags="l", format="shell"
    ).text
    assert "raster1" in subgroup
    assert "raster2" in subgroup
    assert "raster3" not in subgroup

    subgroup = tools.i_group(
        group=group, subgroup="sub2", flags="l", format="shell"
    ).text
    assert "raster1" not in subgroup
    assert "raster2" not in subgroup
    assert "raster3" in subgroup

    group_listing = tools.i_group(group=group, flags="l", format="shell").text
    assert "raster1" in group_listing
    assert "raster2" in group_listing
    assert "raster3" in group_listing


def test_list_files_json(i_group_session):
    """(Sub)group files are listed correctly in JSON format"""
    tools = Tools(session=i_group_session)
    group = "list_files_json_group"
    tools.i_group(group=group, subgroup="sub1", input="raster1,raster2")
    tools.i_group(group=group, subgroup="sub2", input="raster3")

    maps = tools.i_group(group=group, subgroup="sub1", flags="l", format="json").json
    assert any("raster1" in m for m in maps)
    assert any("raster2" in m for m in maps)
    assert all("raster3" not in m for m in maps)

    maps = tools.i_group(group=group, subgroup="sub2", flags="l", format="json").json
    assert all("raster1" not in m for m in maps)
    assert all("raster2" not in m for m in maps)
    assert any("raster3" in m for m in maps)

    maps = tools.i_group(group=group, flags="l", format="json").json
    assert any("raster1" in m for m in maps)
    assert any("raster2" in m for m in maps)
    assert any("raster3" in m for m in maps)


def test_list_subgroups_shell(i_group_session):
    """Subgroups of a group are listed correctly in shell format"""
    tools = Tools(session=i_group_session)
    group = "list_subgroups_shell_group"
    tools.i_group(group=group, subgroup="sub1", input="raster1,raster2")
    tools.i_group(group=group, subgroup="sub2", input="raster3")

    subgroups = tools.i_group(group=group, flags="s", format="shell").text
    assert "sub1" in subgroups
    assert "sub2" in subgroups


def test_list_subgroups_json(i_group_session):
    """Subgroups of a group are listed correctly, and in creation order, in JSON format"""
    tools = Tools(session=i_group_session)
    group = "list_subgroups_json_group"
    tools.i_group(group=group, subgroup="sub1", input="raster1,raster2")
    tools.i_group(group=group, subgroup="sub2", input="raster3")

    subgroups = tools.i_group(group=group, flags="s", format="json").json
    assert subgroups == ["sub1", "sub2"]


def test_unqualified_group_listing_uses_search_path(i_group_session):
    """An unqualified group name is found via the mapset search path, not just the current mapset"""
    tools = Tools(session=i_group_session)
    result = tools.i_group(group="other_group", format="json").json
    assert result == ["other_raster@other_mapset"]


def test_unqualified_subgroup_listing_uses_search_path(i_group_session):
    """An unqualified subgroup lookup also follows the mapset search path"""
    tools = Tools(session=i_group_session)
    result = tools.i_group(group="other_group", subgroup="sub1", format="json").json
    assert result == ["other_raster@other_mapset"]


def test_qualified_name_still_works(i_group_session):
    """Explicitly qualifying the group with @mapset keeps working as before"""
    tools = Tools(session=i_group_session)
    result = tools.i_group(group="other_group@other_mapset", format="json").json
    assert result == ["other_raster@other_mapset"]


def test_group_not_found_anywhere_still_fails(i_group_session):
    """A group that does not exist in any accessible mapset still raises an error"""
    tools = Tools(session=i_group_session)
    with pytest.raises(CalledModuleError):
        tools.i_group(group="no_such_group", format="json")


@pytest.fixture(scope="module")
def labeled_group(i_group_session):
    """Group with two maps with semantic labels and one without"""
    tools = Tools(session=i_group_session)
    group = "labeled_group"
    tools.r_mapcalc(expression="label_a = 1")
    tools.r_mapcalc(expression="label_b = 2")
    tools.r_mapcalc(expression="label_c = 3")
    tools.r_support(map="label_a", semantic_label="L8_1")
    tools.r_support(map="label_c", semantic_label="L8_3")
    tools.i_group(group=group, input="label_a,label_b,label_c")
    return tools, group


def test_json_structure_list(labeled_group):
    """The default structure is a flat list of map names"""
    tools, group = labeled_group
    expected = ["label_a@PERMANENT", "label_b@PERMANENT", "label_c@PERMANENT"]
    assert tools.i_group(group=group, format="json").json == expected
    assert tools.i_group(group=group, format="json", structure="list").json == expected


def test_json_structure_semantic_label_mapname(labeled_group):
    """Semantic labels are keys; a map without label is keyed by its index"""
    tools, group = labeled_group
    result = tools.i_group(
        group=group, format="json", structure="semantic_label-mapname"
    ).json
    assert result == {
        "L8_1": "label_a@PERMANENT",
        "2": "label_b@PERMANENT",
        "L8_3": "label_c@PERMANENT",
    }


def test_json_structure_index_mapname(labeled_group):
    """Indices are keys"""
    tools, group = labeled_group
    result = tools.i_group(group=group, format="json", structure="index-mapname").json
    assert result == {
        "1": "label_a@PERMANENT",
        "2": "label_b@PERMANENT",
        "3": "label_c@PERMANENT",
    }


def test_json_structure_mapname_semantic_label(labeled_group):
    """Map names are keys; a missing semantic label is null"""
    tools, group = labeled_group
    result = tools.i_group(
        group=group, format="json", structure="mapname-semantic_label"
    ).json
    assert result == {
        "label_a@PERMANENT": "L8_1",
        "label_b@PERMANENT": None,
        "label_c@PERMANENT": "L8_3",
    }


def test_json_structure_mapname_index(labeled_group):
    """Map names are keys and their indices are the values"""
    tools, group = labeled_group
    result = tools.i_group(group=group, format="json", structure="mapname-index").json
    assert result == {
        "label_a@PERMANENT": "1",
        "label_b@PERMANENT": "2",
        "label_c@PERMANENT": "3",
    }


def test_json_structure_subgroup(labeled_group):
    """Indices refer to the position in the subgroup"""
    tools, group = labeled_group
    tools.i_group(group=group, subgroup="sub", input="label_b,label_c")
    result = tools.i_group(
        group=group,
        subgroup="sub",
        format="json",
        structure="semantic_label-mapname",
    ).json
    assert result == {"1": "label_b@PERMANENT", "L8_3": "label_c@PERMANENT"}


def test_json_structure_invalid_combinations(labeled_group):
    """Structures other than list require format=json and no -s flag"""
    tools, group = labeled_group
    with pytest.raises(CalledModuleError):
        tools.i_group(group=group, format="shell", structure="index-mapname")
    with pytest.raises(CalledModuleError):
        tools.i_group(group=group, format="json", structure="index-mapname", flags="s")
