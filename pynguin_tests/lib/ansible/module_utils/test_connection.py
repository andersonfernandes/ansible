# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import connection as module_0
import platform as module_1
import re as module_2


@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = False
    module_0.recv_data(bool_0)


def test_case_1():
    str_0 = "Soft Errors"
    connection_0 = module_0.Connection(str_0)
    assert (
        f"{type(connection_0).__module__}.{type(connection_0).__qualname__}"
        == "connection.Connection"
    )
    assert connection_0.socket_path == "Soft Errors"
    with pytest.raises(module_0.ConnectionError):
        connection_0.send(str_0)


def test_case_2():
    list_0 = []
    connection_error_0 = module_0.ConnectionError(list_0)
    assert (
        f"{type(connection_error_0).__module__}.{type(connection_error_0).__qualname__}"
        == "connection.ConnectionError"
    )


def test_case_3():
    none_type_0 = None
    with pytest.raises(AssertionError):
        module_0.Connection(none_type_0)


def test_case_4():
    none_type_0 = None
    var_0 = module_0.request_builder(none_type_0)


@pytest.mark.xfail(strict=True)
def test_case_5():
    bytes_0 = b""
    module_0.write_to_file_descriptor(bytes_0, bytes_0)


@pytest.mark.xfail(strict=True)
def test_case_6():
    none_type_0 = None
    module_0.send_data(none_type_0, none_type_0)


def test_case_7():
    var_0 = module_1.uname()
    connection_0 = module_0.Connection(var_0)
    assert (
        f"{type(connection_0).__module__}.{type(connection_0).__qualname__}"
        == "connection.Connection"
    )
    assert (
        f"{type(connection_0.socket_path).__module__}.{type(connection_0.socket_path).__qualname__}"
        == "platform.uname_result"
    )
    assert len(connection_0.socket_path) == 6


@pytest.mark.xfail(strict=True)
def test_case_8():
    bool_0 = True
    connection_0 = module_0.Connection(bool_0)
    assert (
        f"{type(connection_0).__module__}.{type(connection_0).__qualname__}"
        == "connection.Connection"
    )
    assert connection_0.socket_path is True
    connection_0.removeprefix(bool_0)


@pytest.mark.xfail(strict=True)
def test_case_9():
    regex_flag_0 = module_2.RegexFlag.TEMPLATE
    connection_0 = module_0.Connection(regex_flag_0)
    assert (
        f"{type(connection_0).__module__}.{type(connection_0).__qualname__}"
        == "connection.Connection"
    )
    assert connection_0.socket_path == module_2.RegexFlag.TEMPLATE
    connection_0.removeprefix(connection_0)


@pytest.mark.xfail(strict=True)
def test_case_10():
    regex_flag_0 = module_2.RegexFlag.TEMPLATE
    connection_0 = module_0.Connection(regex_flag_0)
    assert (
        f"{type(connection_0).__module__}.{type(connection_0).__qualname__}"
        == "connection.Connection"
    )
    assert connection_0.socket_path == module_2.RegexFlag.TEMPLATE
    connection_0.removeprefix(connection_0)


@pytest.mark.xfail(strict=True)
def test_case_11():
    regex_flag_0 = module_2.RegexFlag.DOTALL
    connection_0 = module_0.Connection(regex_flag_0)
    assert (
        f"{type(connection_0).__module__}.{type(connection_0).__qualname__}"
        == "connection.Connection"
    )
    assert connection_0.socket_path == module_2.RegexFlag.DOTALL
    str_0 = "d8FotN<My\x0b"
    dict_0 = {str_0: connection_0, str_0: regex_flag_0}
    var_0 = module_0.request_builder(regex_flag_0, **dict_0)
    connection_0.__getattr__(var_0)
