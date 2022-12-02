# TODO: 
# Windowsへの対応
#    パスの生成を工夫する必要がある
#    階層区切りは共通で/でいいという噂

import os
import logging
from tqdm import tqdm
import udfs

def main():
    # 定義
    dirpaths = ['/System/Library/Fonts', '/Library/Fonts', os.path.expanduser('~/Library/Fonts')]
    text = input('Input: ') # /ʔ(ə)ŋ/は[ʔŋ̍]であって[ʔə̩ŋ]ではないよなあと思ってしまっている
    available_fonts = set()

    # fontToolsが警告を出力しないようにする
    logging.disable(logging.WARNING)

    # 判定部分
    for dirpath in dirpaths:
        # tqdmでプログレスバーを表示しながら全ファイルを巡回
        for filepath in tqdm(udfs.all_paths(dirpath)):
            # macではこのファイルがエイリアスとしてデフォルトであるらしいので無視
            if filepath == '/Library/Fonts/Arial Unicode.ttf':
                continue
            
            # 取得
            # set型に入れて重複を回避
            fontname_and_availability = udfs.fetch_fontname_and_availability(text, filepath)

            if fontname_and_availability is not None:
                fontname, available = fontname_and_availability
                if available:
                    available_fonts.add(fontname)

    # ソート
    available_fonts_sorted = sorted(list(available_fonts))

    # 出力
    for available_font in available_fonts_sorted:
        print(available_font)

if __name__ == '__main__':
    main()