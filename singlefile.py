# 処理順序
# フォントファイル名を取得！
# textの各文字についてそのunicode値がlistにあるか確認
    # ないものがあれば不可→処理を終了（→次のファイルへ）
# 
# パス／フォント名をリストに保存（→次のファイルへ）
# リストを表示、大きければ表示是非を確認？

import os
import fontTools.ttLib as ttlib

def is_available(text, filepath):
    '.ttf/.otf/.ttc/.otcについて、textがそのフォントで利用可能であるか（利用可能な文字のみから構成されるか）を返す'

    # ファイルの存在確認
    if not os.path.isfile(filepath):
        print('File not found')
        return None

    # ttlib.TTFontにfontNumberとして渡す値のリストを作成する。collectionの場合は内包するフォントを数え、fontの場合、デフォルト値の[-1]とする。
    if filepath.endswith('.ttf') or filepath.endswith('.otf'):
        font_numbers = [-1]
    elif filepath.endswith('.ttc') or filepath.endswith('.otc'):
        try:
            with ttlib.TTCollection(filepath) as collectionfile:
                font_numbers = range(len(collectionfile))
        except:
            print('ERROR:', filepath)
            return None
    else:
        print('UNSUPPORTED_FILE_TYPE:', filepath)
        return None

    # 各フォントでの是非を保存するリストを作成
    availabilities = []

    # 各フォントに対し実行
    for font_number in font_numbers:
        # 当該フォントで利用可能な文字のdict（cmap）を取得
        try:
            with ttlib.TTFont(filepath, fontNumber=font_number) as fontfile:
                cmap = fontfile.getBestCmap()
        except ttlib.TTLibError:
            print('INVALID_FILE_FORMAT:', filepath)
            return None
        except:
            print('ERROR:', filepath)
            return None
        
        # cmapが有効（存在し、その要素数が1以上）だったらUnicode値のリストを取得
        # cmapはdictかNone
        if cmap:
            available_chars = cmap.keys()
        else:
            print('UNSUITABLE_FILE_FORMAT:', filepath)
            return None

        # 調べたいテキストの各文字について利用可能な文字か確認
        # 利用不可能な文字があればreturn False
        an_unavailble_character_is_found = False

        for char in text:
            if ord(char) not in available_chars:
                print('Unavailble character:', char)
                availabilities.append(False)

                an_unavailble_character_is_found = True
                break
        
        if not an_unavailble_character_is_found:
            availabilities.append(True)
    
    return availabilities

path = '/Library/Fonts/GHEAGrapalatBlit.otf'
text = 'hello'

print(is_available(text, path))