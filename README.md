# jetcam

## Features


## Requirement

### gateway_linux_arm

[不具合と疑われる仕様あり](https://support.skyway.io/hc/ja/community/posts/360047020193-%E8%A7%A3%E6%94%BE%E3%81%95%E3%82%8C%E3%81%9Fvideo-id%E3%82%92%E4%BD%BF%E7%94%A8%E6%99%82%E3%81%AB%E3%82%AF%E3%83%A9%E3%83%83%E3%82%B7%E3%83%A5)  

[ダウンロード v0.3.2](https://github.com/skyway/skyway-webrtc-gateway/releases/tag/0.3.2)  

クラッシュすることは無くなったが、上記v0.3.2を使用してもmedia connectionを完全に開放できていない仕様の疑いがある。2回目新たにmedia connectionを作成しようとすると、400エラーにより作成できない。  
そのため、通常flowでの処理ではない実装の検討が必要


### Backend

```bash
# 映像伝送用アプリケーションのインストール
$ sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

# サンプルプログラムはRubyで書くのでRubyの開発環境をインストール
$ sudo apt install ruby-dev libssl-dev

# Raspberry PiのピンをRubyで使うためのgemをインストール
$ sudo gem install pi_piper
```


## Installation

### Frontend
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


## Note

初期参考コード  
[SkyWay WebRTC Gatewayハンズオン](https://qiita.com/nakakura/items/faeb4f6df82677139761)  
[skyway-lab/skyway-webrtc-gw-handson](https://github.com/skyway-lab/skyway-webrtc-gw-handson)

## Author

- akinko
- akira.seto@gmail.com
- [Qiita](https://qiita.com/akinko)


## License

[MIT license](https://en.wikipedia.org/wiki/MIT_License).


