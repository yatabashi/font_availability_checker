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
    parser.add_argument('-t', '--thorough', action='store_true', help='target literally all the fonts included')
    parser.add_argument('-p', '--shows-paths', action='store_true', help='append the paths of the applicable fonts to the output')
    parser.add_argument('text')

    args = parser.parse_args()

    text = args.text
    if args.file:
        type = 'file'
        specified_path = os.path.abspath(args.file)
    elif args.dir:
        type = 'dir'
        specified_path = os.path.abspath(args.dir)
    else:
        type = 'all'

    # 準備
    used_chars = {ord(character) for character in text}
    requires_thoroughness = args.thorough
    shows_paths = args.shows_paths

    logging.disable(logging.WARNING) # リンク参照unpackPStrings()内での警告出力を抑制：https://fonttools.readthedocs.io/en/latest/_modules/fontTools/ttLib/tables/_p_o_s_t.html

    # 実行
    if type == 'file':
        udfs.process_on_file(used_chars, specified_path, requires_thoroughness)
    elif type == 'dir':
        udfs.process_on_dir(used_chars, specified_path, requires_thoroughness, shows_paths)
    elif type == 'all':
        udfs.process_on_all(used_chars, requires_thoroughness, shows_paths)

if '__name__' == '__main__':
    main()
