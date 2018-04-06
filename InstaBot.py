from init_app import Initapp
from gui_bot import AppGui


if __name__ == "__main__":
    init = Initapp()
    init.install_font()
    app = AppGui()
    app.run()
    app.mainloop()
