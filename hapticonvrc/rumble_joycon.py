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
        self._amp_max = len(AMP)

    def set_amp_max(self, amp: int) -> None:
        if not (0 <= amp <= 12):
            print('amp_maxは0以上12以下の整数にしてください')
        amp = min(amp, 12)
        amp = max(amp, 0)
        self._amp_max = amp

    def _enable_vibration(self) -> None:
        self._write_output_report(b'\x01', b'\x48', b'\x01')

    def send_rumble(self, amp: float = 1.) -> None:
        self._RUMBLE_DATA = self._get_rumble_data(amp)
        self._write_output_report(b'\x10', b'', b'')

    def _get_rumble_data(self, amp: float) -> bytes:
        data = RUMBLE_BYTES.copy()
        amp_level = self._to_amp_level(amp)
        data[2] = data[2].format(amp_code=AMP[amp_level])
        data[6] = data[6].format(amp_code=AMP[amp_level])
        return bytes(list(map(lambda x: int(x, 2), data))) 

    def _to_amp_level(self, amp: float) -> int:
        assert 0 <= amp <= 1
        MAX = self._amp_max - 1
        return int(amp * MAX)
