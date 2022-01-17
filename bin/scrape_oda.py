import sys
import json
from argparse import ArgumentParser

from scraper import OdaScraper, Throttle, Fetcher

def dump_result(ofile, out_string):
    if ofile:
        fh = open(ofile, "w")
    else:
        fh = sys.stdout
    fh.write(out_string)



def run_main(argv):
    default_host   = "https://oda.com"
    default_fmt    = "txt"
    default_max_bw = 0

    arg_parser = ArgumentParser("Application to fetch the complete productcatalog from Oda by scraping html\n")
    arg_parser.add_argument("--host", help=f"Hostname to start crawling - default={default_host}", default=default_host)
    arg_parser.add_argument("--max-bw", help=f"Maximum bandwidth byte/s - default={default_max_bw} 0:unlimited", default=default_max_bw, type=int)
    arg_parser.add_argument("--fmt", help=f"Output format txt|json default={default_fmt}", default=default_fmt)
    arg_parser.add_argument("--outfile", help="Name of output file - default is stdout")

    args = arg_parser.parse_args(argv[1:])

    throttle = Throttle(args.max_bw)
    fetcher = Fetcher(args.host, throttle)

    os = OdaScraper(fetcher)
    pc = os.run()


    if args.fmt == "txt":
        out_string = pc.dump()
    elif args.fmt == "json":
        out_string = json.dumps(pc.data())

    dump_result(args.outfile, out_string)

if __name__ == "__main__":
    run_main(sys.argv)
