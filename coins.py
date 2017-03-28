import argparse
import time
import random
from urllib.parse import urlparse, parse_qs
from itertools import chain
import multiprocessing as mp

import requests
from bs4 import BeautifulSoup

from config import CATEGORY_URL, PROCESS_WORKERS
from models import db, Lot


def get_lots(soup):
    elements = soup.select("a.description-title-link")
    return (
        {
            "a_id": int(el["id"]),
            "title": el.string.strip(),
        }
        for el in elements
    )


def get_pages_count(soup):
    # getting last page link
    last_page_element = soup.select("a.pagination-page")[-1]
    href = last_page_element["href"]
    # getting its address, parsing query string, then getting p (page) param
    last_page_number = parse_qs(urlparse(href).query)["p"][0]
    return int(last_page_number)


def get_page(url, page=None, referer=None):
    return requests.get(
        url,
        {"view": "list", "page": page},
        headers={"Referer": referer},
        allow_redirects=False
    )


def parse_page(text):
    return BeautifulSoup(text, "html.parser")


def iterpages(count):
    return chain(
        range(2, 101),
        range(count - 100, count + 1)
    )


def process_lot(lot):
    if lot.description is None:
        lot.get_description()
        time.sleep(random.uniform(0, 2))
    lot.guess_year()
    print("Updated lot {} with year {}.".format(lot.a_id, lot.year))
    return lot


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch coins for sale from some Russian classified website"
        " and try to guess their minting year using title and description."
    )

    parser.add_argument(
        "--continue", action='store_true',
        help="Don't fetch coins list, just continue to fetch their"
        " descriptions and try to guess years."
    )

    args = parser.parse_args()

    db.connect()
    db.create_tables((Lot, ), safe=True)

    if not vars(args)["continue"]:
        resp = get_page(CATEGORY_URL)
        first_page_soup = parse_page(resp.text)

        pages_count = get_pages_count(first_page_soup)
        lots = get_lots(first_page_soup)

        for page in iterpages(pages_count):
            referer = resp.request.url
            resp = get_page(CATEGORY_URL, page, referer)

            if resp.status_code != 200:
                continue

            soup = parse_page(resp.text)
            lots_dict = get_lots(soup)

            with db.atomic():
                for lot in lots_dict:
                    Lot.get_or_create(
                        defaults=lot, a_id=lot["a_id"]
                    )

            print("Parsed page {}".format(page))
            time.sleep(random.uniform(1, 3))

    lots = Lot.select().where(
        Lot.description.is_null() | Lot.year.is_null()
    )

    p = mp.Pool(PROCESS_WORKERS)

    updated_lots = p.map(process_lot, list(lots))

    with db.atomic():
        for lot in updated_lots:
            lot.save()

    total_count = Lot.select().count()
    with_year_count = Lot.select().where(Lot.year != 0).count()
    pre_2000_count = Lot.select().where(Lot.year < 2000).count()

    print("Total count: {}".format(total_count))
    if total_count > 0:
        print(
            "With year: {with_year} ({percentage:.2f}% of all)".format(
                with_year=with_year_count,
                percentage=(100 * with_year_count / total_count)
            )
        )
        print(
            "Pre-2000: {pre_2000} ({percentage:.2f}% of all"
            " with year)".format(
                pre_2000=pre_2000_count,
                percentage=(100 * pre_2000_count / total_count)
            )
        )
