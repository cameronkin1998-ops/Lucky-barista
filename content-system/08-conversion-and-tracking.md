# 8 · Conversion & Tracking

Social sent 6 sessions in 90 days. This component makes sure every view has a path to checkout, and that every sale can be traced back to the post that drove it.

## The path from post to purchase

```
Post (one product) ─┬─ IG/FB: "Comment FOAM" → ManyChat bot DM → one-tap checkout link ──→ Shop Pay → Order   ← MAIN PATH
                    ├─ TikTok: product tag (orange cart) ───────────────────────────→ Product page → Checkout
                    ├─ TikTok: "DM FOAM" → keyword auto-reply → checkout link ──────→ Shop Pay
                    ├─ Story link sticker → product page
                    └─ Bio link → this week's main product (swap every Monday)
                                       ↘ not ready → bot asks for email → BFCM early access / abandoned-interest email
```

## 1. The DM bot is the main conversion path

Full build: [dm-bot/README.md](dm-bot/README.md). Links come from [`dm-bot/build_links.py`](dm-bot/build_links.py): a product page link and a one-tap checkout link (`/cart/<variant_id>:1`) for each keyword, with `utm_medium=dm`. Tested on 2026-11-01: it redirects straight to Shop Pay.

**Bio link:** points to the week's main product page (with `utm_medium=bio`). If you want more than one link, Instagram allows up to 5 bio links. Keep #1 as the main product, so the bot handles everything else.

## 2. UTM convention (required on every link)

```
?utm_source=<tiktok|instagram|facebook|pinterest>
&utm_medium=<organic|paid|creator|dm|story|bio>
&utm_campaign=q4-<week#>-<theme>        e.g. q4-w3-giftguide
&utm_content=<product-slug>-<format#>   e.g. nanofoamer-f2
```
Keep a running list of every link in the scorecard so each post's result can be traced. Use Shopify's built-in UTM reports (Marketing → Attribution).

## 3. Platform discount codes (so attribution works without UTMs too)

`TIKTOK10`, `INSTA10`, `FB10` (or the BFCM equivalents, such as `TTBF15`), plus one code per creator (for example, `JESS10`). The store has used `IG-EMAIL-` and `FB-EMAIL-` codes before, and all of them are now expired. Reuse that pattern for the email-capture welcome codes.

## 4. Product page fixes before pushing traffic (Week 1)

- [ ] Hero image plus a **UGC video** at the top of the gallery for each Tier A product.
- [ ] Rewrite descriptions to lead with the benefit ("Café microfoam in 20 seconds") and cut the "Description Description" duplicate text that's currently on the HiBrew listings.
- [ ] Add a gift note or "Gift-ready" badge, delivery-date messaging and a returns line.
- [ ] Turn on product reviews (Shopify Product Reviews / Judge.me). Ask past buyers for reviews (18 orders so far).
- [ ] Bundles shown as "Complete the set" upsells on foamer and machine pages.
- [ ] Mobile check: price, ATC button and shipping info all visible above the fold.
- [ ] Hide or unpublish draft and commercial products from the gift collections and the Facebook/TikTok catalogs.

## 5. Capture (for people who aren't ready to buy)

- Email/SMS pop-up: "Get early Black Friday access + 10% off your first order" (Shopify Forms).
- Waitlist forms for Tier C (heated mug, scale).
- Automations (Shopify Email or Klaviyo): welcome series (3 emails), **abandoned cart** (1 h, 24 h), browse abandonment, post-purchase review-and-UGC ask (day 10).

## 6. Pixels and catalog sync

- [ ] Meta pixel plus Conversions API through the Facebook & Instagram channel: confirm events are firing (ViewContent, AddToCart, Purchase).
- [ ] TikTok pixel through the TikTok channel: same three events.
- [ ] Pinterest tag through the Pinterest channel.
- [ ] Catalogs only contain active, in-stock products, with correct prices.
