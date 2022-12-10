import argparse
import os
import logging
from . import udfs

def main():
    # コマンドライン引数
    parser = argparse.ArgumentParser(
        description='`fontac` lists fonts which can display a text.'
    )

    meg = parser.add_mutually_exclusive_group()
    meg.add_argument('-f', '--file', help='check a file')
    meg.add_argument('-d', '--dir', help='check a dir')
    parser.add_argument('-p', '--shows-paths', action='store_true', help='append the paths of the applicable fonts to the output')
    parser.add_argument('text')

    args = parser.parse_args()

    text = args.text
    if args.file:
        type = 'file'
        path = os.path.abspath(args.file)
    elif args.dir:
        type = 'dir'
        path = os.path.abspath(args.dir)
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
        udfs.main_for_dir(text, path, args.shows_paths)
    elif type == 'all':
        udfs.main_for_allfonts(text, args.shows_paths)

if '__name__' == '__main__':
    main()
