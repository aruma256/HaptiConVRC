from pyjoycon import JoyCon

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
