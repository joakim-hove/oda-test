#!/usr/bin/env python3

from scraper import OdaScraper

if __name__ == "__main__":

    os = OdaScraper()
    pc = os.run()

    with open("dump.txt", "w") as fh:
        fh.write(pc.dump())
