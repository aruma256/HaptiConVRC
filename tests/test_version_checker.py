from unittest import mock

import requests
import pytest

from hapticonvrc.version_checker import VersionChecker


@mock.patch('requests.get')
@pytest.mark.parametrize(
    "local_version, expected_result",
    [
        ("0.9.9", (True, "New version available")),
        ("1.1.9", (True, "New version available")),
        ("1.2.2", (True, "New version available")),
        ("1.2.3", (False, "")),
        ("1.2.22", (False, "")),
        ("2.0.0", (False, "")),
    ]
)
def test_is_newer_version_available(mock_get, local_version, expected_result):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "latest": "1.2.3",
        "message": "New version available"
    }

    result = VersionChecker.is_newer_version_available(local_version)

    assert result == expected_result
    mock_get.assert_called_once_with(VersionChecker.UPDATE_JSON_URL, timeout=5)


# requests.get が例外を発生させる場合のテスト
@mock.patch('requests.get')
def test_is_newer_version_available_request_exception(mock_get):
    mock_get.side_effect = requests.RequestException

    local_version = "1.2.3"
    result = VersionChecker.is_newer_version_available(local_version)

    assert result == (False, '')
    mock_get.assert_called_once_with(VersionChecker.UPDATE_JSON_URL, timeout=5)


# レスポンスがステータスコード 200 以外の場合のテスト
@mock.patch('requests.get')
def test_is_newer_version_available_invalid_status_code(mock_get):
    mock_get.return_value.status_code = 404

    local_version = "1.0.0"
    result = VersionChecker.is_newer_version_available(local_version)

    assert result == (False, '')
    mock_get.assert_called_once_with(VersionChecker.UPDATE_JSON_URL, timeout=5)
