from pyjoycon import JoyCon

RUMBLE_BYTES = ['00000001', '00000000', '00{amp_code}00', '00000000'] * 2
AMP = [
	'0001',
	'0010',
	'0011',
	'0100',
	'0101',
	'0110',
	'0111',
	'1000',
	'1001',
	'1010',
	'1011',
	'1100',
]
AMP.reverse()


# thanks to https://github.com/tocoteron/joycon-python/pull/27
class RumbleJoyCon(JoyCon):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enable_vibration()

    def _enable_vibration(self) -> None:
        self._write_output_report(b'\x01', b'\x48', b'\x01')

    def send_rumble(self, amp_level: int) -> None:
        self._RUMBLE_DATA = self._get_rumble_data(amp_level)
        self._write_output_report(b'\x10', b'', b'')

    def _get_rumble_data(self, amp_level: int) -> bytes:
        data = RUMBLE_BYTES.copy()
        data[2] = data[2].format(amp_code=AMP[amp_level])
        data[6] = data[6].format(amp_code=AMP[amp_level])
        return bytes(list(map(lambda x: int(x, 2), data))) 
