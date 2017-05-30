import pytest
from dcc_jp2_converter.modules import profiles


@pytest.fixture
def hathi_fixture():
    return profiles.get_profile("Hathi")


def test_profile_factory(hathi_fixture):
    assert isinstance(hathi_fixture, profiles.Hathi)


def test_hathi_profile_overwrite(hathi_fixture):
    # DEFAULTS to not overwrite
    assert hathi_fixture.overwrite is False

    hathi_fixture.configure(overwrite=True)
    assert hathi_fixture.overwrite is True


def test_hathi_profile_remove_on_success(hathi_fixture):
    # DEFAULTS to not remove
    assert hathi_fixture.remove_on_success is False

    hathi_fixture.configure(remove_on_success=True)
    assert hathi_fixture.remove_on_success is True

@pytest.fixture
def default_fixtures():
    return profiles.get_profile("default")
#
def test_got_default(default_fixtures):
    assert isinstance(default_fixtures, profiles.Default)