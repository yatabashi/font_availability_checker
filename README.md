# fontac

i.e. <u>Font</u> <u>A</u>vailability <u>C</u>hecker

## Installation
```
pip install git+https://github.com/yatabashi/font_availability_checker.git@main
```

Supported only on macOS. On Windows

## Usage
```
fontac (-f [filepath] | -d [dirpath]) [text]
```
* Without any options, it outputs the list of the already installed fonts capable of displaying the text specified.
* When you'd like to know if **a specific font** can display the text, use `-f` option to specify its file.
* If you examine two or more fonts, use `-d` option and specify the directory containing them. The program recursively traverses the directory.
* The options `-f` and `-d` are mutually exclusive.