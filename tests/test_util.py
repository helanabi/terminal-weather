import re
import util
import pytest

class TestStoreLine:

    def test_singleton(self):
        conf = {}
        util.store_line({ "singleton": ('a')}, conf, "a=b")
        assert conf == { "a": "b" }

    def test_comulative(self):
        conf = {}
        util.store_line({"cumulative": ('a')}, conf, "a=b")
        assert conf == { "a": ["b"] }

    def test_space(self):
        conf = {}
        util.store_line({"singleton": ('a')}, conf, "a = b")
        assert conf == { "a": "b" }

    def test_accumulation(self):
        conf = {}
        spec = { "cumulative": ('a') }
        util.store_line(spec, conf, "a=b")
        util.store_line(spec, conf, "a=c")
        assert conf == { "a": ["b", "c"] }        

    def test_unspecified_var(self, capsys):
        with pytest.raises(SystemExit):
            util.store_line({}, {}, "a=b")

        assert capsys.readouterr().err == \
            "Error: unrecognized configuration variable: a\n"

    def test_overwrite(self, capsys):
        conf = { 'a': 'b' }
        with pytest.raises(SystemExit):
            util.store_line({ "singleton": ('a') }, conf, "a=c")

        assert re.match("Error: multiple values .* variable: a\n",
                         capsys.readouterr().err)

    def test_multiple_entries(self):
        conf = {}
        spec = {
            "singleton": ('a', 'b'),
            "cumulative": ('c', 'd')
        }

        sample = ["a=0", "b=1", "c=2", "d=3", "c=4", "d=5"]

        for entry in sample:
            util.store_line(spec, conf, entry)

        assert conf == {
            'a': '0',
            'b': '1',
            'c': ['2', '4'],
            'd': ['3', '5']
        }
