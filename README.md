# fontac

i.e. <ins>Font</ins> <ins>A</ins>vailability <ins>C</ins>hecker

## Installation
```
pip install git+https://github.com/yatabashi/font_availability_checker.git@main
```

Its use as a CLI tool (see below) is supported only on macOS. `fontac/main_direct.py` works on both macOS and Windows.

## Usage
```
fontac (-f [filepath] | -d [dirpath]) [text]
```
* Without any options, it outputs the list of the already installed fonts capable of displaying the text specified.
* When you'd like to know if **a specific font** can display the text, use `-f` option to specify its file.
* If you examine **two or more fonts**, use `-d` option and specify the directory containing them. The program recursively traverses the directory.
* The options `-f` and `-d` are mutually exclusive.