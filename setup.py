from setuptools import setup

setup(
    name = 'fontac', # パッケージ名
    description='extracts fonts available for a specified text, from all the ones installed as default',
    version = '4.1',
    author='yatabashi',
    install_requires = ['fontTools', 'tqdm'],
    packages=['fontac'],
    entry_points = {
        "console_scripts": ['fontac = fontac.main:main'], # ['パッケージ名 = ファイル名:関数名']
    }
)
