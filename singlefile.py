import udfs

path = '/Library/Fonts/GHEAGrapalatBlit.otf'
text = 'おはよー'

fontname, isavailable = udfs.fetch_fontname_and_availability(text, path)

print(f'{fontname} is{"" if isavailable else " NOT"} available for the text.')