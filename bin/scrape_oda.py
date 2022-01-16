#!/usr/bin/env python3
import sys
from argparse import ArgumentParser

from scraper import OdaScraper


def run_main(argv):
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--host", help="Hostname to start crawling - default", default="https://oda.com")

    args = arg_parser.parse_args(argv[1:])

    throttle = Throttle(max_bandwidth)
    fetcher = Fetcher(args.host, throttle)

    os = OdaScraper(fetcher)
    pc = os.run()

    with open("dump.txt", "w") as fh:
        fh.write(pc.dump())


if __name__ == "__main__":
    run_main(sys.argv)
