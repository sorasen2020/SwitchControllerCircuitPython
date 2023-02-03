# SwitchControllerCircuitPython

Raspberry Pi Picoを使ってNintendo Switchのゲームを自動化するCircuitPython用のライブラリです。

# 導入方法

必要なもの

    Raspberry Pi Pico 1台
    USB ケーブル 1本（Raspberry Pi Pico と Switch や PC を接続するのに必要）

動作環境

    CircuitPython 8.0.0-rc.2


参考URL:https://circuitpython.org/board/raspberry_pi_pico/

# 使い方

## 事前準備

Raspberry Pi PicoでCircuitPythonが使えるようにして下さい

## ライブラリのダウンロード

1. [https://circuitpython.org/libraries](https://circuitpython.org/libraries)からCircuitPythonのライブラリ(Bundle for Version 8.x)をダウンロードし展開する
2. このリポジトリをダウンロードし展開する

## 書き込み

1. Raspberry Pi PicoをPCに接続。CIRCUITPYドライブとして認識
2. CircuitPythonのライブラリの中のadafruit_hidフォルダをCIRCUITPYドライブのlibフォルダへコピーする
3. CIRCUITPYドライブにこのリポジトリのboot.py, code.py, switchcontroller.pyをコピーする

フォルダ構成
~~~
CIRCUITPY
  |-- lib
  |    |-- adafruit_hid
  |
  |-- boot.py
  |-- code.py
  |-- switchcontroller.py
~~~

3. Raspberry Pi PicoをSwitchに接続

Aボタンを連打するサンプルなので、NPCの前などで確認してください

# コード修正

必要に応じてcode.pyを修正してください

# Lisence

このプロジェクトのライセンスはMITライセンスです。詳細はLICENSEをご覧ください
