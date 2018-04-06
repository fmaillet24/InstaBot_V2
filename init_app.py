import getpass
import shutil
import os


class Initapp():

    def __init__(self):
        self.username = getpass.getuser()
        self.app_path = os.getcwd()

    def install_font(self):
        capture_it_path = '{}/font/Capture_it.ttf'.format(self.app_path)
        zektron_path = '{}/font/zekton_rg.ttf'.format(self.app_path)
        destination_path = '/Users/{}/Library/Fonts/'.format(self.username)

        shutil.copy2(capture_it_path, destination_path)
        shutil.copy2(zektron_path, destination_path)


if __name__ == "__main__":
    app = Initapp()
    app.install_font()
