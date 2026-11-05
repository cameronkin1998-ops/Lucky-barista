# Lucky Barista — Social Content Marketing System (Q4 2026)

The operating system for turning Instagram, Facebook and TikTok content into sales on luckybarista.com.

**The model in one line:** UGC video of **one impulse-priced product** → "Comment **FOAM** and I'll DM you the link" → **a bot DMs a one-tap checkout link** → order → follow-up and UGC ask.

Owner: Cameron · Season: Nov 2 2026 – Jan 10 2027 · Last updated: 2026-11-01

## Why this structure

| Fact (Shopify, last 90 days) | What it means |
| --- | --- |
| 6 sessions and 0 orders from social | Social isn't sending buyers yet. The path from post to checkout has to be built. |
| Best seller: NanoFoamer V2 ($59.95, 7 orders), and every sale was under $400 | Low-priced, visual accessories sell. They're the organic focus. |
| A bio only holds one link | Every post gets its **own keyword**, and the bot sends **that post's link** in a DM. The bio stops being the bottleneck. |
| TikTok, Facebook/IG, Pinterest and Google sales channels are already connected | Product tags and catalog ads are ready to use |

## The components

| # | Component | Question it answers | File |
| --- | --- | --- | --- |
| 1 | Baseline & goals | Where are we and what does "working" mean? | [01](01-baseline-and-goals.md) |
| 2 | Impulse products & offers | Which product, at what price, with what offer? | [02](02-audience-and-offers.md) |
| 3 | UGC style standard | What does a Lucky Barista post look and sound like? | [03](03-ugc-style-standard.md) + [style-references/](style-references/) |
| 4 | Content pillars & formats | What mix of posts, in what shapes? | [04](04-content-pillars-and-formats.md) |
| 5 | Platform playbooks | How does each post get adapted for IG, FB and TikTok? | [05](05-platform-playbooks.md) |
| 6 | Q4 holiday calendar | What goes out each week until January? | [06](06-q4-holiday-calendar.md) |
| 7 | Production workflow | How does an idea become a post (creators, AI, QA)? | [07](07-production-workflow.md) |
| **8** | **DM link bot** ⭐ | **How does "I want it" become a link in their DMs, automatically?** | **[dm-bot/](dm-bot/)** |
| 9 | Conversion & tracking | How does a click become an order, and how do we know? | [08](08-conversion-and-tracking.md) |
| 10 | Community & engagement | What happens after we post? | [09](09-community-and-engagement.md) |
| 11 | Paid amplification | Which posts get money behind them? | [10](10-paid-amplification.md) |
| 12 | Measurement & decisions | What do we track, and what do the numbers tell us to do? | [11](11-measurement.md) |
| 13 | Guardrails | What do we never do? | [12](12-guardrails.md) |
| **14** | **Autonomous pipeline** | **How does content get reviewed, posted and measured without Cameron?** | **[autonomy/](autonomy/README.md)** |

Working files: [`templates/`](templates/) (UGC brief, creator outreach, caption formulas, weekly scorecard) · [`dm-bot/products.csv`](dm-bot/products.csv) (keyword → product → variant ID) · [`dm-bot/build_links.py`](dm-bot/build_links.py) (generates UTM-tagged product and one-tap checkout links).

## The loop every post runs

```
1 PRODUCT    →  2 UGC POST           →  3 KEYWORD CTA          →  4 BOT DM             →  5 ORDER        →  6 COME BACK
impulse item    hook in 1 s, real       "Comment FOAM ☕"          public reply +          Shop Pay          follow-up DM, email,
$20–$60         hands, real sound       TikTok: "tap the cart     one-tap checkout        1 tap             day-10 UGC ask,
                                        or DM FOAM"               link, CRM tag                             retargeting
```

## Launch order (this week)

1. **Mon–Tue Nov 2–3:** build the DM bot in ManyChat (dm-bot/README.md Steps 0–3) and run the launch test.
2. **Tue Nov 3:** set up TikTok product tags and keyword replies (Step 4). Decide on MUG and WHISK pricing (component 2).
3. **Wed Nov 4:** first FOAM post on all three platforms with "Comment FOAM".
4. **This week:** add your style examples to `style-references/`. Recruit 5–10 UGC creators (component 7). Creators need product shipped by **Nov 10** to deliver before BFCM.

## Weekly operating rhythm (about 6–8 hours a week)

| Day | What happens |
| --- | --- |
| **Mon** · Plan (60 min) | Read the scorecard. Pick this week's 2 keywords/products. Update the ManyChat bot fields with this week's links (`build_links.py`). Send creator briefs. |
| **Tue** · Batch (90 min) | Film or collect UGC. Higgsfield gap-fill. |
| **Wed** · Edit + schedule (60 min) | Repurpose each hero video into its versions. QA. Schedule. Every caption carries its keyword CTA. |
| **Daily** · Engage (20 min) | Check the ManyChat Live Chat inbox for handoffs (questions, machine buyers). Reply to non-keyword comments. |
| **Thu** · Amplify (30 min) | Boost the post with the most DMs triggered per 1,000 views |
| **Fri** · Measure (30 min) | Scorecard: views → keyword comments → DMs sent → checkouts → orders, per product |

## Rules

1. **One post, one product, one keyword.**
2. **Impulse band only for organic ($20–$60).** Machines sell through DM conversations.
3. **UGC first.** AI (Higgsfield) is for b-roll and carousels, always labeled, never a fake customer.
4. **The bot only answers people who asked.** No cold DMs, nothing outside the 24-h window.
5. **Friday's numbers decide Monday's plan.**
