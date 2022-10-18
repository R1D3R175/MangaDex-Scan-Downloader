import parser
from webscraper import WebScraper
from imagescraper import Downloader

def pad(*lists, padding=None):
    max_length = max(len(l) for l in lists)
    return [l + [padding] * (max_length - len(l)) for l in lists]

if __name__ == "__main__":
    argparser = parser.create_parser()
    args = argparser.parse_args('-u https://mangadex.org/title/259dfd8a-f06a-4825-8fa6-a2dcd7274230/yofukashi-no-uta?tab=chapters&page=6 -c 1 -d ./test'.split())

    urls = args.urls
    chapters = args.chapters

    if len(chapters) > len(urls):
        raise ValueError("Chapters range must be less or equal to the URL(s) provided")

    urls, chapters = pad(urls, chapters, padding=[])

    schema = {}

    for url, chapter in zip(urls, chapters):
        scraper = WebScraper(url, args.language, chapter)
        schema = schema | scraper.scrape()

    if not schema:
        raise ValueError("Could not find any chapter for the provided URL(s)")

    manga_name, artist = scraper.get_manga_info()

    downloader = Downloader(manga_name, artist, schema, args.directory)
    downloader.download()