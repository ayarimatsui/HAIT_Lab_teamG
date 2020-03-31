# HAIT_Lab_teamG
HAIT Lab Primary 東京3期 チームG 最終開発用リポジトリ

AIで栄養管理ができるwebアプリケーションをFlaskとYOLOで作りました。  
webページに料理の画像をアップロードすると、自動で何の料理が写っているのかが認識され、そのカロリーや栄養素が表示されます。

＜実行の様子＞
![実行画面](https://github.com/ayarimatsui/HAIT_Lab_teamG/blob/master/images_for_readme/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202020-03-28%2023.03.14.png)


#### ※このリポジトリをcloneしても動かないので気をつけてください。具体的な手順は以下で説明していきます。(編集中)

＜実行できるようにするために＞  

このリポジトリ中のstatic, templatesディレクトリと、judge_yolo.py, save_img.py, web.pyを自分のローカルのリポジトリに入れます。
  
YOLOを使うためにhttps://github.com/pjreddie/darknet からdarknetを自分のローカルのリポジトリにダウンロードします。  

```
$ git clone https://github.com/pjreddie/darknet.git
$ cd darknet
```
コンパイルします。

```
$ make
```

確認のために以下のコマンドを実行してみます。

```
$ ./darknet
```
結果、`usage: ./darknet <function>`というエラーが出れば、darknetはちゃんと動いています。

続いて、自作データセット(私が作成したもの)で学習したモデルを利用するための準備です。  
自身のdarknetディレクトリの中に次のファイルを入れていきます。

・darknet/data/に[names.list](https://github.com/ayarimatsui/HAIT_Lab_teamG/blob/master/web_application/darknet/data/names.list)  
・darknet/data/に[obj.names](https://github.com/ayarimatsui/HAIT_Lab_teamG/blob/master/web_application/darknet/data/obj.names)  
・darknet/cfg/に[obj.data](https://github.com/ayarimatsui/HAIT_Lab_teamG/blob/master/web_application/darknet/cfg/obj.data)  
・darknet/cfg/に[yolo-obj.data](https://github.com/ayarimatsui/HAIT_Lab_teamG/blob/master/web_application/darknet/cfg/yolo-obj.cfg)  
・darknet/backup/に学習済みモデルの重みのファイルを入れます。
