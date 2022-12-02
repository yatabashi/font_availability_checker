import logging
import udfs

def main():
    # 定義
    filepath = '/Library/Fonts/GHEAGrapalatBlit.otf'
    text = input('Input: ') # /ʔ(ə)ŋ/は[ʔŋ̍]であって[ʔə̩ŋ]ではないよなあと思ってしまっている

    # fontToolsが警告を出力しないようにする
    logging.disable(logging.WARNING)

    # 取得
    fontname_and_availability = udfs.fetch_fontname_and_availability(text, filepath)

    if fontname_and_availability is not None:
        fontname, isavailable = fontname_and_availability
        
        print(f'{fontname} is{"" if isavailable else " NOT"} available for the text.')
    else:
        print('unsupported file')

if __name__ == '__main__':
    main()