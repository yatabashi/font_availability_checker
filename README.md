# fontac

i.e. <ins>Font</ins> <ins>A</ins>vailability <ins>C</ins>hecker

他言語版：[English](./README-en.md)

`fontac`は、ある文字列を表示可能なフォントをリストアップするプログラムです。

## インストール
CLIツールとして利用する（macOSでのみ可能）ためには、次のコマンドを実行してください：
```
pip install git+https://github.com/yatabashi/font_availability_checker.git@main
```
アンインストールは`pip uninstall fontac`で可能です。

また、ソースファイルを直接実行して利用することも可能です。その場合、次のようにしてパッケージをダウンロードしてください。
* Gitがインストールされている場合、次を実行する：  
    ```
    git clone https://github.com/yatabashi/font_availability_checker.git
    ```
* Gitがインストールされて**いない**場合、緑色のボタン「Code」をクリックし、「Download ZIP」からZIPファイルをダウンロードして、これを展開する。

## 使い方
* CLIツールとして使う：  
次の形式のコマンドが利用可能です。なお、`-f`オプションと`-d`オプションは相互に排他的です。
    ```
    fontac (-f [照会するファイル] | -d [照会するディレクトリ]) (-p) [テキスト]
    ```
    詳細は下記を参照してください。

* ソースファイルを直接使う：  
`fontac/main_direct.py`を利用してください。5行目から8行目の変数が設定される必要があります。詳細は下記を参照してください。

実行の際は、表示したいテキスト、検索対象、出力形式を指定してください。
* 表示したいテキスト
    | CLI | main_direct.py |
    | - | - |
    | 必須 | `text` |

* 検索対象
    | CLI | main_direct.py | 説明 |
    | - | - | - |
    | `-f`とファイルパス | `type == 'file'` | 指定された一つのフォントが、指定されたテキストを表示可能かどうかを出力する |
    | `-d`とディレクトリパス | `type == 'dir'`および`path`の設定 | 指定されたディレクトリ内（再帰的に検索）に存在するフォントの中から、指定されたテキストを表示可能なものを出力する |
    | どちらも指定せず | `type == 'all'`および`path`の設定 | インストールされている全てのフォントの中から、指定されたテキストを表示できるものを出力する（検索範囲を制限しない） |

* 出力形式（検索対象が単一ファイルでない場合のみ有効）
    | CLI | main_direct.py | 説明 |
    | - | - | - |
    | `-p`あり | `show_paths == True` | フォント名と、対応するフォントファイルのパスを出力する |
    | `-p`なし | `show_paths == False` | フォント名のみを出力する |

<!-- TODO:
available_fontsとfontname_to_paths.keys()に同じデータを保存していて冗長
 -->