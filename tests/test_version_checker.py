import pytest
import requests
from unittest import mock

from hapticonvrc.version_checker import VersionChecker, UPDATE_JSON_URL


class TestVersionChecker:

    @pytest.fixture
    def version_checker(self):
        return VersionChecker()

    @mock.patch('requests.get')
    def test_is_newer_version_available(self, mock_get, version_checker):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'latest': '1.2.0',
            'message': 'New version available!'
        }
        mock_get.return_value = mock_response

        assert version_checker.is_newer_version_available('1.1.0') is True
        assert version_checker.message == 'New version available!'

        mock_get.assert_called_once_with(UPDATE_JSON_URL, timeout=5)

    @mock.patch('requests.get')
    def test_is_newer_version_available_no_update(self,
                                                  mock_get,
                                                  version_checker):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'latest': '1.1.0',
            'message': 'New version available!'
        }
        mock_get.return_value = mock_response

        assert version_checker.is_newer_version_available('1.2.0') is False
        assert version_checker.message is None

        mock_get.assert_called_once_with(UPDATE_JSON_URL, timeout=5)

    @mock.patch('requests.get')
    def test_is_newer_version_available_request_exception(
            self, mock_get, version_checker):
        mock_get.side_effect = requests.RequestException()

        assert version_checker.is_newer_version_available('1.1.0') is False
        assert version_checker.message is None

        mock_get.assert_called_once_with(UPDATE_JSON_URL, timeout=5)

    def test_get_message(self, version_checker):
        version_checker.message = 'New version available!'
        assert version_checker.get_message() == 'New version available!'

    def test_is_local_version_outdated(self, version_checker):
        assert version_checker._is_local_version_outdated('1.2.0', '1.1.0') is True # noqa
        assert version_checker._is_local_version_outdated('1.1.0', '1.2.0') is False # noqa
        assert version_checker._is_local_version_outdated('1.1.0', '1.1.0') is False # noqa
