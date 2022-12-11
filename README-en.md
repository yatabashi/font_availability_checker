# fontac

i.e. <ins>Font</ins> <ins>A</ins>vailability <ins>C</ins>hecker

In other languages: [日本語](./README.md)

`fontac` lists fonts which can display a text.

## Installation
(only on macOS) The following command enables its use as a CLI tool:
```
pip install git+https://github.com/yatabashi/font_availability_checker.git@main
```
Uninstallation is done with `pip uninstall fontac`.

You can also use the program by directly running the source file. In this case, download the package as follows.
* If Git is installed, run the following command:
    ```
    git clone https://github.com/yatabashi/font_availability_checker.git
    ```
* Otherwise,
    1. Click on the green button labeled "Code".
    1. Download a ZIP file by clicking on "Download ZIP".
    1. Unzip it.

## Usage
* Use as CLI tool:  
    The following format is recognised as a command:
    ```
    fontac (-f [queried file] | -d [queried dir]) (-t) (-p) [text]
    ```
    The options `-f` and `-d` are mutually exclusive. See below for details.
* Direct use of source file:  
    Make use of `fontac/main_direct.py`. The variables in line 5 to 9 need to be set. See below for details.

When executing the program, specify the text to be displayed, the search target and the output format.
* Text to be displayed
    | CLI | main_direct.py |
    | - | - |
    | required | `text` |

* Search target
    | CLI | main_direct.py | description |
    | - | - | - |
    | with `-f` and file path | `type == 'file'` | Output whether the single font is capable of displaying the specified text |
    | with `-d` and dir path | `type == 'dir'` with `path` set | Output ones capable of displaying the specified text from among the fonts located in the specified directory (recursively searched) |
    | without either | `type == 'all'` with `path` set | Output ones capable of displaying the specified text from among all the fonts installed (no limitation of search range) |

* Search method
    | CLI | main_direct.py | 説明 |
    | - | - | - |
    | with `-t` | `requires_thoroughness = True` | Check subfamily names and examine every font in Collection file |
    | without `-t` | `requires_thoroughness = False` | Ignore differences of subfamily names and examine only the first font in Collection file |

* Output format (valid only if the search target is NOT a single font)
    | CLI | main_direct.py | description |
    | - | - | - |
    | with `-p` | `show_paths == True` | Output the font names and the paths of the corresponding files |
    | without `-p` | `show_paths == False` | Output the font names only |
