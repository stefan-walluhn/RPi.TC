from rpitc import SectionBlockedError
from rpitc.section import Section
import fysom
import pytest


class TestSection:

    def test_inital_idle(self, section):
        assert not section.blocked

    def test_requires_next(self):
        with pytest.raises(TypeError):
            Section(previous=None)

    def test_requires_last(self):
        with pytest.raises(TypeError):
            Section(next=None)

    def test_arrive(self, section):
        section.arrive()
        assert section.blocked
        assert section.status == Section.ARRIVING

    def test_arrive_in_only_once(self, section):
        section.arrive()
        with pytest.raises(fysom.FysomError):
            section.arrive()

    def test_wait(self, section):
        section.arrive()
        section.wait()
        assert section.blocked
        assert section.status == Section.WAITING

    def test_depart(self, section):
        section.arrive()
        section.wait()
        section.depart()
        assert section.blocked
        assert section.status == Section.DEPARTING

    def test_resolve(self, section):
        section.resolve()
        assert not section.blocked

    def test_onleavedeparting(self, section):
        section.arrive()
        section.wait()
        section.depart()
        section.resolve()
        section.previous.depart.assert_called_with()

    def test_no_onleavedeparting_if_idle(self, section):
        section.resolve()
        section.previous.depart.assert_not_called
