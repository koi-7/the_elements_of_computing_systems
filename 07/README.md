# 7章 バーチャルマシン#1：スタック操作

- 関数内で大域変数を書き換える時は関数内で ```global SP``` などして宣言する
  - でないと関数内で ```SP += 1``` といった記述ができない