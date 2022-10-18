import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from xpaths import READER_IMAGE, READER_PAGES_COUNT

class Downloader:
    def __init__(self, manga_name: str, artist: str, schema: dict, directory: str):
        self.manga_name = manga_name
        self.artist = artist
        self.schema = schema
        self.directory = directory

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--log-level=3") # FATAL
        options.add_argument("--disable-gpu")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--window-size=3840,2160")

        service = Service(r"/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=options)

        print("\n[+] Downloader Chrome driver initialized")

    def _create_folders(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        if not os.path.exists(f"{self.directory}/{self.manga_name} - {self.artist}"):
            os.makedirs(f"{self.directory}/{self.manga_name} - {self.artist}")

        os.chdir(f"{self.directory}/{self.manga_name} - {self.artist}")

        print("[+] Folders created")

    def _get_pages_count(self):
        pages_message = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, READER_PAGES_COUNT)))
        WebDriverWait(self.driver, 10).until_not(EC.text_to_be_present_in_element((By.XPATH, READER_PAGES_COUNT), "?"))
        pages_count = int(pages_message.text.strip().split(" / ")[-1])

        return pages_count

    def download(self):
        self._create_folders()

        root = self.driver.find_element(By.TAG_NAME, "html")

        root.click()
        root.send_keys(Keys.ARROW_RIGHT)
        root.send_keys(Keys.ARROW_LEFT)

        for chapter in self.schema:
            if not os.path.exists(f"Ch. {chapter} - {self.schema[chapter]['title']}"):
                os.makedirs(f"Ch. {chapter} - {self.schema[chapter]['title']}")

            self.driver.get(self.schema[chapter]['url'])
            pages_count = self._get_pages_count()
            print("\n[+] Starting to download {} pages of Ch. {} ({})".format(pages_count, chapter, self.schema[chapter]['title']))

            for page in range(1, pages_count + 1):
                scan = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, READER_IMAGE.format(page))))

                with open(f"Ch. {chapter} - {self.schema[chapter]['title']}/{page}.png", "wb") as image:
                    sleep(0.05)
                    image.write(scan.screenshot_as_png)
                    print("[+] Page {}/{} downloaded".format(page, pages_count))

                root = self.driver.find_element(By.TAG_NAME, "html")
                root.send_keys(Keys.ARROW_RIGHT)
