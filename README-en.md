# fontac

i.e. <ins>Font</ins> <ins>A</ins>vailability <ins>C</ins>hecker

In other languages：[日本語](./README.md)

Here I publish a program that outputs the fonts which can display the characters, or tells whether a particular font is available for a text.

## Installation
(only on macOS) The following command enables its use as a CLI tool:
```
pip install git+https://github.com/yatabashi/font_availability_checker.git@main
```
Uninstallation is done with `pip uninstall fontac`.

You can also use the program by writing settings directly in the file. In this case, download the package as follows.
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
    fontac (-f [queried file] | -d [queried dir]) (-p) [text]
    ```
    The options `-f` and `-d` are mutually exclusive. See below for details.
* Direct use of source file:  
    Make use of `fontac/main_direct.py`. In running the program, set the four variables `text`, `type`, `path`, and `shows_paths` in line 5 to 8. See below for details.

When executing the program, set the text to be displayed, the search target and the output format.
* Text to be displayed
    | CLI | main_direct.py |
    | - | - |
    | required | `text` |

* Search target
    | CLI | main_direct.py | description |
    | - | - | - |
    | with `-f` and file path | `type == 'file'` | Outputs whether the single font is capable of displaying the specified text |
    | with `-d` and dir path | `type == 'dir'`with `path` set | Outputs ones capable of displaying the specified text from among the fonts located in the specified directory (recursively searched) |
    | without either | `type == 'all'`with `path` set | Outputs ones capable of displaying the specified text from among all the fonts installed (no limitation of search range) |

* Output format (valid only if the search target is NOT a single font)
    | CLI | main_direct.py | description |
    | - | - | - |
    | `-v`あり | `is_verbose == True` | Outputs the determinations of each font point by point |
    | `-v`なし | `is_verbose == False` | Doesn't output the determinations of each font |

    | CLI | main_direct.py | description |
    | - | - | - |
    | with `-p` | `show_paths == True` | Outputs the font names and the paths of the corresponding files |
    | without `-p` | `show_paths == False` | Outputs the font names only |
