import os, re
import pytest
from terminal_weather import config

class Args:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

@pytest.fixture
def conf_file(tmp_path):
    with open(os.path.join(tmp_path, "sample_conf"), 'w') as f:
        yield f

def test_lookup(conf_file):
    config.DEFAULTS["default"] = "default value"
    config.CONF_SPEC["testing"] = ("conf-opt",)
    config.CONF_SPEC["cumulative"] = ("conf-list","arglist")

    conf_file.write("conf-opt=conf value\n"
                    "conf-list=first\n"
                    "conf-list=second\n")
    conf_file.flush()

    args = Args(conf=conf_file.name,
                argopt="arg value",
                arglist="inside iterable")

    lookup = config.init_conf(args)

    assert lookup("argopt") == "arg value"
    assert lookup("conf-opt") == "conf value"
    assert lookup("default") == "default value"
    assert lookup("unset") == None

    conf_list =  lookup("conf-list")
    assert len(conf_list) == 2
    assert conf_list[0] == "first"
    assert conf_list[1] == "second"

    arglist = lookup("arglist")
    assert len(arglist) == 1
    assert arglist[0] == "inside iterable"

def test_cf_overrides(conf_file, tmp_path):
    os.environ.clear()
    args = Args(conf=None)

    def mock_path(base, *path):
        os.environ.update({ base: str(tmp_path) })
        filepath = tmp_path
        if len(path) > 1:
            filepath = os.path.join(filepath, *path[:-1])
            os.makedirs(filepath)
        filepath = os.path.join(filepath, path[-1])
        with open(filepath, 'w') as f:
            pass

    def compare(expected):
        config.init_conf(args)
        assert config.CONF_FILE == expected

    def test_path(base, *path):
        mock_path(base, *path)
        compare(os.path.join(tmp_path, *path))

    test_path("HOME", ".terminal-weather")
    test_path("HOME", ".config", "terminal-weather", "conf")
    test_path("XDG_CONFIG_HOME", "terminal-weather", "conf")

    os.environ.update(TERMINAL_WEATHER_CF=os.path.join(tmp_path, "env_conf"))
    test_path("HOME", "env_conf")

    setattr(args, "conf", conf_file.name),
    compare(conf_file.name)

# def test_space():
#     conf = {}
#     config.store_line({"singleton": ('a')}, conf, "a = b")
#     assert conf == { "a": "b" }

# def test_accumulation():
#     conf = {}
#     spec = { "cumulative": ('a') }
#     config.store_line(spec, conf, "a=b")
#     config.store_line(spec, conf, "a=c")
#     assert conf == { "a": ["b", "c"] }        

# def test_unspecified_var(capsys):
#     with pytest.raises(SystemExit):
#         config.store_line({}, {}, "a=b")

#     assert capsys.readouterr().err == \
#         "Error: unrecognized configuration variable: a\n"

# def test_overwrite(capsys):
#     conf = { 'a': 'b' }
#     with pytest.raises(SystemExit):
#         config.store_line({ "singleton": ('a') }, conf, "a=c")

#     assert re.match("Error: multiple values .* variable: a\n",
#                      capsys.readouterr().err)

# def test_multiple_entries():
#     conf = {}
#     spec = {
#         "singleton": ('a', 'b'),
#         "cumulative": ('c', 'd')
#     }

#     sample = ["a=0", "b=1", "c=2", "d=3", "c=4", "d=5"]

#     for entry in sample:
#         config.store_line(spec, conf, entry)

#     assert conf == {
#         'a': '0',
#         'b': '1',
#         'c': ['2', '4'],
#         'd': ['3', '5']
#     }
