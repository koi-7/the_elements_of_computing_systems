# 10章 コンパイラ#1：構文解析

## 使用法

### 前準備

出力用のファイル名と比較用のファイル名が同じなので比較用のファイルを退避もしくは改名しておく

```
$ rename 's/.xml/_orig.xml/' *.xml
```

### コンパイル

```
$ ./JackAnalizer.py <.jack ファイルの入ったディレクトリ>
```

## 第1段階：トークナイザ

xxxT.xml を出力するプログラムは JackAnalizer_forPhase1.py、JackTokenizer_forPhase1.py とし、第2段階のパーサとは別のプログラムとして書いた。

### 方針

1. 1行読んでコメントもしくは API コメントの途中なら何もせずに次の行へ
2. 読み込んだソースコードの1行からトークンリストを作成する
3. トークンリストを pop し各要素がどのトークンタイプかを見て xml ファイルを記述していく

### make_token_list メソッド

トークンリストを生成するにあたってテキストに記載されている API の他に make_token_list メソッドを追加した。このメソッドは今読まれているソースコードの一行から各トークンを要素としたリストを返す。

  - 例：```if (x < 153)``` → ```['if', '(', 'x', '&lt;', '153', ')']```

この実装はソースコードの一行を一文字ずつ解析することで実現した。

### トークンリストの作り方について

Jack プログラムの中で "（ダブルクォーテーション）で囲まれた部分はプログラマが文字列を自由に記述できるので、コード一行を一文字ずつ読んで解析する方法では工夫が必要となる。

そこで、make_token_list メソッドではダブルクォーテーションの解析は対象外とし、その代わりにメソッドにコード一行を渡す前にダブルクォーテーションについての解析を行った。

例えば ArrayTest/Main.jack の15行目にはダブルクォーテーションが含まれたソースコードが記述されている。

```
let length = Keyboard.readInt("HOW MANY NUMBERS? ");
```

ここでまず Python のダブルクォーテーションを区切りとした split 関数を用いてリスト（list とする）を作成する。このとき元々あったダブルクォーテーションも再度加えておく。

```
## list
['let length = Keyboard.readInt(', '"HOW MANY NUMBERS? "', ');']
```

次に list[0] と list[2] を make_token_list メソッドに渡せばトークンのリストが返されるのであとは適宜それらをつなぎ合わせればよい。

```
token_list = make_token_list(list[0]) + [list[1]] + make_token_list(list[2])
```

これで以下のリストが完成する。

```
# token_list
['let', 'length', '=', 'Keyboard', '.', 'readInt', '(', '"HOW MANY NUMBERS? "', ')', ';']
```

## 第2段階：パーサ

### 第1段階からの変更点

- xxxT.xml ファイルは出力せず、xxx.xml ファイルのみ出力する
- トークンリストを一行ごとではなく Jack プログラム全体分で作成するようにした
  - 例えば ArrayTest/Main.jack を読み込むと以下のような長いリストが作成される
    ```
    ['class', 'Main', '{', ..., 'return', ';', '}', '}']
    ```
- トークンリストの作成を hasMoreTokens() から独立させ、JackAnalyzer から呼び出すようにした
  - make_token_list() メソッド（とその内部にある make_partial_token_list() メソッド）からトークンリストが作成される

### 方針

1. 入力のプログラム全体に適用したトークンリストを作成する
2. 作成したトークンリストをもとにパースを行う

### write_xml メソッド

本プログラム作成にあたってテキストに記載された API に加え、XML をファイルに書き込む write_xml() メソッドを記述した。このメソッドでは終端記号のトークンタイプに基づいて XML を書き込む。また、後続トークンの有無の確認（hasMoreTokens()）、次トークンの読み込み（advance()）も write_xml() 内に記述した。

### 妥協点

- シンタックスのチェックなし
  - つまりコンパイル時に構文エラーなどは検出しない。プログラマが正しくプログラムすることを期待している
- インデント省略
- テキストの p.240 には

  > compilexxx() は、入力の次の構文要素が xxx の場合のみ呼ぶようにするとよい。

  とあるが、条件分岐の関係でコードが乱雑になった（特に expression、term まわり）ので構文要素が xxx であろうとなかろうと呼ぶようにした
  - 11章では XML は関係なくなるので本来はテキストに従った方がいいのかもしれない
