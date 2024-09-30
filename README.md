# PaperPeek

## 使用技術

<p style="display: inline">
    <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
    <img src="https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=for-the-badge">
</p>


## 目次

1. [プロジェクトの概要](#プロジェクトの概要)
2. [環境](#環境)
3. [ディレクトリ構成](#ディレクトリ構成)
4. [開発環境構築](#開発環境構築)


## プロジェクト概要

最新の論文を手軽にチェックするためのツール開発．


## 環境

| 言語・ツール | バージョン |
| ------------ | ---------- |
| Python | 3.12.4 |
| uv | 0.4.17 |


## ディレクトリ構成

```
.
|-- .python-version
|-- Dockerfile
|-- Makefile
|-- README.md
|-- entrypoint.sh
|-- pyproject.toml
|-- src
`-- uv.lock
```


## 開発環境構築

- イメージのビルド

```
make build
```

- コンテナの起動

```
make run
```

- linterの実行

```
make check
```

- formatterの実行 (diffの表示)

```
make format
```

- isortの実行 (diffの表示)

```
make isort
```

- コンテナ内でのPythonスクリプトの実行

```
uv run python src/hoge.py
```
