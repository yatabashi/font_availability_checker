import logging
import udfs

# 直接入力
text = '' # 検索対象の文字列を指定する
type = 'all' # 検索の種類を指定する。'all'は全フォントから利用可能なものを抽出して出力する。'file'は一つの、'dir'は複数のフォントの利用可能性を判定する。
path = '' # typeが'file'または'dir'の場合、そのフォントのファイルまたはファイルを含むディレクトリを指定する。
requires_thoroughness = False # サブファミリーや、Collectionファイルの各フォントまで精査するか。
shows_paths = False # typeが'dir'または'all'の場合、該当したフォントのファイルパスも出力するかどうかを指定する（Trueで出力して、Falseで出力しない）。

# 準備
used_chars = {ord(character) for character in text}
specified_path = path

logging.disable(logging.WARNING) # リンク参照unpackPStrings()内での警告出力を抑制：https://fonttools.readthedocs.io/en/latest/_modules/fontTools/ttLib/tables/_p_o_s_t.html

# 実行
if type == 'file':
    udfs.process_on_file(used_chars, specified_path, requires_thoroughness)
elif type == 'dir':
    udfs.process_on_dir(used_chars, specified_path, requires_thoroughness, shows_paths)
elif type == 'all':
    udfs.process_on_all(used_chars, requires_thoroughness, shows_paths)
else:
    print('invalid value set to `type`')
