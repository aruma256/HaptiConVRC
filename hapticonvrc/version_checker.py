import requests


class VersionChecker:
    UPDATE_JSON_URL = 'https://github.com/aruma256/HaptiConVRC/raw/main/version_info.json'  # noqa

    @staticmethod
    def _get_latest_version_info() -> dict:
        try:
            res = requests.get(VersionChecker.UPDATE_JSON_URL, timeout=5)
            if res.status_code == 200:
                data = res.json()
                return data
        except requests.RequestException:
            pass
        return {}

    @staticmethod
    def _is_local_version_outdated(latest_version: str,
                                   local_version: str) -> bool:
        remote = tuple(map(int, latest_version.split('.')))
        local = tuple(map(int, local_version.split('.')))
        return remote > local

    @staticmethod
    def is_newer_version_available(local_version: str) -> tuple[bool, str]:
        latest_version_info = VersionChecker._get_latest_version_info()
        latest_version = latest_version_info.get('latest', '0.0.0')
        message = latest_version_info.get('message', '新しいバージョンがリリースされています')
        if VersionChecker._is_local_version_outdated(latest_version,
                                                     local_version):
            return (True, message)
        else:
            return (False, '')
