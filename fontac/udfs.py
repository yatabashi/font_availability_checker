import sys
import os
from fontTools import ttLib as ttlib
from tqdm import tqdm
import typing

def all_fontfile_paths(dirpath: str):
    'ディレクトリ下の全フォントファイルのパスを（再帰的に）取得する'

    paths = []

    for current_path, _, files in os.walk(dirpath):
        for file in files:
            if file.endswith(('.ttf', '.otf', '.ttc', '.otc')):
                path = current_path + '/' + file

                # macではこのファイルがエイリアスとしてデフォルトであるらしいので無視
                if path == '/Library/Fonts/Arial Unicode.ttf':
                    continue

                paths.append(path)

    return sorted(paths)

def get_fontname(name_table, filepath):
    # リファレンス（下記リンク）を参照
    # https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html
    # https://learn.microsoft.com/en-us/typography/opentype/spec/name#platform-encoding-and-language-ids

    j_family_name = e_family_name = ''
    for name in name_table:
        isJapanese = (name.platformID == 1 and name.langID == 11) or (name.platformID == 3 and name.langID == 1041)
        isEnglish = (name.platformID == 1 and name.langID == 0) or (name.platformID == 3 and name.langID == 1033)
        isFamilyName = name.nameID == 1 or name.nameID == 16

        if isJapanese and isFamilyName:
            j_family_name = str(name)

        if isEnglish and isFamilyName:
            e_family_name = str(name)

    if j_family_name:
        return j_family_name
    elif e_family_name:
        return e_family_name
    else:
        return filepath[filepath.rfind('/')+1:] + ' (failed to read the font name)'

def check_availability(text: str, filepath: str, discovered: typing.List[str]): # -> (fontname, isavailable, abend, message)
    'フォントファイルについて、そのフォント名と、textがそのフォントで利用可能であるか（利用可能な文字のみから構成されるか）を返す'

    # ファイルの存在確認
    if not os.path.isfile(filepath):
        return (None, None, 1, 'file not found')

    # 当該フォントで利用可能な文字のdict（cmapテーブル）と、フォント名を得るためのnameテーブルを取得
    try:
        # fontNumber=0 は.ttc/.otcの場合にフォントを指定するためのもの。.ttf/.otfの場合、この設定は無視される。
        # 下記リンク参照
        # https://fonttools.readthedocs.io/en/latest/ttLib/ttFont.html#fontTools.ttLib.ttFont.TTFont
        # https://aznote.jakou.com/prog/opentype/05_name.html
        with ttlib.TTFont(filepath, fontNumber=0) as fontfile:
            # nameテーブルからフォント名を取得
            name_table = fontfile['name'].names
            fontname = get_fontname(name_table, filepath)

            # そのフォントファミリーがすでに発見されていれば無視する
            if fontname in discovered:
                return (None, None, 1, 'this font family already discovered')

            # cmapテーブルを取得
            cmap: dict = fontfile.getBestCmap()
    except:
        return (None, None, 1, 'failed to read file')

    # cmapが有効（存在し、その要素数が1以上）だったらUnicode値のリストを取得
    # cmapはdictかNone
    if cmap:
        available_chars = cmap.keys()
    else:
        return (None, None, 1, 'contains no font data suitable')

    # 調べたいテキストの各文字について利用可能な文字か確認
    # 利用不可能な文字があればFalseを返し、なければTrueを返す
    for char in text:
        if ord(char) not in available_chars:
            return (fontname, False, 0, f'doesn\'t contain "{char}"')

    return (fontname, True, 0, '')

def main_for_file(text: str, filepath: str):
    # 取得
    _, isavailable, abend, message = check_availability(text, filepath)

    if not abend:
        if isavailable:
            print(f'Yes, available.')
        else:
            print(f'No, unavailable; {message}')
    else:
        print(f'Error: {message}')

def main_for_dir(text: str, dirpath: str, shows_paths: bool):
    # ディレクトリの存在確認
    if not os.path.isdir(dirpath):
        print('Directory not found')
        return

    # 定義
    discovered_fonts = set()
    available_fonts = set()
    fontname_to_paths: typing.Dict[str, typing.List[str]] = dict()

    # tqdmでプログレスバーを表示しながら全ファイルを巡回
    for filepath in tqdm(all_fontfile_paths(dirpath)):
        # 取得
        fontname, isavailable, _, _ = check_availability(text, filepath, discovered_fonts)

        # 記録
        # set型に入れて重複を回避
        # 発見されたことを記録
        if fontname:
                discovered_fonts.add(fontname)

        # 利用可能であったことを記録
        if isavailable:
            available_fonts.add(fontname)

            if fontname in fontname_to_paths:
                fontname_to_paths[fontname].append(filepath)
            else:
                fontname_to_paths[fontname] = [filepath]

    # ソート
    available_fonts_sorted = sorted(list(available_fonts))

    # 出力
    print(f'{len(available_fonts_sorted)} hits:')

    if shows_paths:
        for available_font in available_fonts_sorted:
            print(f'{available_font}: {fontname_to_paths[available_font]}')
    else:
        for available_font in available_fonts_sorted:
            print(available_font)

def main_for_allfonts(text: str, shows_paths: bool):
    # 定義
    platform = sys.platform
    if platform == 'darwin':
        dirpaths = ['/System/Library/Fonts', '/System/Library/AssetsV2/com_apple_MobileAsset_Font7', '/Library/Fonts', os.path.expanduser('~/Library/Fonts')]
    elif platform == 'win32':
        dirpaths = ['C:\Windows\Fonts', os.path.expanduser('~\AppData\Local\Microsoft\Windows\Fonts')]
    else:
        print('Platform unsupported')
        sys.exit()

    discovered_fonts = set()
    available_fonts = set()
    fontname_to_paths: typing.Dict[str, typing.List[str]] = dict()

    # 判定部分
    for dirpath in dirpaths:
        # tqdmでプログレスバーを表示しながら全ファイルを巡回
        for filepath in tqdm(all_fontfile_paths(dirpath)):
            # 取得
            fontname, isavailable, _, _ = check_availability(text, filepath, discovered_fonts)

            # 記録
            # set型に入れて重複を回避
            # 発見されたことを記録
            if fontname:
                discovered_fonts.add(fontname)

            # 利用可能であったことを記録
            if isavailable:
                available_fonts.add(fontname)

                if fontname in fontname_to_paths:
                    fontname_to_paths[fontname].append(filepath)
                else:
                    fontname_to_paths[fontname] = [filepath]

    # ソート
    available_fonts_sorted = sorted(list(available_fonts))

    # 出力
    print(f'{len(available_fonts_sorted)} hits:')

    if shows_paths:
        for available_font in available_fonts_sorted:
            print(f'{available_font}: {fontname_to_paths[available_font]}')
    else:
        for available_font in available_fonts_sorted:
            print(available_font)
