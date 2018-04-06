import threading
import tkinter as tk
from tkinter.font import Font
from tkinter.messagebox import showwarning
from tkinter.ttk import Progressbar
from bot_wb import BotWb
from bot_ph import BotPh
from constants import ACCOUNT_INFO, HASHTAG_LIST, STATS, USER_INFO


class AppGui(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.font = Font(family="Zekton", size=14)
        self.font_title = Font(family="Capture it", size=32)
        self.title('InstaBot')
        self.resizable(False, False)
        self.first_title = tk.Label(self, text='INSTABOT V2.0')
        self.first_title.grid(row=0, columnspan=2, sticky='NSEW')
        self.first_title.configure(font=self.font_title)
        self.list_already_good = 1

    def login(self):
        self.login_label = tk.Label(self, text='Login')
        self.login_label.grid(row=1, column=0, sticky='W')
        self.login_label.configure(font=self.font)
        self.password_label = tk.Label(self, text='Password')
        self.password_label.grid(row=2, column=0, sticky='W')
        self.password_label.configure(font=self.font)

        self.value_login = tk.StringVar()
        self.login_entry = tk.Entry(self, textvariable=self.value_login)
        self.login_entry.grid(row=1, column=1, sticky='E')

        self.value_password = tk.StringVar()
        self.password_entry = tk.Entry(self, show='*',
                                       textvariable=self.value_password)
        self.password_entry.grid(row=2, column=1, sticky='E')

    def display_mode(self):
        self.title_display = tk.Label(self, text='Display Mode')
        self.title_display.grid(row=3, columnspan=2, sticky='NSEW')
        self.title_display.configure(font=self.font_title)

        self.display_var = tk.IntVar()
        self.display_one = tk.Checkbutton(self, variable=self.display_var)
        self.display_one_lab = tk.Label(self, text='Web Browser View')
        self.display_one_lab.grid(row=4, column=1)
        self.display_one_lab.configure(font=self.font)
        self.display_one.grid(row=4, column=1, sticky='W')

        self.display_var_two = tk.IntVar()
        self.display_two = tk.Checkbutton(self, variable=self.display_var_two)
        self.display_two_lab = tk.Label(self, text='Phantom Mode')
        self.display_two_lab.grid(row=5, column=1)
        self.display_one_lab.configure(font=self.font)
        self.display_two.grid(row=5, column=1, sticky='W')

    def display_button_start(self):
        self.button_title = tk.Button(self, text='START',
                                      command=self.loading_bar)
        self.button_title.grid(row=6, column=1, sticky='NSEW')
        self.button_title.configure(font=self.font)
        self.button_quit = tk.Button(self, text='QUIT', command=self.quit_gui)
        self.button_quit.grid(row=6, column=0, sticky='NSEW')
        self.button_quit.configure(font=self.font)
        self.progress = Progressbar(self, orient=tk.HORIZONTAL,
                                    mode='determinate')

    def find_display_mode(self):
        self.display_wb = self.display_var.get()
        self.display_ph = self.display_var_two.get()

    def define_driver(self):
        self.find_display_mode()
        if self.display_wb == 1 and self.display_ph == 0:
            self.app = BotWb()
        elif self.display_wb == 0 and self.display_ph == 1:
            self.app = BotPh()
        else:
            showwarning("InstaBot Error", "Wrong display choice...")

    def start_one(self):
        self.username = self.value_login.get()
        self.password = self.value_password.get()
        USER_INFO.append(self.username)
        USER_INFO.append(self.password)
        self.define_driver()
        self.app.login_sel(self.username, self.password)
        if self.app.find_if_log() is False:
            showwarning("InstaBot Error", "Wrong Password... Please try again")
        else:
            self.app.find_welcome_elements(self.username)
            self.post = ACCOUNT_INFO[0]
            self.followers = ACCOUNT_INFO[1]
            self.following = ACCOUNT_INFO[2]
            self.welcome()
            self.hashtag_list()
            self.mode_choice()
            self.login_label.destroy()
            self.password_label.destroy()
            self.login_entry.destroy()
            self.password_entry.destroy()
            self.display_button_start_bot()
            self.update_idletasks()

    def loading_bar(self):
        def loading_traitement():
            self.progress.grid(row=6, column=1, sticky='NSEW')
            self.progress.start()
            self.start_one()
            self.progress.stop()
            self.progress.grid_forget()
            self.button_title['state'] = 'normal'
        self.button_title['state'] = 'disabled'
        threading.Thread(target=loading_traitement).start()

    def welcome(self):
        self.title_welcome = tk.Label(self,
                                      text='Welcome {} ,'
                                      .format(self.username))
        self.title_welcome.grid(row=1, columnspan=2, sticky='W')
        self.title_welcome.configure(font=self.font, bg='white', fg='black')

        self.welcome_posts = tk.Label(self,
                                      text='Posts: {}'
                                      .format(self.post))
        self.welcome_posts.grid(row=2, columnspan=2, sticky='W')
        self.welcome_posts.configure(font=self.font, bg='white', fg='black')

        self.welcome_flw = tk.Label(self,
                                    text='Followers: {}'
                                    .format(self.followers))
        self.welcome_flw.grid(row=2, columnspan=2)
        self.welcome_flw.configure(font=self.font, bg='white', fg='black')

        self.welcome_flwing = tk.Label(self,
                                       text='Following: {}'
                                       .format(self.following))
        self.welcome_flwing.grid(row=2, columnspan=2, sticky='E')
        self.welcome_flwing.configure(font=self.font, bg='white', fg='black')

    def hashtag_list(self):
        self.display_one.destroy()
        self.display_one_lab.destroy()
        self.title_hastag = tk.Label(self, text='Hashtag')
        self.title_hastag.grid(row=3, columnspan=2, sticky='NSEW')
        self.title_hastag.configure(font=self.font_title)

        self.button_get_last = tk.Button(self, text='Last Ones',
                                         command=self.last_hash)
        self.button_get_last.grid(row=4, column=0, sticky='NSEW')
        self.button_get_last.configure(font=self.font)
        self.button_get_last = tk.Button(self, text='Clear',
                                         command=self.clear_hash)
        self.button_get_last.grid(row=4, column=1, sticky='NSEW')
        self.button_get_last.configure(font=self.font)

        self.value_hash1 = tk.StringVar()
        self.hash1 = tk.Entry(self, textvariable=self.value_hash1)
        self.hash1.grid(row=5, column=0, sticky='W')

        self.value_hash2 = tk.StringVar()
        self.hash2 = tk.Entry(self, textvariable=self.value_hash2)
        self.hash2.grid(row=5, column=1, sticky='E')

        self.value_hash3 = tk.StringVar()
        self.hash3 = tk.Entry(self, textvariable=self.value_hash3)
        self.hash3.grid(row=6, column=0, sticky='W')

        self.value_hash4 = tk.StringVar()
        self.hash4 = tk.Entry(self, textvariable=self.value_hash4)
        self.hash4.grid(row=6, column=1, sticky='E')

        self.value_hash5 = tk.StringVar()
        self.hash5 = tk.Entry(self, textvariable=self.value_hash5)
        self.hash5.grid(row=7, column=0, sticky='W')

        self.value_hash6 = tk.StringVar()
        self.hash6 = tk.Entry(self, textvariable=self.value_hash6)
        self.hash6.grid(row=7, column=1, sticky='E')

        self.value_hash7 = tk.StringVar()
        self.hash7 = tk.Entry(self, textvariable=self.value_hash7)
        self.hash7.grid(row=8, column=0, sticky='W')

        self.value_hash8 = tk.StringVar()
        self.hash8 = tk.Entry(self, textvariable=self.value_hash8)
        self.hash8.grid(row=8, column=1, sticky='E')

        self.value_hash9 = tk.StringVar()
        self.hash9 = tk.Entry(self, textvariable=self.value_hash9)
        self.hash9.grid(row=9, column=0, sticky='W')

        self.value_hash10 = tk.StringVar()
        self.hash10 = tk.Entry(self, textvariable=self.value_hash10)
        self.hash10.grid(row=9, column=1, sticky='E')

    def last_hash(self):
        self.app.load_hashtag_list()
        self.print_last_hash()
        self.update_idletasks()

    def print_last_hash(self):
        try:
            self.hash1.delete(0, tk.END)
            self.hash1.insert(0, '{}'.format(HASHTAG_LIST[0]))
            self.hash1['state'] = 'disabled'
            self.hash2.delete(0, tk.END)
            self.hash2.insert(0, '{}'.format(HASHTAG_LIST[1]))
            self.hash2['state'] = 'disabled'
            self.hash3.delete(0, tk.END)
            self.hash3.insert(0, '{}'.format(HASHTAG_LIST[2]))
            self.hash3['state'] = 'disabled'
            self.hash4.delete(0, tk.END)
            self.hash4.insert(0, '{}'.format(HASHTAG_LIST[3]))
            self.hash4['state'] = 'disabled'
            self.hash5.delete(0, tk.END)
            self.hash5.insert(0, '{}'.format(HASHTAG_LIST[4]))
            self.hash5['state'] = 'disabled'
            self.hash6.delete(0, tk.END)
            self.hash6.insert(0, '{}'.format(HASHTAG_LIST[5]))
            self.hash6['state'] = 'disabled'
            self.hash7.delete(0, tk.END)
            self.hash7.insert(0, '{}'.format(HASHTAG_LIST[6]))
            self.hash7['state'] = 'disabled'
            self.hash8.delete(0, tk.END)
            self.hash8.insert(0, '{}'.format(HASHTAG_LIST[7]))
            self.hash8['state'] = 'disabled'
            self.hash9.delete(0, tk.END)
            self.hash9.insert(0, '{}'.format(HASHTAG_LIST[8]))
            self.hash9['state'] = 'disabled'
            self.hash10.delete(0, tk.END)
            self.hash10.insert(0, '{}'.format(HASHTAG_LIST[9]))
            self.hash10['state'] = 'disabled'
        except IndexError:
            pass
        self.list_already_good = 0

    def clear_hash(self):
        self.hash1['state'] = 'normal'
        self.hash1.delete(0, tk.END)
        self.hash2['state'] = 'normal'
        self.hash2.delete(0, tk.END)
        self.hash3['state'] = 'normal'
        self.hash3.delete(0, tk.END)
        self.hash4['state'] = 'normal'
        self.hash4.delete(0, tk.END)
        self.hash5['state'] = 'normal'
        self.hash5.delete(0, tk.END)
        self.hash6['state'] = 'normal'
        self.hash6.delete(0, tk.END)
        self.hash7['state'] = 'normal'
        self.hash7.delete(0, tk.END)
        self.hash8['state'] = 'normal'
        self.hash8.delete(0, tk.END)
        self.hash9['state'] = 'normal'
        self.hash9.delete(0, tk.END)
        self.hash10['state'] = 'normal'
        self.hash10.delete(0, tk.END)
        HASHTAG_LIST.clear()
        self.list_already_good = 1

    def get_hash_put_list(self):
        hashtag_1 = self.value_hash1.get()
        HASHTAG_LIST.append(hashtag_1)
        self.hash1['state'] = 'disabled'
        hashtag_2 = self.value_hash2.get()
        HASHTAG_LIST.append(hashtag_2)
        self.hash2['state'] = 'disabled'
        hashtag_3 = self.value_hash3.get()
        HASHTAG_LIST.append(hashtag_3)
        self.hash3['state'] = 'disabled'
        hashtag_4 = self.value_hash4.get()
        HASHTAG_LIST.append(hashtag_4)
        self.hash4['state'] = 'disabled'
        hashtag_5 = self.value_hash5.get()
        HASHTAG_LIST.append(hashtag_5)
        self.hash5['state'] = 'disabled'
        hashtag_6 = self.value_hash6.get()
        HASHTAG_LIST.append(hashtag_6)
        self.hash6['state'] = 'disabled'
        hashtag_7 = self.value_hash7.get()
        HASHTAG_LIST.append(hashtag_7)
        self.hash7['state'] = 'disabled'
        hashtag_8 = self.value_hash8.get()
        HASHTAG_LIST.append(hashtag_8)
        self.hash8['state'] = 'disabled'
        hashtag_9 = self.value_hash9.get()
        HASHTAG_LIST.append(hashtag_9)
        self.hash9['state'] = 'disabled'
        hashtag_10 = self.value_hash10.get()
        HASHTAG_LIST.append(hashtag_10)
        self.hash10['state'] = 'disabled'
        print(HASHTAG_LIST)

    def mode_choice(self):
        self.title_multiple_choice = tk.Label(self, text='Mode')
        self.title_multiple_choice.grid(row=10, columnspan=2, sticky='NSEW')
        self.title_multiple_choice.configure(font=self.font_title)

        self.choice_one_var = tk.IntVar()
        self.choice_one = tk.Checkbutton(self, variable=self.choice_one_var)
        self.choice_one_lab = tk.Label(self, text='Like')
        self.choice_one_lab.grid(row=11, column=0)
        self.choice_one_lab.configure(font=self.font)
        self.choice_one.grid(row=11, column=0, sticky='E')

        self.choice_two_var = tk.IntVar()
        self.choice_two = tk.Checkbutton(self, variable=self.choice_two_var)
        self.choice_two_lab = tk.Label(self, text='Comments')
        self.choice_two_lab.grid(row=12, column=0)
        self.choice_two_lab.configure(font=self.font)
        self.choice_two.grid(row=12, column=0, sticky='E')

        self.choice_three_var = tk.IntVar()
        self.choice_three = tk.Checkbutton(self,
                                           variable=self.choice_three_var)
        self.choice_three_lab = tk.Label(self, text='Follow')
        self.choice_three_lab.grid(row=13, column=0)
        self.choice_three_lab.configure(font=self.font)
        self.choice_three.grid(row=13, column=0, sticky='E')

        self.choice_four_var = tk.IntVar()
        self.choice_four = tk.Checkbutton(self,
                                          variable=self.choice_three_var)
        self.choice_four_lab = tk.Label(self, text='Unfollow')
        self.choice_four_lab.grid(row=14, column=0)
        self.choice_four_lab.configure(font=self.font)
        self.choice_four.grid(row=14, column=0, sticky='E')

    def display_button_start_bot(self):
        self.button_start = tk.Button(self, text='START',
                                      command=self.loading_start)
        self.button_start.grid(row=15, column=1, sticky='NSEW')
        self.button_start.configure(font=self.font)
        self.button_quit_2 = tk.Button(self, text='QUIT',
                                       command=self.quit_gui)
        self.button_quit_2.grid(row=15, column=0, sticky='NSEW')
        self.button_quit_2.configure(font=self.font)
        self.progress_two = Progressbar(self, orient=tk.HORIZONTAL,
                                        mode='determinate')

    def bots_working(self):
        self.title_bots_working = tk.Label(self, text='Works Done')
        self.title_bots_working.grid(row=16, columnspan=2, sticky='NSEW')
        self.title_bots_working.configure(font=self.font_title)

        self.image_liked = tk.Label(self, text='Images Liked: {}'
                                    .format(STATS[0]))
        self.image_liked.grid(row=17, column=0, sticky='W')
        self.image_liked.configure(font=self.font)

        self.com_post = tk.Label(self, text='Comments posted: {}'
                                 .format(STATS[1]))
        self.com_post.grid(row=18, column=0, sticky='W')
        self.com_post.configure(font=self.font)

        self.follow_f = tk.Label(self, text='Followed: {}'
                                 .format(STATS[2]))
        self.follow_f.grid(row=19, column=0, sticky='W')
        self.follow_f.configure(font=self.font)

        self.after(2000, self.bots_working)

    def find_mode(self):
        self.lik_mode = self.choice_one_var.get()
        self.com_mode = self.choice_two_var.get()
        self.fol_mode = self.choice_three_var.get()

    def start_two(self):
        if self.list_already_good == 1:
            self.get_hash_put_list()
            self.app.put_hash_to_txt()
        self.find_mode()
        if self.lik_mode == 1 and self.com_mode == 0 and self.fol_mode == 0:
            self.app.run_like_mode()
        elif self.lik_mode == 1 and self.com_mode == 1 and self.fol_mode == 0:
            # run like com mode
            self.app.run_like_com_mode()
        elif self.lik_mode == 1 and self.com_mode == 1 and self.fol_mode == 1:
            # run like com fol mode
            pass
        elif self.lik_mode == 0 and self.com_mode == 1 and self.fol_mode == 0:
            # run com mode
            pass
        elif self.lik_mode == 0 and self.com_mode == 1 and self.fol_mode == 1:
            # run com follow mode
            pass
        elif self.lik_mode == 0 and self.com_mode == 0 and self.fol_mode == 1:
            # run fol mode
            pass
        else:
            showwarning("InstaBot Error", "Wrong Mode Choice")

    def loading_start(self):
        def loading_traitement_two():
            self.progress_two.grid(row=15, column=1, sticky='NSEW')
            self.progress_two.start()
            self.start_two()
            self.progress_two.stop()
            self.progress_two.grid_forget()
            self.button_title['state'] = 'normal'
        self.button_title['state'] = 'disabled'
        threading.Thread(target=loading_traitement_two).start()
        self.bots_working()

    def quit_gui(self):
        self.destroy()

    def run(self):
        self.login()
        self.display_mode()
        self.display_button_start()


if __name__ == "__main__":
    app = AppGui()
    app.run()
    app.mainloop()
