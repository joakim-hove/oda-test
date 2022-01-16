import sys
import json
from argparse import ArgumentParser

from scraper import OdaScraper, Throttle, Fetcher


def run_main(argv):
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--host", help="Hostname to start crawling", default="https://oda.com")
    arg_parser.add_argument("--max-bw", help="Maximum bandwidth byte/s - 0 : unlimited", default=0, type=int)
    arg_parser.add_argument("--fmt", help="Output format txt|json", default="txt")

    args = arg_parser.parse_args(argv[1:])

    throttle = Throttle(args.max_bw)
    fetcher = Fetcher(args.host, throttle)

    os = OdaScraper(fetcher)
    pc = os.run()

    if args.fmt == "txt":
        with open("dump.txt", "w") as fh:
            fh.write(pc.dump())
    elif args.fmt == "json":
        with open("dump.json", "w") as fh:
            fh.write(json.dumps(pc.data()))



if __name__ == "__main__":
    run_main(sys.argv)
