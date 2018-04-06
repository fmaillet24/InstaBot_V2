from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from constants import ACCOUNT_INFO, HASHTAG_LIST, STATS, COM_LIST
from random import randint


class BotPh():

    def __init__(self):
        self.com_nb = 0
        self.nb_like = 0
        self.cmp_hash = 0
        self.cmp_like = 0
        self.list_link = []
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options=options)

    def login_sel(self, username, password):
        self.browser.get('https://www.instagram.com/accounts/login/')
        self.browser.implicitly_wait(2)
        sleep(1)
        user = self.browser.find_element_by_name('username')
        user.send_keys(username)
        sleep(1)
        self.browser.implicitly_wait(2)
        pwd = self.browser.find_element_by_name('password')
        pwd.send_keys(password)
        self.browser.implicitly_wait(2)
        sleep(1)
        btn = self.browser.find_element_by_xpath('//form/span/button[text()="Log in"]')
        btn.click()
        self.browser.implicitly_wait(2)

    def find_if_log(self):
        try:
            self.browser.find_element_by_xpath('//*[@id="slfErrorAlert"]')
            return False
        except NoSuchElementException:
            return True

    def find_welcome_elements(self, username):
        self.browser.get('https://instagram.com/{}'.format(username))
        self.browser.implicitly_wait(2)
        for info in self.browser.find_elements_by_class_name("_fd86t"):
            ACCOUNT_INFO.append(info.text)

    def hashtag_search(self):
        self.browser.get('https://instagram.com/explore/tags/{}'
                         .format(HASHTAG_LIST[self.cmp_hash]))

    def find_list_to_like(self):
        search_link = '/p'
        find_pict_link = self.browser.find_elements_by_tag_name('a')
        for element in find_pict_link:
            link_pict = element.get_attribute('href')
            if search_link in link_pict:
                self.list_link.append(link_pict)

    def link_to_like(self):
        self.browser.get('{}'.format(self.list_link[self.cmp_like]))

    def hash_like(self):
        self.browser.execute_script("window.scrollTo(0, 200);")
        sleep(1)
        try:
            self.browser.find_elements_by_xpath("//a[@role='button']/span[text()='Like']/..")[0].click()
        except IndexError:
            pass

    def com_pict(self):
        self.rand_com = randint(0, 19)
        self.com = COM_LIST[self.rand_com]
        self.com_button = self.browser.find_elements_by_xpath("//a[@role='button']/span[text()='Comment']/..")[0]
        self.com_button.click()
        sleep(1)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.publier_click = self.browser.find_elements_by_xpath('//textarea[@placeholder = "Add a comment…"]')[0]
        self.publier_click.click()
        self.publier_click.send_keys(self.com)
        sleep(1)
        self.publier_click.submit()

    #def follow(self):
    #    button_follow = body/div[4]/div[1]/div[2]/div[1]/article[1]/header[1]/div[2]/div[1]/div[2]/span[2]/button[1]


    def run_like_mode(self):
        while self.cmp_hash < 11:
            self.cmp_like = 10
            self.hashtag_search()
            self.find_list_to_like()
            while self.cmp_like < 21:
                if self.nb_like <= 500:
                    self.when_i_like = randint(6, 10)
                    self.link_to_like()
                    sleep(self.when_i_like)
                    self.hash_like()
                    sleep(self.when_i_like)
                    self.nb_like += 1
                    STATS[0] = self.nb_like
                    self.cmp_like += 1
            self.list_link.clear()
            self.cmp_hash += 1

    def run_like_com_mode(self):
        while self.cmp_hash < 11:
            self.cmp_like = 10
            self.hashtag_search()
            self.find_list_to_like()
            while self.cmp_like < 21:
                if self.nb_like <= 500:
                    self.when_i_like = randint(6, 10)
                    self.link_to_like()
                    sleep(self.when_i_like)
                    self.hash_like()
                    sleep(self.when_i_like)
                    self.com_pict()
                    sleep(self.when_i_like)
                    self.com_nb += 1
                    self.nb_like += 1
                    STATS[0] = self.nb_like
                    STATS[1] = self.com_nb
                    self.cmp_like += 1
                elif self.nb_like >= 500:
                    self.when_i_like = randint(6, 10)
                    self.link_to_like()
                    sleep(self.when_i_like)
                    self.com_pict()
                    sleep(self.when_i_like)
                    self.com_nb += 1
                    self.nb_like += 1
                    STATS[0] = self.nb_like
                    STATS[1] = self.com_nb
                    self.cmp_like += 1
            self.list_link.clear()
            self.cmp_hash += 1

    def run_like_com_fol_mode(self):
        pass
