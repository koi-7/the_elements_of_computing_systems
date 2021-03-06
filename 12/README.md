# 12章 オペレーティングシステム

## String

### setInt

- 引数の数値を文字列に変換してセットする
- 新たに文字列をセットするため、代入するインデックスの数字を初期化する必要がある
- 再帰呼び出しを利用した実装を行う
  - 単純に setInt を再帰呼び出しする実装を行おうとすると、毎回インデックスの数字が初期化されるので、2桁以上の負の数値を上手く変換できなくなる（"-" がつかない）
    - 再帰部分のみを処理するメソッド int2String を別に定義してそれを呼び出すことで対処

## Output

### initMap

練習問題の "A" は以下のように黒塗りのピクセルの箇所を列ごとに合計すればよい。なお、Output.create の最初の引数は ASCII コード（10進数）となっている。

![](https://user-images.githubusercontent.com/61448492/91246656-63db2c80-e78b-11ea-9a1e-b04abfa8e13b.png)

### moveCursor

仕様によれば、カーソル移動のあと「そこに表示されている文字を消去」しなければならない。消去する代わりに空白の文字を printChar で書き込むという手法が考えられるが、printChar で書き込んだ後はカーソルが移動するのでスクリーンの右下に移動して何か新たに文字を書き込む（まさにテストファイルに書かれている手続き）際には問題が生じやすいので注意が必要である。

### printChar

先に記した "A" 画像の i 行の数値は map[i] として取得できるので、j ビット目の色を判断するには Math クラスで定義した Math.bit 関数を呼び出すとよい（先人の知恵）。

## Keyboard

### readChar

のちに readLine、readInt のどちらの関数でも使われるので readChar がしっかり動作しないとこれらもうまく動作しない。図12-14（p.296）のアルゴリズム通りの実装ではキーが連続で入力されるので適当に Sys.wait を用いて調整する。

### readLine、readInt

readLine が実装できれば readInt もほとんど同じように実装できる。String から int への変換には String.intValue を用いればよい。

## Memory

### alloc

配列の名前がその配列の先頭のポインタをさすことを意識する。このポインタは数値を加えることで好きな場所を指すことができる。また、他の変数に代入を行えばその変数は同じポインタを指す。

![](https://user-images.githubusercontent.com/61448492/91385692-737e7200-e86c-11ea-95a4-183798d1dbc9.png)

変数として「今注目している空きへの空間ポインタ（current_pointer）」、「そのひとつ手前の空き空間へのポインタ（previous_pointer）」を用意する。

current_pointer の length を見ながら size より大きい空き空間が見つかるまで freeList た辿る（first-fit）。

![](https://user-images.githubusercontent.com/61448492/91388371-200f2280-e872-11ea-89ee-56bc45786333.png)

空き空間が見つかれば block を確保する。block が current_ptr[next] に食い込む場合（current_ptr[length] = size + 1）や block の確保によって current_ptr[lentgth] が 0 になる場合（current_ptr = size + 2）、その領域を飛ばすように freeList を更新する。

![](https://user-images.githubusercontent.com/61448492/91523906-d89f9980-e938-11ea-902c-d6260f7747e0.png)

### deAlloc

解放した領域は freeList の末尾につなげるより先頭にもってくる方が楽。

![](https://user-images.githubusercontent.com/61448492/91414674-dcbfae80-e887-11ea-87ef-5eb80f7e42aa.png)

## Sys

### init

各 OS クラスの init ファンクションを呼び出す順番に注意。
