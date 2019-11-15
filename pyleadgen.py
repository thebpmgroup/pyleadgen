import argparse
from webdirectory import WebDirectory
from yelp import Yelp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python lead generator")
    parser.add_argument("--url", help="Url of the web directory to crawl")
    parser.add_argument("--searchterm", help="What to search for, e.g. accountants")
    parser.add_argument("--location", help="Where to search for the search term, e.g. London")
    parser.add_argument("--maxhits", help="The maximum number of hits to return")
    parser.add_argument("--stealth-level", help="The amount of time to pause between each scrape, in seconds")

    args = parser.parse_args()

    wd = WebDirectory

    if "YELP" in args.url.upper():
        print("Using yelp")
        wd=Yelp()
    elif "GOOGLE" in args.url.upper():
        print("Google is not implemented at this time")
    else:
        print("That url is not supported")

    wd.url = args.url
    wd.searchterm = args.searchterm
    wd.location = args.location
    wd.maxhits = args.maxhits
    wd.stealth_level = args.stealth_level or 0

    print(type(wd))
    wd.run()