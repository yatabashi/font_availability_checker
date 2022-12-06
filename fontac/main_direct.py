import logging
import udfs

# 直接入力
text = '㐧'
type = 'all'
path = ''

logging.disable(logging.WARNING)

# 実行
if type == 'file':
    udfs.main_for_file(text, path)
elif type == 'dir':
    udfs.main_for_dir(text, path)
elif type == 'all':
    udfs.main_for_allfonts(text)
