from fontac import udfs

# 直接入力
text = '/ʔ(ə)ŋ/は[ʔŋ̍]であって[ʔə̩ŋ]ではないよなあと思ってしまっている'
type = 'file'
path = '/System/Library/Fonts/Supplemental/AmericanTypewriter.ttc'

# 実行
if type == 'file':
    udfs.main_for_file(text, path)
elif type == 'dir':
    udfs.main_for_dir(text, path)
elif type == 'all':
    udfs.main_for_allfonts(text)