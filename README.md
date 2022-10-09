# HaptiConVRC

VRChatでアバターの接触イベントを検知して、Joy-Conを振動させるシステム

* 開発中バージョンのため不安定です。
* [ライセンス](LICENSE)

# 必要なもの

* Joy-Con L または R
* PCVR環境(Windows10)
    * PCはBluetooth接続可能なこと
        * USBのBluetoothアダプタでも可

# 導入方法

1. Unityで、アバターの接触を検出したい部位（Armature）に `VRC Contact Receiver (Script)` を設定する。
    ![設定例](docs/unity.png)
    * Shape : Sphereで任意の検出範囲
    * Filtering
        * Allow Self と Allow Others にチェックを入れることを推奨
        * Collision Tags : Hand と Finger を推奨
    * Receiver
        * Receiver Type : 
            * 「なで」系の動作に使用する場合は `Proximity`
            * 「ツン」系の動作に使用する場合は `On Enter`
        * Parameter : わかりやすいパラメータ名を設定する。（例：左耳なら `Contact_Left_Ear` ）
1. PCにPythonをインストールする。
    * インストール時、 `Add Python3.x to PATH` にチェックを入れることを推奨
1. HaptiConVRCのzipをダウンロードし、展開する。
    * [最新版リンク](https://github.com/aruma256/HaptiConVRC/archive/refs/heads/main.zip)
1. 展開したフォルダの `setup.py` を実行する。
    * 必須ライブラリが自動インストールされる。
1. `config.json` をメモ帳などで開き、必要があれば以下の設定項目を更新して上書き保存する。
    * `address`
        * `"/avatar/parameters/（ステップ1で作成した、Joy-Conと連携させるContact Receiverのパラメータ名）` に設定する。
        * 例 : `/avatar/parameters/Contact_Left_Ear`
        * Joy-Conの片方のみ使う場合、使わないほうのパラメータ名は空欄 `""` にする
    * `amp_max`
        * 振動の強さを 0～12 の中から選ぶ。（作者推奨: 10）
    * `mode`
        * Receiver Typeに合わせる（`Proximity` または `On Enter`）
1. Joy-ConをPCに接続する。
    * Joy-ConをSwitch本体から取り外し、ペアリングボタンを長押しし、WindowsのBluetooth接続設定からペアリングをする
    * Switch本体つなげると、Joy-ConとSwitch本体が再ペアリングされる。
    * PC側にペアリング情報が残っていると、再ペアリングできない。その場合はPCでペアリング解除を行う。
1. `main.py` を実行する。



[#HaptiConVRC でツイートしてね](https://twitter.com/intent/tweet?text=%23HaptiConVRC)
