# ターミナルから実行できるようにしたい

import os
import sys
import udfs
import argparse

# コマンドライン引数
# 絶対パス／相対パス？
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


# コマンドラインinput
# text = input('text: ')
# type = input('file/dir/all: ')
# if type in ['file', 'dir']:
#     path = input('path: ')
# elif type == 'all':
#     pass
# else:
#     sys.exit('Invalid input')


# 直接入力
# text = '/ʔ(ə)ŋ/は[ʔŋ̍]であって[ʔə̩ŋ]ではないよなあと思ってしまっている'
# type = 'file'
# path = '/System/Library/Fonts/Supplemental/AmericanTypewriter.ttc'


# 実行
if type == 'file':
    udfs.main_for_file(text, path)
elif type == 'dir':
    udfs.main_for_dir(text, path)
elif type == 'all':
    udfs.main_for_allfonts(text)
