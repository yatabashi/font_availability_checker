import os
import fontTools.ttLib as ttlib
import logging

logging.disable((logging.WARNING))

from tqdm import tqdm

def fetch_fontname_and_availability(text, filepath):
    '.ttf/.otf/.ttc/.otcについて、textがそのフォントで利用可能であるか（利用可能な文字のみから構成されるか）を返す'
    
    # ファイルの存在確認
    if not os.path.isfile(filepath):
        # print('File not found')
        return None
    
    # ttlib.TTFontにfontNumberとして渡す値を設定する。collectionの場合は一律0とし、fontの場合、デフォルト値の-1とする。
    # TODO: これ、fontの場合も0でよかったり？
    if filepath.lower().endswith('.ttf') or filepath.lower().endswith('.otf'):
        font_number = -1
    elif filepath.lower().endswith('.ttc') or filepath.lower().endswith('.otc'):
        font_number = 0
    else:
        # print('UNSUPPORTED_FILE_TYPE:', filepath)
        return None
    
    # 当該フォントで利用可能な文字のdict（cmapテーブル）と、フォント名を得るためのnameテーブルを取得
    try:
        with ttlib.TTFont(filepath, fontNumber=font_number) as fontfile:
            # cmapテーブル、nameテーブルを取得
            cmap = fontfile.getBestCmap() # TODO: 1 extra bytes in post.stringData array のような警告が出る場合がある
            name_table = fontfile['name'].names
            
    except ttlib.TTLibError:
        # print('INVALID_FILE_FORMAT:', filepath)
        return None
    except:
        # print('ERROR:', filepath)
        return None
    
    # cmapが有効（存在し、その要素数が1以上）だったらUnicode値のリストを取得
    # cmapはdictかNone
    if cmap:
        available_chars = cmap.keys()
    else:
        # print('UNSUITABLE_FILE_FORMAT:', filepath)
        return None
        
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
    # 利用不可能な文字があればFalseを返す
    for char in text:
        if ord(char) not in available_chars:
            # print('Unavailble character:', char) <- 問い合わせがあった場合には答えるか。
            return (fontname, False)
    
    return (fontname, True)

def all_paths(dir_path):
    paths = []

    for current_path, _, files in os.walk(dir_path):
        for file in files:
            path = current_path + '/' + file
            paths.append(path)
            
    return paths

dirpaths = ['/System/Library/Fonts', '/Library/Fonts', os.path.expanduser('~/Library/Fonts')]
text = '/ʔ(ə)ŋ/は[ʔŋ̍]であって[ʔə̩ŋ]ではないよなあと思ってしまっている'
available_fonts = set()

for dirpath in dirpaths:
    for filepath in tqdm(all_paths(dirpath)):
        # エイリアスとしてデフォルトであるらしい
        if filepath == '/Library/Fonts/Arial Unicode.ttf':
            continue

        fontname_and_availability = fetch_fontname_and_availability(text, filepath)

        if fontname_and_availability is not None:
            fontname, available = fontname_and_availability
            if available:
                available_fonts.add(fontname)

available_fonts_sorted = sorted(list(available_fonts))

for available_font in available_fonts_sorted:
    print(available_font)