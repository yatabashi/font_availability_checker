import logging
import udfs

# 直接入力
text = '' # 検索対象の文字列を指定する
type = 'all' # 検索の種類を指定する。'all'は全フォントから利用可能なものを抽出して出力する。'file'は一つの、'dir'は複数のフォントの利用可能性を判定する。
path = '' # typeが'file'または'dir'の場合、そのフォントのファイルまたはファイルを含むディレクトリを指定する。
shows_paths = False # typeが'dir'または'all'の場合、該当したフォントのファイルパスも出力するかどうかを指定する（Trueで出力して、Falseで出力しない）。

logging.disable(logging.WARNING)

# 実行
if type == 'file':
    udfs.main_for_file(text, path)
elif type == 'dir':
    udfs.main_for_dir(text, path, shows_paths)
elif type == 'all':
    udfs.main_for_allfonts(text, shows_paths)
else:
    print('invalid value set to `type`')
