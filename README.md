# Stanford NLP English Parser Server

このrepositoryはstanfordnlpをflaskでAPI化したものです。

## set up environment

Python 3.7.2 で動作を確認しています。

次をおこなってください。

```bash
pip isntall -r requirements.txt
python download_model.py
```

このrepositoryのルート直下に`stanford_resource`という名前のディレクトリが作成されその中に2.67GB程度のモデルがダウンロードされます。

## start the server

次をおこなってください。

```bash
python server.py
```

しばらくするとserverが起動します。

起動後, 

http://localhost:5020/api?document=This%20is%20a%20test%20sentence.

などによってCONLLの結果が返ります。
(Postmanなどを使うと見やすいです。)

http://localhost:5020/

にアクセスすると、parse用のページを表示します。

例

![画面](screenshot.png?raw=true)

## docker 

次を行うことでdocker image(4.0GB程度)を作成できます。

```bash
docker build -t snlp .
```

次でserverの立ち上げができます(memoryを8GBなど多めにとることを推奨します。)

```bash
docker run -it -p 5020:5020 snlp
```

もしくはdockerhubに上がっている[image](https://cloud.docker.com/u/takuyakubo/repository/docker/takuyakubo/snlp)を使うこともできます。

```bash
docker run -it -p 5020:5020 takuyakubo/snlp:english
```

## To Do

- 他言語(特に日本語)
- dockerfileなどの最適化
