import pytest

from .. import jsfnargs


@pytest.mark.parametrize("input, expected",
                         [("()", []),
                          ("('foo')", ["'foo'"]),
                          ("( 0 )", ["0"]),
                          ("( 0, 1)", ["0", "1"]),
                          ("( 'foo', \"bar\")", ["'foo'", "\"bar\""]),
                          ("( 0, 1,)", ["0", "1"]),
                          ("( 0, `foo\nbar`))", ["0", "`foo\nbar`"]),
                          ("((1), () => {})", ["(1)", "() => {}"]),
                          ("(')', '(')", ["')'", "'('"]),
                          ("('', \"\")", ["''", '""']),
                          ("('a\\'b', \"a\\\"b\")", ["'a\\'b'", '"a\\"b"']),
                          ("({1:2, 3:4}, [5,6], () => {7,8})",
                           ["{1:2, 3:4}", "[5,6]", "() => {7,8}"])])
def test_valid(input, expected):
    assert jsfnargs.get_args(input) == expected


@pytest.mark.parametrize("input",
                         ["(", "(\")", "(1,'foo)", "(1,'foo\\')"])
def test_invalid(input):
    with pytest.raises(ValueError):
        assert jsfnargs.get_args(input)
