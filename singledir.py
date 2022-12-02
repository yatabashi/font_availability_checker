import udfs

dirpath = '/Users/kuroiwashu/Library/Fonts'
text = '/ʔ(ə)ŋ/は[ʔŋ̍]であって[ʔə̩ŋ]ではないよなあと思ってしまっている'
available_fonts = []

for filepath in udfs.all_paths(dirpath):
    tup = udfs.fetch_fontname_and_availability(text, filepath)

    if tup is not None:
        fontname, available = tup
        if available:
            available_fonts.append(fontname)

for available_font in available_fonts:
    print(available_font)