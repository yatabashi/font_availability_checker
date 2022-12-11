import sys
import os
from fontTools import ttLib
from tqdm import tqdm
import typing

# 基本定数・基本関数定義
FONT_DIRS_ON_MACOS = ['/System/Library/Fonts', '/System/Library/AssetsV2/com_apple_MobileAsset_Font7', '/Library/Fonts', os.path.expanduser('~/Library/Fonts')]
FONT_DIRS_ON_WINDOWS = ['C:\Windows\Fonts', os.path.expanduser('~\AppData\Local\Microsoft\Windows\Fonts')]

def get_fontfile_paths(dir_path: str):
    paths = []

    for current_path, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(('.ttf', '.otf', '.ttc', '.otc')):
                path = current_path + '/' + file

                # macOS環境で、エイリアスとしてあるので無視
                if path == '/Library/Fonts/Arial Unicode.ttf':
                    continue

                paths.append(path)

    return sorted(paths)

def get_family_name(file, file_path):
    name_table = file['name'].names

    # リファレンスを参照：https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html, https://learn.microsoft.com/en-us/typography/opentype/spec/name#platform-encoding-and-language-ids

    j_family_name = e_family_name = ''
    for name in name_table:
        is_japanese = (name.platformID == 1 and name.langID == 11) or (name.platformID == 3 and name.langID == 1041)
        is_english = (name.platformID == 1 and name.langID == 0) or (name.platformID == 3 and name.langID == 1033)
        is_family_name = name.nameID == 1 or name.nameID == 16 # nameID 1はsubfamily名を含む場合があり、16はない場合がある

        if is_japanese and is_family_name:
            j_family_name = str(name)

        if is_english and is_family_name:
            e_family_name = str(name)

    if j_family_name:
        return j_family_name
    elif e_family_name:
        return e_family_name
    else:
        return file_path[file_path.rfind('/')+1:] + ' (failed to read the font name)'

def get_full_name(file, file_path):
    name_table = file['name'].names

    # リファレンスを参照：https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html, https://learn.microsoft.com/en-us/typography/opentype/spec/name#platform-encoding-and-language-ids

    j_full_name = e_full_name = ''
    for name in name_table:
        is_japanese = (name.platformID == 1 and name.langID == 11) or (name.platformID == 3 and name.langID == 1041)
        is_english = (name.platformID == 1 and name.langID == 0) or (name.platformID == 3 and name.langID == 1033)
        is_full_name = name.nameID == 4

        if is_japanese and is_full_name:
            j_full_name = str(name)

        if is_english and is_full_name:
            e_full_name = str(name)

    if j_full_name:
        return j_full_name
    elif e_full_name:
        return e_full_name
    else:
        return file_path[file_path.rfind('/')+1:] + ' (failed to read the font name)'

def get_font_number(file_path):
    try:
        with ttLib.TTCollection(file_path) as collection:
            return len(collection)
    except:
        return 1

# ファイルに対する関数定義
def fetch_availability(used_chars: set, file_path: str, discards: set = {}): # -> (abend, name, is_available, message)
    if not os.path.isfile(file_path):
        return (1, None, None, 'file not found')
        
    try:
        with ttLib.TTFont(file_path, fontNumber=0) as font:
            name = get_family_name(font, file_path)

            if name in discards:
                return (1, name, None, 'discarded')
            
            cmap = font.getBestCmap()
            available_chars = cmap.keys()

            used_and_unavailable_chars = used_chars - available_chars

            if len(used_and_unavailable_chars) == 0:
                return (0, name, True, '')
            else:
                return (0, name, False, f'unavailable are {used_and_unavailable_chars}')
    except:
        return (1, None, None, 'failed to load')

def fetch_availability_with_thoroughness(used_chars: set, file_path: str): # .ttc/.otc対応のため、list()を返す
    if not os.path.isfile(file_path):
        return [(1, None, None, 'file not found')]
        
    returns = []

    for i in range(get_font_number(file_path)):
        try:
            with ttLib.TTFont(file_path, fontNumber=i) as font:
                name = get_full_name(font, file_path)

                cmap = font.getBestCmap()
                available_chars = cmap.keys()

                used_and_unavailable_chars = used_chars - available_chars

                if len(used_and_unavailable_chars) == 0:
                    returns.append((0, name, True, ''))
                else:
                    returns.append((0, name, False, f'unavailable are {used_and_unavailable_chars}'))
        except:
            returns.append((1, None, None, 'failed to load'))
    
    return returns

# ディレクトリに対する関数定義
def extract_fonts_available(used_chars: set, dir_path: str):
    if not os.path.isdir(dir_path):
        return None

    discovered_fonts = set()
    available_fontname_to_paths: typing.Dict[str, typing.List[str]] = dict()
        
    for file_path in tqdm(get_fontfile_paths(dir_path)):
        _, font_name, is_available, _ = fetch_availability(used_chars, file_path, discovered_fonts)

        discovered_fonts.add(font_name)

        if is_available:
            if font_name in available_fontname_to_paths:
                available_fontname_to_paths[font_name].append(file_path)
            else:
                available_fontname_to_paths[font_name] = [file_path]
    
    return available_fontname_to_paths

def extract_fonts_available_with_thoroughness(used_chars: set, dir_path: str):
    if not os.path.isdir(dir_path):
        return None

    available_fontname_to_paths: typing.Dict[str, typing.List[str]] = dict()
        
    for file_path in tqdm(get_fontfile_paths(dir_path)):
        results = fetch_availability_with_thoroughness(used_chars, file_path)

        for result in results:
            _, font_name, is_available, _ = result

            if is_available:
                if font_name in available_fontname_to_paths:
                    available_fontname_to_paths[font_name].append(file_path)
                else:
                    available_fontname_to_paths[font_name] = [file_path]

    return available_fontname_to_paths

# mainから実行する関数定義
def process_on_file(used_chars, specified_path, requires_thoroughness):
    if requires_thoroughness:
        results = fetch_availability_with_thoroughness(used_chars, specified_path)

        for result in results:
            abend, name, is_available, message = result

            if abend:
                print(f'ERROR: {message}')
            else:
                if is_available:
                    print(f'Yes, {name} is available.')
                else:
                    print(f'No, {name} is unavailable: {message}')
    else:
        abend, name, is_available, message = fetch_availability(used_chars, specified_path)

        if abend:
            print(f'ERROR: {message}')
        else:
            if is_available:
                print(f'Yes, {name} is available.')
            else:
                print(f'No, {name} is unavailable: {message}')

def process_on_dir(used_chars, specified_path, requires_thoroughness, shows_paths):
    if requires_thoroughness:
        available_fontname_to_paths = extract_fonts_available_with_thoroughness(used_chars, specified_path)
    else:
        available_fontname_to_paths = extract_fonts_available(used_chars, specified_path)

    if available_fontname_to_paths is None:
        print('dir not found')

    available_fonts_sorted = sorted(list(available_fontname_to_paths.keys()))

    print(f'{len(available_fonts_sorted)} hits:')

    if shows_paths:
        for available_font in available_fonts_sorted:
            print(f'{available_font}: {available_fontname_to_paths[available_font]}')
    else:
        for available_font in available_fonts_sorted:
            print(available_font)

def process_on_all(used_chars, requires_thoroughness, shows_paths):
    platform = sys.platform

    if platform == 'darwin':
        dir_paths = FONT_DIRS_ON_MACOS
    elif platform == 'win32':
        dir_paths = FONT_DIRS_ON_WINDOWS
    else:
        print('Platform unsupported')
        return

    all_available_fontname_to_paths: typing.Dict[str, typing.List[str]] = dict()

    print(f'{len(dir_paths)} directories are to loaded.')
    for dir_path in dir_paths:
        if requires_thoroughness:
            available_fontname_to_paths = extract_fonts_available_with_thoroughness(used_chars, dir_path)
        else:
            available_fontname_to_paths = extract_fonts_available(used_chars, dir_path)

        # resultがNoneとなる（dirが見つからない）ことがもしあったらエラーを吐くべき

        for fontname, paths in available_fontname_to_paths.items():
            if fontname in all_available_fontname_to_paths.keys():
                all_available_fontname_to_paths[fontname].extend(paths)
            else:
                all_available_fontname_to_paths[fontname] = paths

    all_available_fonts_sorted = sorted(list(all_available_fontname_to_paths.keys()))

    print(f'{len(all_available_fonts_sorted)} hits:')

    if shows_paths:
        for available_font in all_available_fonts_sorted:
            print(f'{available_font}: {all_available_fontname_to_paths[available_font]}')
    else:
        for available_font in all_available_fonts_sorted:
            print(available_font)
