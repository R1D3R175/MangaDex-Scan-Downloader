import argparse
from uuid import UUID

def range_parse(argument):
    try:
        if "-" in argument:
            args = argument.split("-")
            if len(args) == 1:
                if argument[0] == "-": 
                    start = 1
                    end = args[0]
                elif argument[-1] == "-": 
                    start = args[0]
                    return [ start, '*' ]
            elif len(args) == 2:
                start = args[0]
                end = args[1]

                if start > end:
                    raise ValueError()
            else:
                raise ValueError()

            return [ start, end ]
        else:
            return [int(argument), "!"]
    except:
        raise argparse.ArgumentTypeError("Invalid range. Expected formats are \"<start>-<end>\" or \"<start>\" where <start> and <end> are positive integers and 1 <= <start> <= <end>")

def mangadex_url(argument: str):
    if argument.startswith("https://mangadex.org/title/"):
        uuid = argument.split("https://mangadex.org/title/")[1].split("/")[0]
        try:
            uuid_tester = UUID(uuid, version=4)
        except ValueError:
            pass

        if str(uuid_tester) == uuid:
            if "?" in argument:
                argument = argument.split("?")[0]

            return argument


    raise argparse.ArgumentTypeError("Invalid URL. Expected format is \"https://mangadex.org/title/<uuid>/<name>\"")

def create_parser():
    parser = argparse.ArgumentParser(description='MangaDex Web-scraper and Image Downloader', epilog="Enjoy! Brought to you by Ben (aka. R1D3R)")
    
    # -u or --urls, a list of urls to scrape
    parser.add_argument(
        '-u', '--urls',
        action='extend',
        default=[],
        help='URL(s) to scrape and download',
        nargs='+',
        metavar='URL',
        type=mangadex_url,
        required=True
    )

    # -d or --directory, the directory where the manga will be saved
    parser.add_argument(
        '-d', '--directory',
        action='store',
        default='.',
        help='Directory to save the manga',
        nargs='?',
        metavar='DIRECTORY',
        type=str,
        required=False
    )

    # -l or --language, the locale to download
    parser.add_argument(
        '-l', '--language',
        action='store',
        default='English',
        help='Locale to download',
        nargs='?',
        metavar='LANG',
        type=str,
        required=False
    )

    # -c or --chapters, a list of ranges of chapters to download
    parser.add_argument(
        '-c', '--chapters',
        action='extend',
        default=[],
        help='Chapter(s) to download for each URL (e.g. 1-3, 5, 7-, -9)',
        nargs='+',
        metavar='X-Y',
        type=range_parse,
        required=False
    )

    return parser