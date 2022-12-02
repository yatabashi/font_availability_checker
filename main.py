# ターミナルから実行できるようにしたい

import udfs

# CUI
# text = input('text: ')
# type = input('file/dir/dirs: ')
# if type in ['file', 'dir']:
#     path = input('path: ')
# elif type == 'dirs':
#     pass
# else:
#     sys.exit('Invalid input')

# 直接入力
text = '/ʔ(ə)ŋ/は[ʔŋ̍]であって[ʔə̩ŋ]ではないよなあと思ってしまっている'
type = 'file'
path = '/System/Library/Fonts/Supplemental/AmericanTypewriter.ttc'

# 実行
if type == 'file':
    udfs.main_for_file(text, path)
elif type == 'dir':
    udfs.main_for_dir(text, path)
elif type == 'dirs':
    udfs.main_for_dirs(text)
