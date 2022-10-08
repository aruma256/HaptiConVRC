import json
from pathlib import Path

from version_checker import VersionChecker

from pyjoycon import JoyCon, get_L_id, get_R_id
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

CONFIG_FILE = Path("config.json")
VERSION = '0.1.0'
RUMBLE_BYTES = ['00000001', '00000000', '00000100', '00000000'] * 2
RUMBLE_DATA = bytes(list(map(lambda x: int(x, 2), RUMBLE_BYTES))) 


# thanks to https://github.com/tocoteron/joycon-python/pull/27
class RumbleJoyCon(JoyCon):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_rumble(self, data=RUMBLE_DATA):
        self._enable_vibration()
        self._RUMBLE_DATA = data
        self._write_output_report(b'\x10', b'', b'')

    def _enable_vibration(self):
        self._write_output_report(b'\x01', b'\x48', b'\x01')


def _load_config() -> dict:
    with CONFIG_FILE.open(encoding='utf-8') as f:
        return json.load(f)


def main():
    print(f'HaptiConVRC-v{VERSION}')
    #
    version_checker = VersionChecker()
    if version_checker.is_newer_version_available(VERSION):
        print(version_checker.get_message())
    #
    config = _load_config()
    if config['contact_parameters']['L']:
        try:
            joycon_l = RumbleJoyCon(*get_L_id())
            print('Joy-Con L を接続しました。')
        except ValueError:
            print('エラー : Joy-Con L に接続できません')
            exit(1)
    else:
        joycon_l = None
    if config['contact_parameters']['R']:
        try:
            joycon_r = RumbleJoyCon(*get_R_id())
            print('Joy-Con R を接続しました。')
        except ValueError:
            print('エラー : Joy-Con R に接続できません')
            exit(1)
    else:
        joycon_r = None
    #
    def _on_osc(address, value):
        if address == config['contact_parameters']['L']['address']:
            if joycon_l and value:
                joycon_l.send_rumble()
        if address == config['contact_parameters']['R']['address']:
            if joycon_r and value:
                joycon_r.send_rumble()

    dispatcher = Dispatcher()
    dispatcher.set_default_handler(_on_osc)
    server = BlockingOSCUDPServer((config['OSC']['listen']['ip'], config['OSC']['listen']['port']), dispatcher)
    server.serve_forever()

main()

