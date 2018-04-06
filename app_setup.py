from setuptools import setup

APP = ['run.py']
DATA_FILES = ['files/hashtag_list.txt', 'font/Capture_it.ttf',
              'font/zektron_rg.ttf', 'bot_ph.py', 'bot_wb.py', 'constants.py',
              'gui_bot.py', 'init_font.py']
OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
