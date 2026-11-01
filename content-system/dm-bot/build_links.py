#!/usr/bin/env python3
"""Build the DM links for every product in products.csv.

For each row it prints two links:
  - product page link (shows reviews and variants)
  - one-tap checkout link (Shopify cart permalink, goes straight to checkout)
Both carry UTMs, so Shopify can attribute the sale to the platform and campaign.

Usage:
  python3 build_links.py --platform instagram --campaign q4-w1 [--discount TTBF15]
"""
import argparse, csv, pathlib
from urllib.parse import urlencode

STORE = "https://www.luckybarista.com"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--platform", required=True, choices=["instagram", "facebook", "tiktok"])
    p.add_argument("--campaign", required=True, help="e.g. q4-w1-foam")
    p.add_argument("--discount", default="", help="optional Shopify discount code to auto-apply")
    p.add_argument("--csv", default=str(pathlib.Path(__file__).with_name("products.csv")))
    a = p.parse_args()

    with open(a.csv, newline="") as f:
        rows = list(csv.DictReader(f))

    out = csv.writer(open(1, "w", closefd=False))
    out.writerow(["keyword", "variant", "product_link", "checkout_link"])
    for r in rows:
        utm = {
            "utm_source": a.platform,
            "utm_medium": "dm",
            "utm_campaign": a.campaign,
            "utm_content": r["keyword"].lower(),
        }
        product_q = dict(utm, variant=r["variant_id"])
        checkout_q = dict(utm)
        if a.discount:
            checkout_q = {"discount": a.discount, **checkout_q}
        product_link = f"{STORE}/products/{r['handle']}?{urlencode(product_q)}"
        checkout_link = f"{STORE}/cart/{r['variant_id']}:1?{urlencode(checkout_q)}"
        out.writerow([r["keyword"], r["variant_label"], product_link, checkout_link])

if __name__ == "__main__":
    main()
