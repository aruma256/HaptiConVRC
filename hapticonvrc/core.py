import json
from pathlib import Path
import time

from pyjoycon import get_L_id, get_R_id
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

from hapticonvrc.rumble_engine.proximity_engine import ProximityEngine
from hapticonvrc.rumble_engine.onenter_engine import OnEnterEngine

from .rumble_joycon import RumbleJoyCon
from .version_checker import VersionChecker

CONFIG_FILE = Path("config.json")
VERSION = '0.2.0'


class Core:

    def __init__(self) -> None:
        self._joycon_l = None
        self._joycon_r = None
        self._engine_l = None
        self._engine_r = None

    def _print_name(self) -> None:
        print(f'HaptiConVRC-v{VERSION}')

    def _version_check(self) -> None:
        version_checker = VersionChecker()
        if version_checker.is_newer_version_available(VERSION):
            print(version_checker.get_message())

    def _load_config(self) -> None:
        with CONFIG_FILE.open(encoding='utf-8') as f:
            self._config = json.load(f)

    def _create_joycon(self, side: str) -> RumbleJoyCon:
        try:
            joycon = RumbleJoyCon(*(get_L_id() if side=='L' else get_R_id()))
            print(f'Joy-Con {side} を接続しました。')
            return joycon
        except ValueError:
            print(f'エラー : Joy-Con {side} に接続できません。3秒後に終了します...')
            time.sleep(3)
            exit(1)

    def _create_engine(self, name, joycon):
        if name == 'On Enter':
            return OnEnterEngine(joycon)
        elif name == 'Proximity':
            return ProximityEngine(joycon)
        else:
            print(f'mode "{name}" は使用できません。"On Enter"または"Proximity"を指定してください。')
            print('3秒後に終了します...')
            time.sleep(3)
            exit(1)

    def _create_engines(self) -> None:
        if self._config['contact_parameters']['L']['address']:
            joycon = self._create_joycon('L')
            joycon.set_amp_max(self._config['contact_parameters']['L']['amp_max'])
            self._engine_l = self._create_engine(self._config['contact_parameters']['L']['mode'], joycon)
        if self._config['contact_parameters']['R']['address']:
            joycon = self._create_joycon('R')
            joycon.set_amp_max(self._config['contact_parameters']['R']['amp_max'])
            self._engine_r = self._create_engine(self._config['contact_parameters']['R']['mode'], joycon)

    def start(self) -> None:
        self._print_name()
        self._version_check()
        self._load_config()
        self._create_engines()
        #
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self._on_osc)
        server = BlockingOSCUDPServer((self._config['OSC']['listen']['ip'], self._config['OSC']['listen']['port']), dispatcher)
        server.serve_forever()

    def _on_osc(self, address, value):
        if address == self._config['contact_parameters']['L']['address']:
            if self._engine_l:
                self._engine_l.update(value)
        if address == self._config['contact_parameters']['R']['address']:
            if self._engine_r:
                self._engine_r.update(value)
