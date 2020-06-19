![](https://github.com/penpenpng/powami-script/workflows/Test/badge.svg)

# ぽわみスクリプト
ぽわみスクリプトは人類と [ぽわみbot](https://twitter.com/powamibot) の対話のために生まれた言語です。


# 使い方
文法にしたがってぽわみスクリプトを構成し、 ぽわみbot にリプライを送信……すると使えるようになる予定です。

または、 Python を用意して、

```
> pip install -r requirements.txt
> rpws script.pws [arg]
```

で実行します。 `rpws` は Windows 向けのヘルパーです。Mac や Linux をお使いの方は同等のものを自作するか、単に `python -m pws script.pws <arg>` してください。


# サンプルコード
`/samples` に置いてあります。


# リファレンス
## 有効な文字
**ぽわみスクリプト** のソースコードの中で有効な文字は下記の7種に限られます:

```
ぽ わ ！ ？ ～ ー っ
```

`！？～ー` はいずれも全角であることに注意してください。

上記以外のすべての文字は無視されるため、コメントとして活用できます。

なお、空白文字、タブ文字、改行も同様に無視されますが、本リファレンスでは見やすさのために適宜これらの文字を使うことがあります。
実際のスクリプトでは単語を空白で区切る必要はありませんし、インデントも不要です。


## 変数
ぽわみスクリプトには **変数** を宣言する文法はありません。

代わりに、最初から以下の 10 個の変数が用意されています:

* `ぽ～わ`
* `わ～ぽ`
* `ぽ` または `わ` のみからなる 3 文字の文字列 (全 8 種)

基本的にはすべての変数の初期値は空文字列ですが、以下の変数は例外です:

* `ぽ～わ` の初期値は、プログラムへの入力文字列です
    * プログラムへの入力が存在しない場合は空文字列になります
* `ぽぽぽ` の初期値は 文字列 `ぽ` です
* `わわわ` の初期値は 文字列 `わ` です

上記の 3 つの変数はあくまで初期値が特別なだけで、その他の点では通常の変数となんら変わりません。
後から値を上書きすることも可能です。


## 値
ぽわみスクリプトの変数に格納できる値は **ぽわみ型の文字列** だけです。

ぽわみ型の文字列とは、空文字列または `ぽわ！？～ー` の 6 種類の文字のみから構成される文字列のことです。
ぽわみ型文字列は `っ` を含むことができないことに注意してください。


## 入出力
前述の通り、ぽわみスクリプトのプログラムへの入力は変数 `ぽ～わ` の初期値として与えられます。
入力はぽわみ型の文字列のみが許されます。
`ぽわ！？～ー` 以外の文字が入力に含まれていた場合、その文字は読み捨てられます。

プログラムの出力は、スクリプトが終了した時点で `わ～ぽ` に格納されている値です。
または、後述するように、実行時にエラーが発生した場合の出力は `ぽ……？` になります。


## 変数の更新
変数に格納されている値の更新には **命令文** を用います。
命令文とは **命令語** と 1 つまたは 2 つの変数をそのまま繋げたものです。
命令語の後にいくつの変数を伴うかは、命令語ごとに決まっています。

例えば、命令語 `ぽー！` は 1 つの変数を伴って用います。
したがって `ぽー！ ぽわわ` は正しい命令文です。
この命令文は、変数 `ぽわわ` に格納されている文字列の右端1文字を削除します。

命令語の完全なリストは本リファレンスの末尾付録を参照してください。

### 特別な命令語: `ぽわ～`
`ぽわ～` はいわゆる代入のために用いる命令語で、例外的な文法に従います。

`ぽわ～` の後には 1 つの変数と 1 文字以上のぽわみ型の文字列と `っ` がこの順で続きます。
例えば、`ぽわ～ ぽわわ ぽ！わ！わ～ っ` は正しい命令文です。
この命令文は、変数 `ぽわわ` に文字列 `ぽ！わ！わ～` を格納します。

`ぽわ～` によって変数に空文字列を格納することはできません。

`ぽわ～` の 2 番目のパラメータに変数を渡すことはできないことに注意してください。
`ぽわ～ ぽわわ ぽぽぽ っ` は正しい命令文ですが、変数 `ぽぽぽ` の中身が 変数 `ぽわわ` にコピーされるわけではありません。


## 制御文
ぽわみスクリプトにはいわゆる `if` や `while` に近い機能を持つ **制御文** が用意されています。

制御文は次のように構成されます:

```
<制御キーワード> <変数> <パターン> っ
    <ブロック>
っ
```

ここで、

* **制御キーワード** とは `ぽ？`, `ぽ！？`, `わ？`, `わ！？` のいずれかのことです
* **パターン** とは `ぽわ！？～ー` の 6 種類の文字からなる 1 文字以上の文字列です
* **ブロック** とは 1 つ以上の **文** のことです
    * 文 とは 命令文 または 制御文 のことです

例えば、`ぽ？ ぽわわ ぽーわ っ <命令文> <制御文> っ` は正しい制御文です。

制御文は、与えられた変数の値がパターンと **マッチ** したかどうかに応じて、制御キーワードごとに異なった振る舞いをします。


### パターンとマッチ
#### 短い説明
本節はこの手の概念に慣れている人のための手短な説明です。
不慣れな人はこの節を飛ばして次に進んでください。

* `ー` は正規表現における `.` と同様に振る舞います
* `～` は正規表現における `*` と同様に振る舞います
    * ただし例外的に、パターンが `～` のみの 1 文字ならば、パターンは空文字列のみとマッチします
* `？` は(拡張)正規表現における `?` と同様に振る舞います
* `！` はメタ文字をエスケープします
    * `！！` のようにして自分自身をエスケープします


#### 丁寧な説明
1 つのパターンは 1 つのぽわみ文字列の集合を表します。
「値 `X` がパターン `P` とマッチする」とは、`P` が表す集合に、`X` が含まれていることを指します。

* `ぽ` または `わ` のみからなるパターンは、それと全く同じ見た目のぽわみ文字列のみを含む集合を表します。
    * つまり、パターン `ぽわ` にマッチする文字列は `ぽわ` だけです。
* パターンが中に `ー` を含むとき、パターンは `ー` を任意の1文字に置き換えてできるすべての文字列の集合を表します。
    * 例えば、パターン `ぽー` は文字列 `ぽわ` にも `ぽぽ` にもマッチします。`ぽー` 自体にももちろんマッチします。
* パターンが中に `～` を含むとき、パターンは `～` とその直前の文字 `C` を `C` の 0 回以上の繰り返しに置き換えてできるすべての文字列の集合を表します。
    * 例えば、パターン `ぽわ～` は `ぽ`, `ぽわ`, `ぽわわ`, `ぽわわわ` などにマッチします。
* パターンが中に `？` を含むとき、パターンは `？` 自体とその直前の 0 文字以上 1 文字以下の文字列を削除してできるすべての文字列の集合を表します。
    * 例えば、パターン `ぽぽ？` は `ぽ` または `ぽぽ` にのみマッチします。
* 上記のパターンは組み合わせて用いることができます。
    * 例えば、`ぽー～わ` は `ぽ` で始まって `わ` で終わるすべての文字列にマッチします。
* 上述のように `？`, `ー`, `～` はパターンの中で特別な働きをします。これらの文字の特別な働きを無効化して、単にそれ自体とマッチさせたいとき、特別な文字の直前に `！` を置きます。
    * 例えば、パターン `ぽわ！～` は `ぽわ～` のみにマッチします。
    * `！` もまた特別な文字です。したがって `ぽわ！` だけにマッチさせたいパターンは `ぽわ！！` と書きます。
* 例外的に、パターン `～` は空文字列とだけマッチします。


### 条件分岐
* 制御キーワードが `ぽ？` の場合、値がパターンにマッチしたときに限ってブロック内を実行します
* 制御キーワードが `ぽ！？` の場合、値がパターンにマッチしなかったときに限ってブロック内を実行します


### ループ
* 制御キーワードが `わ？` の場合、
    1. 値がパターンにマッチしているか確かめます
    2. 1 でマッチしていれば、ブロックの実行します
    3. 1 に戻ります
* 制御キーワードが `わ！？` の場合もほぼ同様ですが、2 でブロックを実行するのは 1 でマッチしていなかったときです


#### ループの中断
1 つの制御文のブロックの実行回数の上限は 1000 回です。


## エラー
スクリプトが文法上正しくても、以下の場合にはエラーになります。エラーが発生した場合、プログラムの出力は `ぽ……？` に置き換えられます。

* パターンが解釈不能なとき
    * 例えば、パターン `？` は `？` の直前に何も存在しないため、解釈不能です
* 1 つのループが 1000 回を超えて実行されたとき


## 命令語の一覧
下記表で、`x` は 1 番目の変数を、`y` は (存在するならば) 2 番目の変数を表しています。

|  命令語  | 変数の数 | 説明                                                                                                             |
| :------: | :------: | :--------------------------------------------------------------------------------------------------------------- |
|  ぽ～～  |    2     | `x` を `x` の右側に `y` を繋げたものにする。                                                                     |
|  わ～～  |    2     | `x` を `x` の左側に `y` を繋げたものにする。                                                                     |
|  ぽーー  |    2     | `x` を `x` の右端 1 文字を削除したものにし、`y` を削除した 1 文字にする。削除に失敗した時 `y` は空文字列になる。 |
|  わーー  |    2     | `x` を `x` の左端 1 文字を削除したものにし、`y` を削除した 1 文字にする。削除に失敗した時 `y` は空文字列になる。 |
|  ぽー！  |    1     | `x` を `x` の右端 1 文字を削除したものにする。                                                                   |
|  わー！  |    1     | `x` を `x` の左端 1 文字を削除したものにする。                                                                   |
| ぽーわわ |    1     | `x` を `x` の **反転** にする。                                                                                  |
|   ぽぽ   |    2     | `x` を `x` と `y` の **積** にする。                                                                             |
|   わわ   |    2     | `x` を `x` と `y` の **和** にする。                                                                             |
|  ぽわ～  |   特殊   | 「特別な命令語」の節を参照。                                                                                     |
|  わぽ～  |    2     | `x` を `y` と同じにする。                                                                                        |

反転、積、和について説明するために、文字の種類と量について次で説明します。


### 文字の種類と量
ぽわみ文字 (ぽわみ型の文字列を構成する 6 種類の文字) はそれぞれが **属性** と **量** を 1 つずつ持ちます。

| 文字  | 属性  |  量   |
| :---: | :---: | :---: |
|  ぽ   | ぽわ  |   1   |
|  わ   | ぽわ  |   0   |
|  ！   | ！？  |   1   |
|  ？   | ！？  |   0   |
|  ～   | ～ー  |   1   |
|  ー   | ～ー  |   0   |


### 反転
文字列の反転とは、その文字列の各文字の量を変化させた文字列のことです。`ぽわ！` の反転は `わぽ？` です。


### 積
2 つの文字列の積とは、次の手続きに従って得られる文字列のことです。

1. 左端を合わせて文字列の各文字を対応させる。対応にあぶれた文字は削除する。
2. 各文字の対応について……
   * 文字の属性が異なれば、文字を削除する。
   * 文字の属性が等しければ、量が *小さい* 方の文字を残す。


### 和
2 つの文字列の和とは、次の手続きに従って得られる文字列のことです。積と異なる点は、量の大きい方の文字を残す点のみです。

1. 左端を合わせて文字列の各文字を対応させる。対応にあぶれた文字は削除する。
2. 各文字の対応について……
   * 文字の属性が異なれば、文字を削除する。
   * 文字の属性が等しければ、量が *大きい* 方の文字を残す。

