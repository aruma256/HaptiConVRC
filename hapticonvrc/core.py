import json
from pathlib import Path
import time

from pyjoycon import get_L_id, get_R_id
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

from .rumble_joycon import RumbleJoyCon
from .version_checker import VersionChecker

CONFIG_FILE = Path("config.json")
VERSION = '0.1.0'


class Core:

    def __init__(self) -> None:
        self._joycon_l = None
        self._joycon_r = None

    def _print_name(self) -> None:
        print(f'HaptiConVRC-v{VERSION}')

    def _version_check(self) -> None:
        version_checker = VersionChecker()
        if version_checker.is_newer_version_available(VERSION):
            print(version_checker.get_message())

    def _load_config(self) -> None:
        with CONFIG_FILE.open(encoding='utf-8') as f:
            self._config = json.load(f)

    def _setup_joycon_l(self) -> None:
        try:
            self._joycon_l = RumbleJoyCon(*get_L_id())
            print('Joy-Con L を接続しました。')
        except ValueError:
            print('エラー : Joy-Con L に接続できません。3秒後に終了します...')
            time.sleep(3)
            exit(1)

    def _setup_joycon_r(self) -> None:
        try:
            self._joycon_r = RumbleJoyCon(*get_R_id())
            print('Joy-Con R を接続しました。')
        except ValueError:
            print('エラー : Joy-Con R に接続できません。3秒後に終了します...')
            time.sleep(3)
            exit(1)

    def _setup_joycons(self) -> None:
        if self._config['contact_parameters']['L']:
            self._setup_joycon_l()
        if self._config['contact_parameters']['R']:
            self._setup_joycon_r()

    def start(self) -> None:
        self._print_name()
        self._version_check()
        self._load_config()
        self._setup_joycons()
        #
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self._on_osc)
        server = BlockingOSCUDPServer((self._config['OSC']['listen']['ip'], self._config['OSC']['listen']['port']), dispatcher)
        server.serve_forever()

    def _on_osc(self, address, value):
        if address == self._config['contact_parameters']['L']['address']:
            if self._joycon_l and value:
                self._joycon_l.send_rumble()
        if address == self._config['contact_parameters']['R']['address']:
            if self._joycon_r and value:
                self._joycon_r.send_rumble()
