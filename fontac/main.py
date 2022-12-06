import argparse
import os
import logging
import udfs

def main():
    # コマンドライン引数
    parser = argparse.ArgumentParser()

    meg = parser.add_mutually_exclusive_group()
    meg.add_argument('-f', '--file', help='specifies a font file checked')
    meg.add_argument('-d', '--directory', help='specifies a directory in which font files checked exist')
    parser.add_argument('text')

    args = parser.parse_args()

    text = args.text
    if args.file:
        type = 'file'
        path = os.path.abspath(args.file)
    elif args.directory:
        type = 'dir'
        path = os.path.abspath(args.directory)
    else:
        type = 'all'

    # fontToolsが警告を出力しないようにする
    # unpackPStrings()内でwarningが出力されている（下記リンク参照）
    # https://fonttools.readthedocs.io/en/latest/_modules/fontTools/ttLib/tables/_p_o_s_t.html
    logging.disable(logging.WARNING)

    # 実行
    if type == 'file':
        udfs.main_for_file(text, path)
    elif type == 'dir':
        udfs.main_for_dir(text, path)
    elif type == 'all':
        udfs.main_for_allfonts(text)

if '__name__' == '__main__':
    main()
