import subprocess
import sys
import time

def main():
    proc = subprocess.run([
        sys.executable,
        '-m',
        'pip',
        'install',
        '-r',
        'requirements.txt',
    ])
    if proc.returncode == 0:
        print('ライブラリインストール: 成功')
    else:
        print('ライブラリインストール: 失敗')
    print('5秒後に終了します...')
    time.sleep(5)

main()
