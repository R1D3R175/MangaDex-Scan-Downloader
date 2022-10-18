from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from xpaths import *

class WebScraper:
    def __init__(self, url, language, chapters):
        self.URL = url
        self.language = language
        self.chapters = chapters
        self.stop = False

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--log-level=3") # FATAL
        options.add_argument("--disable-gpu")
        options.add_argument("--hide-scrollbars")

        service = Service(r"/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=options)

        self._update_volume_container()
        print("\n[+] WebScraper Chrome driver initialized")

    def _update_volume_container(self, page_index: int = 1):
        if page_index < 1:
            raise ValueError("Pages indexing starts from 1")

        target_url = self.URL + "?tab=chapters&page={}".format(page_index)

        if self.driver.current_url != target_url:
            self.driver.get(target_url)
            
        self.volume_container = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, VOLUME_CONTAINER)))
        sleep(0.35)

    def _get_page_number(self):
        divs = self.volume_container.find_elements(By.XPATH, "./div")

        page_div = self.volume_container.find_element(By.XPATH, PAGES.format(len(divs)))

        try:
            last_button = page_div.find_element(By.XPATH, LAST_BUTTON)
            text = last_button.text.strip()
            to_int = int(text)
        except:
            last_button = page_div.find_element(By.XPATH, LAST_BUTTON_FIX)
            text = last_button.text.strip()
            to_int = int(text)

        print("\n[+] Found {} page(s) to scrape".format(to_int))
        return to_int

    def _get_manga_name(self):
        if self.URL not in self.driver.current_url:
            raise ValueError("You must be on the manga page to get info")

        manga_name = self.driver.find_element(By.XPATH, MANGA_NAME).text.strip()
        return manga_name

    def _get_artist(self):
        if self.URL not in self.driver.current_url:
            raise ValueError("You must be on the manga page to get info")

        artist = self.driver.find_element(By.XPATH, ARTIST).text.strip()
        return artist

    def _get_volumes_in_page(self, page_index: int):
        if page_index < 1:
            raise ValueError("Pages indexing starts from 1")

        self._update_volume_container(page_index)

        divs = self.volume_container.find_elements(By.XPATH, "./div")

        print("\n[+] Volumes in Page {}: {}".format(page_index, len(divs) - 2))
        return len(divs) - 2

    def _get_chapters_in_volume(self, volume_index: int):
        self.chapters_container = self.volume_container.find_element(By.XPATH, CHAPTERS.format(2 + volume_index))
        chapters = self.chapters_container.find_elements(By.XPATH, "./div")

        volume_number = self.volume_container.find_element(By.XPATH, CHAPTERS_VOLUME_NUMBER.format(2 + volume_index)).text.strip().split("Volume ")[-1]

        print("\n[+] Chapters in Vol. {}: {}".format(volume_number, len(chapters)))
        return len(chapters)

    def _check_chapter_number(self, chapter_number: int):
        if self.chapters:
            start = self.chapters[0]
            if self.chapters[1] == '*':
                end = chapter_number
            elif self.chapters[1] == '!':
                end = start
            else:
                end = self.chapters[1]

            if not (chapter_number >= start and chapter_number <= end):
                self.stop = chapter_number > end
                return False

        return True

    def _get_chapter_localized(self, chapter_index: int):
        if chapter_index < 1:
            raise ValueError("Chapter indexing starts from 1")

        single_locale = False

        try:
            chapter_number = self.chapters_container.find_element(By.XPATH, LOCALES_TITLE.format(chapter_index))
            try:
                chapter_number = int(chapter_number.text.strip().split()[-1])
            except ValueError:
                chapter_number = float(chapter_number.text.strip().split()[-1])

            if not self._check_chapter_number(chapter_number):
                print("[-] Skipping Chapter {} because is not in the range".format(chapter_number))
                return None, None, None

        except:
            single_locale = True

        if not single_locale:
            locales_container = self.chapters_container.find_element(By.XPATH, LOCALES_CONTAINER.format(chapter_index))
            locales = locales_container.find_elements(By.XPATH, "./div")
        else:
            locale_div = self.chapters_container.find_element(By.XPATH, LOCALE_SINGLE.format(chapter_index))
            locales = [1]   
            
        for locale in range(1, len(locales) + 1):
            if not single_locale:
                locale_div = locales_container.find_element(By.XPATH, LOCALE_ITERATOR.format(locale))
            else:
                locale_info = locale_div.find_element(By.XPATH, CHAPTER_URL)

                try:
                    chapter_number = int(locale_info.get_attribute("title").split(" - ")[0].split("Ch. ")[-1])
                except ValueError:
                    chapter_number = float(locale_info.get_attribute("title").split(" - ")[0].split("Ch. ")[-1])

                if not self._check_chapter_number(chapter_number):
                    print("[-] Skipping Chapter {} because is not in the range".format(chapter_number))
                    return None, None, None

            locale_image = locale_div.find_element(By.XPATH, CHAPTER_LOCALE)
            locale_alt = locale_image.get_attribute("alt")

            if self.language in locale_alt:
                locale_info = locale_div.find_element(By.XPATH, CHAPTER_URL)
                locale_url = locale_info.get_attribute("href")
                locale_title = locale_info.get_attribute("title")

                print("[+] Found {} version for Chapter {} (Title: \"{}\")".format(self.language, chapter_number, locale_title))
                return chapter_number, locale_title, locale_url
        else:
            print("[-] Could not find {} version for Chapter {}".format(self.language, chapter_number))
            return None, None, None

    def get_manga_info(self):
        manga_name = self._get_manga_name()
        artist = self._get_artist()

        return manga_name, artist

    def scrape(self):
        page_number = self._get_page_number() 

        urls = {}

        for page in reversed(range(1, page_number + 1)):
            self._update_volume_container(page)
            volumes = self._get_volumes_in_page(page)

            for volume in reversed(range(volumes)):
                chapters = self._get_chapters_in_volume(volume)

                for chapter in reversed(range(1, chapters + 1)):
                    chapter_number, title, url = self._get_chapter_localized(chapter)  

                    urls[chapter_number] = {
                        "title": title,
                        "url": url
                    }  

                    if self.stop:
                        print("\n[-] Range satisfied, stopping")
                        del urls[None]
                        return urls

        del urls[None]
        return urls