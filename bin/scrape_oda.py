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
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--host", help="Hostname to start crawling", default="https://oda.com")
    arg_parser.add_argument("--max-bw", help="Maximum bandwidth byte/s - 0 : unlimited", default=0, type=int)
    arg_parser.add_argument("--fmt", help="Output format txt|json", default="txt")
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
