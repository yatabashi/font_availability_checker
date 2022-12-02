import logging
from tqdm import tqdm
import udfs

def main():
    # 定義
    dirpath = '/Users/kuroiwashu/Library/Fonts'
    text = input('Input: ') # /ʔ(ə)ŋ/は[ʔŋ̍]であって[ʔə̩ŋ]ではないよなあと思ってしまっている
    available_fonts = set()

    # fontToolsが警告を出力しないようにする
    logging.disable(logging.WARNING)

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