# 1 · Baseline & Goals

## Baseline (pulled from Shopify on 2026-11-01)

**Traffic, last 90 days, by referrer**

| Source | Sessions | Added to cart | Checkouts |
| --- | --- | --- | --- |
| Direct | 363 | 10 | 0 |
| Search | 81 | 1 | 1 |
| Social | 6 | 1 | 0 |
| Other | 9 | 1 | 0 |

**Sales, last 12 months: $1,790 gross across 18 orders**

| Product | Orders | Gross |
| --- | --- | --- |
| Subminimal NanoFoamer V2 | 7 | $499.65 |
| HiBrew H13 Dual Boiler | 1 | $389.00 |
| HiBrew H2B 5-in-1 capsule | 3 | $359.70 |
| Subminimal FlowTip jug | 3 | $192.00 |
| HiBrew H1B 6-in-1 capsule | 1 | $139.90 |
| HiBrew H4A portable | 1 | $109.90 |
| Subminimal Subscale | 1 | $79.99 |
| NanoScreen Kit | 1 | $20.00 |

**What the numbers say**
- People who have bought from us bought **accessories and machines under $400**. The $1,000–$14,000 commercial catalog has never sold online. Organic social shouldn't push it.
- Milk drinks are where we're strongest (NanoFoamer, FlowTip). That ties straight into latte-art UGC, which already performs well on all three platforms.
- 363 direct sessions with 0 checkouts means there's interest the store isn't converting. The fixes are product pages, gift framing and trust (component 8).
- Shopify sales channels for **TikTok, Facebook (covers Instagram), Pinterest and Google** are already connected. Product tagging is available on all of them.

## Q4 goals (Nov 2 – Jan 10)

These are deliberately reachable from a near-zero start. Review them on Dec 1 and raise them if we're ahead.

| Stage | Metric | Weekly target by Dec 1 | Season target |
| --- | --- | --- | --- |
| See | Combined views (TT + IG + FB) | 25,000/wk | 300,000 |
| Care | Saves + shares | 300/wk | 3,000 |
| Click | Store sessions from social (UTM-tagged) | 150/wk | 1,500 |
| Capture | New email/SMS subscribers | 40/wk | 400 |
| Buy | Orders attributed to social | 5/wk | 50 orders, about $5,000 |
| Proof | UGC pieces received (creators + customers) | 6/wk | 60 |

**North-star metric: social-attributed revenue per week.** Every other metric is there to explain this one.

## How to re-pull the baseline (every Friday)

Paste these into Shopify Analytics → Reports, or ask Claude to run them:

```
FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_completed_checkout GROUP BY referrer_source SINCE -7d UNTIL today
FROM sessions SHOW sessions WHERE referrer_source = 'social' GROUP BY referrer_name SINCE -7d UNTIL today
FROM sales SHOW orders, total_sales GROUP BY order_referrer_source, order_referrer_name SINCE -7d UNTIL today
FROM sales SHOW orders, gross_sales GROUP BY product_title ORDER BY gross_sales DESC SINCE -7d UNTIL today LIMIT 10
```
