# jetcam
SkyWayとRaspberryPi(以下:ラズパイ)を利用したリモートカメラシステム。  
旅行中のペット見守りカメラとして開発。  

_コチラはVer1.0 別リポジトリにLEGOアーム制御版が存在します。_  

![frontend](doc/img/frontend.png)
![raspberrypi](doc/img/raspi.jpg)  

![diagram](doc/img/diagram.png)



## Features
- WEBアプリを通して外出先から自宅のカメラにアクセス
- WEBアプリを途中退室、ブラウザを急に閉じても再度アクセス可能
- ログイン認証付きWEBアプリで安心・安全
- メッセージ入力により、LEDを点灯、消灯操作
- メッセージ入力により、カメラがあるラズパイ側のプログラムをシャットダウン可能


## Requirement
- Webアプリ側(frontend): Nuxt.jsにて構築
- ラズパイ側(backend): Pythonにて構築


### ラズパイ
実行環境
- device:Raspberry Pi 3 Model B
- OS: Raspbian GNU/Linux 9 (stretch)
- python:3.5.3 
- camera: USBカメラ ELECOM UCAM-C0220FBBK
- Lチカ:LED、抵抗、ジャンパーコード、ブレッドボード

python3.5はすでにサポート終了しているので、上位バージョンをおすすめします。  

USBカメラに関しては、古いものや特殊なものを除いて一般的なUSBカメラであれば問題ないと思います。  

Lチカ環境はGPIOの21番ピンを使用。グラウンドとLEDの間には適切な抵抗を入れて下さい。  
[参考サイト:SkyWay WebRTC Gatewayハンズオン](https://qiita.com/nakakura/items/9d5fb1ff43c40c97c244)


### SkyWay
SkyWayを利用して、カメラ映像をストリーミングする  
  
NTTコミュニケーションズが提供する「ビデオ通話、音声通話をかんたんにアプリに実装できる、
マルチプラットフォームなSDK」  
[公式ページ](https://webrtc.ecl.ntt.com/)
  
**上記公式サイトに沿って設定し、APIKeyを取得する。(無料)**


#### WebRTC Gateway
SkyWayが提供するIOT端末用のSkyWayEngine

[公式解説](https://webrtc.ecl.ntt.com/documents/webrtc-gateway.html)

[GitHub](https://github.com/skyway/skyway-webrtc-gateway)

[API仕様書](http://35.200.46.204/)

**ラズパイで実行するため`gateway_linux_arm`をダウンロードする**  
[ダウンロード v0.3.2](https://github.com/SkyWay/SkyWay-webrtc-gateway/releases/tag/0.3.2)

### Firebase
[Firebase](https://firebase.google.com/?hl=ja)  
以下の理由によりFirebaseを利用する
- Wepアプリのデプロイ(Hosting)
- Webアプリにメールアドレスによるログイン機能の実装(Authentication)
- skyway APIKeyを格納(Firestore)


#### Hosting
Webアプリのデプロイ先となる。


#### Authentication
ログインに利用したいメールアドレスを追加する  
**`ルール`で読み書き権限を認証ユーザーのみに必ず設定すること**


#### Firestore
SkyWay APIKeyを格納する。  
`apis > SkyWay > key`こちらにstring形式で入力


## Backend
ラズパイ上で実行する  

- gateway_linux_armを任意のディレクトリに移し実行権限を付与する
- `backend`ディレクトリを移す
- gstreamerのインストール

```sh
# 映像伝送用アプリケーションのインストール
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

- 必要モジュールをラズパイにインストール
```sh
pip3 install -r requirements.txt
```

- config.pyを設定
```sh
#config.pyにリネーム
mv config_sample.py config.py

# 取得したSkyWayのAPIKEYを入力
API_KEY = "**********"
```


## Frontend
Nuxt.jsにて構築。  

- `npm run generate`にてコンパイル
- 生成された`dist`ディレクトリをfirebaseでdeployする

```bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```

## Usage
### ラズパイ側(カメラ・バックエンド)

```sh
#skywayエンジンであるweb_gatewayを起動
./gatway_linux_arm

#制御プログラムを起動
python3 wabrtc_control.py

```

### Webアプリ側(視聴側・フロントエンド)

1. Firebaseにデプロイしたサイトにアクセス
2. 設定してメールアドレス、パスワードでログイン
3. EstablishでPeer確立(skywayにつなぐ)
4. ラズパイ側のPeeIDが表示されるので選択(jetcam)
5. Callでラズパイと接続

接続が確立すると、映像が表示される

6. Messageに入力するとラズパイ側のコマンドに表示される
 - onを入力すると、LEDが点灯する
 - offを入力すると、LEDが消灯する
 - バルスを入力すると、ラズパイ側のプログラムが終了する
7. Stopでskywayから切断する


## Note

### gateway_linux_arm
[不具合と疑われる仕様あり](https://support.SkyWay.io/hc/ja/community/posts/360047020193-%E8%A7%A3%E6%94%BE%E3%81%95%E3%82%8C%E3%81%9Fvideo-id%E3%82%92%E4%BD%BF%E7%94%A8%E6%99%82%E3%81%AB%E3%82%AF%E3%83%A9%E3%83%83%E3%82%B7%E3%83%A5)

上記で案内されている`v0.3.2`を使用して、クラッシュすることは無くなったが、media connectionを完全に開放できていない疑いが残る。2回目以降新たにmedia connectionを作成しようとすると、400エラーにより作成できない。
そのため、通常flowでの処理ではない実装の検討が必要  
本コードでは、media connectionが開放されない事を前提として、通常稼働できるように実装した。

### Pythonリモートデバッグ
ラズパイでのリモートデバッグのススメ。  
GPIO使ってLチカ、gateway_linux_arm実行と環境依存があるので、ラズパイ上でのデバッグ開発が便利です。

jetbrainsでのリモートデバッグ利用法  
[jetbrains 解説](https://pleiades.io/help/idea/remote-debugging-with-product.html#remote-debug-config)

```sh
pip3 install pydevd-pycharm
```

```py
#webrtc_control.py
# jetBrainsリモートデバッグ用モジュール
import pydevd_pycharm

pydevd_pycharm.settrace('192.168.0.20', port=60000,
                         stdoutToServer=True, stderrToServer=True)

#IPアドレス,portはリモートデバッグ先の任意の値に変更

#リモートデバッグが不要であればコメントアウトする
```


## Author

- akinko
- akira.seto@gmail.com
- [Qiita](https://qiita.com/akinko)


## License

[MIT license](https://en.wikipedia.org/wiki/MIT_License).


