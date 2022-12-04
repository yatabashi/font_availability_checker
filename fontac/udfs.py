import sys
import os
from fontTools import ttLib as ttlib
import logging
from tqdm import tqdm

def all_paths(dirpath: str):
    'ディレクトリ下の全ファイルのパスを（再帰的に）取得する'
    
    paths = []

    for current_path, _, files in os.walk(dirpath):
        for file in files:
            path = current_path + '/' + file
            paths.append(path)
            
    return paths

def fetch_fontname_and_availability(text: str, filepath: str): # -> (fontname, isavailable, abend, message)
    '.ttf/.otf/.ttc/.otcについて、そのフォント名と、textがそのフォントで利用可能であるか（利用可能な文字のみから構成されるか）を返す'
    
    # ファイルの存在確認
    if not os.path.isfile(filepath):
        return (None, None, 1, 'File not found')
    
    # 当該フォントで利用可能な文字のdict（cmapテーブル）と、フォント名を得るためのnameテーブルを取得
    try:
        # fontNumber=0 は.ttc/.otcの場合にフォントを指定するためのもの。.ttf/.otfの場合、この設定は無視される。
        with ttlib.TTFont(filepath, fontNumber=0) as fontfile:
            # cmapテーブル、nameテーブルを取得
            cmap = fontfile.getBestCmap()
            name_table = fontfile['name'].names
    except:
        return (None, None, 1, 'Failed to read file')
    
    # cmapが有効（存在し、その要素数が1以上）だったらUnicode値のリストを取得
    # cmapはdictかNone
    if cmap:
        available_chars = cmap.keys()
    else:
        return (None, None, 1, 'Contains no font data suitable')
        
    # フォント名を取得
    j_family_name = e_family_name = ''
    for name in name_table:
        isJapanese = (name.platformID == 1 and name.langID == 11) or (name.platformID == 3 and name.langID == 1041)
        isEnglish = (name.platformID == 1 and name.langID == 0) or (name.platformID == 3 and name.langID == 1033)
        
        if isJapanese and (name.nameID == 1 or name.nameID == 16):
            j_family_name = str(name)
        
        if isEnglish and (name.nameID == 1 or name.nameID == 16):
            e_family_name = str(name)

    if j_family_name:
        fontname = j_family_name
    elif e_family_name:
        fontname = e_family_name
    else:
        fontname = filepath[filepath.rfind('/')+1:] + ' (failed to read the font name)'

    # 調べたいテキストの各文字について利用可能な文字か確認
    # 利用不可能な文字があればFalseを返し、なければTrueを返す
    # TODO:高速化できるか？
    for char in text:
        if ord(char) not in available_chars:
            return (fontname, False, 0, f'it doesn\'t contain "{char}"')
    
    return (fontname, True, 0, '')

def extract_available_fonts(text: str, dirpath: str):
    # ディレクトリの存在確認
    if not os.path.isdir(dirpath):
        return None

    # 定義
    available_fonts = set()

    # fontToolsが警告を出力しないようにする
    logging.disable(logging.WARNING)

    # tqdmでプログレスバーを表示しながら全ファイルを巡回
    for filepath in tqdm(all_paths(dirpath)):
        # macではこのファイルがエイリアスとしてデフォルトであるらしいので無視
        if filepath == '/Library/Fonts/Arial Unicode.ttf':
            continue
        
        # 取得
        # set型に入れて重複を回避
        fontname, isavailable, _, _ = fetch_fontname_and_availability(text, filepath)

        if isavailable:
            available_fonts.add(fontname)

    # ソート
    available_fonts_sorted = sorted(list(available_fonts))

    return available_fonts_sorted

def main_for_file(text: str, filepath: str):
    # ファイルの存在確認
    if not os.path.isfile(filepath):
        print('File not found')
        return
    
    # fontToolsが警告を出力しないようにする
    logging.disable(logging.WARNING)

    # 取得
    fontname, isavailable, abend, message = fetch_fontname_and_availability(text, filepath)

    if not abend:
        if isavailable:
            print(f'{fontname} is available for the text.')
        else:
            print(f'{fontname} is NOT available for the text; {message}')
    else:
        print(message)

def main_for_dir(text: str, dirpath: str):
    available_fonts_sorted = extract_available_fonts(text, dirpath)

    if available_fonts_sorted is None:
        print('Directory not found')

    # 出力
    print(f'{len(available_fonts_sorted)} hits:')
    for available_font in available_fonts_sorted:
        print(available_font)

def main_for_allfonts(text: str):
    # 定義
    os_name = os.name
    if os_name == 'posix':
        dirpaths = ['/System/Library/Fonts', '/Library/Fonts', os.path.expanduser('~/Library/Fonts')]
    elif os_name == 'nt':
        dirpaths = ['C:\Windows\Fonts']
    else:
        print('Unsupported OS')
        sys.exit()

    available_fonts = set()

    # 判定部分
    for dirpath in dirpaths:
        available_fonts.update(extract_available_fonts(text, dirpath))

    # ソート
    available_fonts_sorted = sorted(list(available_fonts))

    # 出力
    print(f'{len(available_fonts_sorted)} hits:')
    for available_font in available_fonts_sorted:
        print(available_font)