MANGA_NAME = "/html/body/div/div[1]/div/div[2]/div[2]/div/div[1]/div[3]/p"
ARTIST = "/html/body/div/div[1]/div/div[2]/div[2]/div/div[1]/div[3]/div[3]"

VOLUME_CONTAINER = "/html/body/div/div[1]/div/div[2]/div[2]/div/div[1]/div[8]/div[2]/div[2]/div"

# ALL OF THE FOLLOWING XPATHS ARE TO BE USED AFTER THE VOLUME CONTAINER XPATH

# Must always start from 2 (indicates the volume) 
# This XPath is used to get the container of the chapters of the volume
CHAPTERS_VOLUME_NUMBER = "./div[{}]/div[1]/div[1]"
CHAPTERS = "./div[{}]/div[2]"
CHAPTERS_FULL = VOLUME_CONTAINER + CHAPTERS[1:]
CHAPTERS_VOLUME_NUMBER_FULL = VOLUME_CONTAINER + CHAPTERS_VOLUME_NUMBER[1:]

# To be used after CHAPTERS, gets all locales for specified chapter index\
LOCALE_SINGLE = "./div[{}]/div/div/div/div[1]"
LOCALES_CONTAINER = "./div[{}]/div[2]"
LOCALES_TITLE = "./div[{}]/div[1]/span"

LOCALE_SINGLE_FULL = CHAPTERS_FULL + LOCALE_SINGLE[1:]
LOCALES_CONTAINER_FULL = CHAPTERS_FULL + LOCALES_CONTAINER[1:]
LOCALES_TITLE_FULL = CHAPTERS_FULL + LOCALES_TITLE[1:]

# To be used after LOCALES_CONTAINER, gets specified locale div
LOCALE_ITERATOR = "./div[{}]/div[2]/div[1]"
LOCALE_ITERATOR_FULL = LOCALES_CONTAINER_FULL + LOCALE_ITERATOR[1:]

# Use CHAPTER_LOCALE by looking up the alt attribute of the image
# Use CHAPTER_URL to get the href attribute of the locale you want
# Both XPaths are used after using LOCALE_ITERATOR
CHAPTER_LOCALE = "./img"
CHAPTER_URL = "./a"

# After getting all the divs with VOLUME_CONTAINER XPath,
# get the length of the list and use it for formatting the PAGES XPath
# e.g. PAGES.format(len(volume_container_divs))
# Look up the text of the element found to get page number
PAGES = "./div[{}]"
LAST_BUTTON = "./a[5]/span" # If you find an svg tag with this xpath, you should use LAST_BUTTON_FIX
LAST_BUTTON_FIX = "./a[4]/span"

PAGES_FULL = VOLUME_CONTAINER + PAGES[1:]
LAST_BUTTON_FULL = PAGES_FULL + LAST_BUTTON[1:]
LAST_BUTTON_FIX_FULL = PAGES_FULL + LAST_BUTTON_FIX[1:]

READER_PAGES_COUNT = "/html/body/div/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]"
READER_IMAGE = "/html/body/div/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/img[{}]"