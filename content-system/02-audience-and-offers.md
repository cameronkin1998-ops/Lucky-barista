# 2 · Audience & Offers: the impulse-product model

**Structure:** one simple product per post, one keyword per product, and the DM bot sends the buy link ([dm-bot/](dm-bot/)). Organic content sells **impulse-priced items** that someone decides on in under 10 seconds, with no research needed. Espresso machines are not the organic focus. They get sold through DM conversations and the "ask me" fallback.

## What makes a product impulse-buyable

| Test | Pass if… |
| --- | --- |
| Price | **$20–$60** (sweet spot $25–$50). Below the "I need to think about it" line. |
| Explainable in 3 seconds | The video shows the whole value without words (foam forming, a mug stirring itself) |
| Visual payoff | Something satisfying happens on camera |
| Giftable | Works as a stocking stuffer or Secret Santa gift with no sizing or compatibility worries |
| Single variant (or 2 max) | Lets you send a one-tap checkout link with no choices to make |
| Price check | Within reach of comparable Amazon listings. Impulse buyers check. |
| Ships now | In stock and fulfilled within 2–3 days |

## The impulse lineup (from the live catalog, 2026-11-01)

| Keyword | Product | Price | In stock | Fit | Why / watch-outs |
| --- | --- | --- | --- | --- | --- |
| **FOAM** | Subminimal NanoFoamer V2 | $59.95 | 7 (standard) | ⭐ A | Proven best seller (7 orders). Very visual. Top of the price band. |
| **SHOT** | Subminimal UpShot shot mirror | $34.95 | 10 | ⭐ A | Most impulse-friendly price. "See inside your shot" hook. Needs a bottomless portafilter, so say so. |
| **FLICK** | Subminimal Flick WDT | $49.95 | 10 | ⭐ A | Satisfying retractable-needle click. For home-barista viewers. |
| **FROTH** | HiBrew M3A 4-in-1 milk foamer | $49.90 | 10 | ⭐ A | Hot and cold foam at the push of a button. Broad appeal (not just espresso people). Gift under $50. |
| **MUG** | Auto-Stir Mug | $49.95 | ✔ (dropship) | B | Very filmable. **$49.95 is well above typical self-stirring mug prices.** Price-test it (see below) before pushing it hard. |
| **TEMP** | Subminimal contactless thermometer | $49.95 | 10 | B | Better as a FOAM add-on than as a standalone post |
| **SCREEN** | NanoScreen Kit | $20 | 19 | Add-on | Upsell in the FOAM follow-up DM |
| *(waitlist)* | Digital scale with timer | $34.95 | draft | A once stocked | Perfect impulse item. Turn it on as soon as stock lands (Nov 24). |
| *(not for impulse)* | Whisk 3-in-1 frother | $55.48 | ✔ | C | Too expensive for a handheld whisk. Reprice it (around $19.99–$24.99) or leave it out. |
| *(not for impulse)* | Heated smart mug | $89.95 | draft | — | Above the impulse band. Treat it as a gift item with a waitlist. |

**Product rotation:** feature **one product per post** and **2 products per week** max, so the same keyword repeats across 3–4 posts and the audience learns it. Suggested order: Weeks 1–2 FOAM + FROTH → Week 3 SHOT + MUG (after the price test) → Weeks 4–5 BFCM: the best 2 performers plus the scale → December: the best performers on gift framing.

## Pricing for impulse (Cameron to fill in costs)

I don't have your landed costs, so these are rules to apply rather than final prices:

| Rule | Detail |
| --- | --- |
| Margin floor | Price ≥ landed cost (product + shipping + fees) × 2.5. Impulse items need room for ads and a BFCM discount. |
| Charm pricing | End in .95 / .99, and stay under a round number ($29.99, not $31). |
| Free-shipping threshold | Set it just above one item (for example, free shipping over $45), so a single impulse buy qualifies or an add-on gets them there |
| Anchor | Show the comparison in the DM: "café latte $6.50 a day vs a foamer once" |
| Price test (MUG, WHISK) | Run 2 weeks at a lower price. Compare DM-to-order conversion against FOAM. Keep the price that earns more profit per DM. |

## Offers (all delivered by the DM bot)

| Offer | Mechanic | When |
| --- | --- | --- |
| **DM-only price** | Discount code auto-applied in the checkout link (`--discount` in `build_links.py`): "10% off because you asked" | Testing weeks. A reason to comment now. |
| **Bundle in the follow-up** | FOAM + SCREEN, FOAM + TEMP, FROTH + a second unit for a gift | Message B, all season |
| **BFCM** | DM-list early access Nov 24, sitewide offer Nov 27–30 | Weeks 4–5 |
| **"Order by" urgency** | Shipping-cutoff line added to every DM | Dec 8 – cutoff |
| **Gift card** | Instant digital card | After the cutoff |

## Who we're talking to

| Persona | Hook that works on them | Platform |
| --- | --- | --- |
| **Gift buyer** | "The gift for the coffee person, under $50" | FB, IG |
| **Café-latte habit** | "Stop paying $6.50 for this" | TikTok, IG |
| **Home-barista upgrader** | "Your shot is channeling and you can't see it" | TikTok, IG |
| **Self-gifter** | "My $35 coffee-corner upgrade" | All |

Higher-ticket buyers (machines, $269–$559) still come in through DMs ("MACHINE: tell me your budget") and get a personal answer from Cameron.
