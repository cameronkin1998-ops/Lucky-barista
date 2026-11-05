# Autonomous Content Pipeline: Generate → Review → Post → Learn

The goal: Lucky Barista content gets made, checked, published to TikTok, Instagram, Facebook and Pinterest, and measured every day without Cameron touching it. Cameron sets the rules, gets a daily summary, and can stop anything at any point.

Status 2026-11-05: **design.** Stage 1 (generate) is live. Stages 2–4 need the setup listed under *Prerequisites*.

## The pipeline

Lucky Barista runs on **Shopify, Higgsfield, Google Drive and Gmail**, plus a posting service. It doesn't use GoHighLevel at all; GHL is only for Ripple Automations and its clients.

```
 09:00  1. GENERATE   (live)   lucky-barista-daily-ugc skill → Higgsfield video + carousel → Drive folder + Content Log
          │
 10:30  2. REVIEW     (new)    lucky-barista-content-review skill
          │                    downloads each asset, pulls frames, checks it against the rubric below,
          │                    checks the caption against the guardrails, checks the product is in stock on Shopify
          │                    → PASS / FIX (one automatic retry) / HOLD (Cameron decides)
          ▼
 11:30  3. PUBLISH    (new)    lucky-barista-publish skill → Ayrshare API (posting service)
          │                    one post per platform with that platform's caption, scheduled at its best time,
          │                    TikTok AI-generated label on, keyword CTA as the first comment → feeds the ManyChat DM bot
          ▼
 Daily  4. LEARN      (new)    lucky-barista-performance skill (next morning)
                               Ayrshare post analytics + Shopify UTM orders → Content Log → tomorrow's generation
                               favors the hooks, products and formats that sold
```

Each stage is its own skill and scheduled task, so one stage failing never takes down the others, and each can be paused separately.

## Posting layer: Ayrshare (recommended)

Ayrshare is a posting API built for automation. It publishes to **TikTok, Instagram, Facebook and Pinterest** from one request, and it's already been through each platform's API approval, so we don't need our own developer apps.

| Need | Ayrshare | Status |
| --- | --- | --- |
| **TikTok AI-generated label** | `isAIGenerated: true` turns on TikTok's AI-generated content label. Also `isBrandOrganic` (promotional content label). | ✅ **Confirmed in Ayrshare's TikTok docs.** This removes the main blocker for automatic TikTok posting. |
| TikTok, Instagram Reels, Facebook Reels, Pinterest pins | One API call with the platform list, the media URL and options for each platform (Pinterest board and destination link) | Verify the exact field names during the build |
| Scheduling | A `scheduleDate` on the post. Scheduled posts can be deleted, which is what makes "veto" possible. | Verify during the build |
| First comment | A first-comment option for the "Comment FOAM" CTA | Verify during the build |
| Analytics | Per-post analytics endpoint | Verify during the build |
| Connecting accounts | Cameron links TikTok, IG, FB and Pinterest once in the Ayrshare dashboard | Prerequisite |

**How Claude connects:** an **Ayrshare API key** stored as a secret in a **separate cloud environment just for Lucky Barista**. That keeps it away from the Ripple routines. The environment's network policy has to allow `api.ayrshare.com`. Check Ayrshare's current plans; you need one that covers 4 platforms and scheduled posts.

**Alternatives** if Ayrshare doesn't fit: hosted posting services that offer a ready-made MCP connector (bundle.social, PostFast, PostEverywhere), or open-source **Postiz** (self-hosted). Before choosing any of them, confirm it can set TikTok's AI-generated label.

**Not suitable:** the Higgsfield TikTok connection (it only stages drafts that a person then has to submit, and it's TikTok-only); Shopify's sales channels (they sync products for ads and shopping, but can't publish organic posts); building our own apps against each platform's API (weeks of app review).

## Stage 2: the review agent

Each asset gets a scored check. **Hard fails** block it automatically. **Soft checks** add up to a score.

### Hard fails (any one means no automatic posting)
| # | Check | How it's checked |
| --- | --- | --- |
| H1 | The product on screen matches the reference product (shape, color, parts) | 8 frames compared visually with the reference image |
| H2 | No AI glitches: extra or merged fingers, objects melting, liquid flowing the wrong way, grounds coming out of the wrong part | Frame-by-frame look at hands and the product's moving parts |
| H3 | No readable text, logos, or other brands in the footage | Frame check |
| H4 | The caption makes no invented claim (no reviews, "best-seller", made-up specs) and every fact matches the product listing | Caption compared with the Shopify listing |
| H5 | The product is in stock and the link works | `luckybarista.com/products/<handle>.js` → `available: true`, HTTP 200 |
| H6 | Not a repeat: the same product + hook isn't already published in the last 7 days | Content Log |
| H7 | AI disclosure is ready for that platform (see *Disclosure*) | Post settings |

### Soft score (0–10; 7 or higher passes)
- The hook (action happens within the first second): 0–3
- A satisfying beat every 1–3 s, per the viral formula: 0–2
- A payoff shot at the end (finished drink or result): 0–2
- Looks like a real person filmed it on a phone (light, framing, not glossy): 0–2
- The caption follows the format and has the keyword CTA: 0–1

### Verdicts
- **PASS** (no hard fails, score ≥ 7): goes to Publish.
- **FIX** (a soft score below 7, or H2/H3 on one carousel slide): regenerate once (a single slide, or a new video if the credit floor allows), then review again. A second fail becomes HOLD.
- **HOLD** (any other hard fail, or a second fail): not posted. The reason and frames go into the Drive doc and the daily email for Cameron.

The review notes are written into the piece's Drive doc and logged as a `review` column in the Content Log. **Every verdict is logged**, which is how we judge whether the reviewer can be trusted with more autonomy.

## Stage 3: the publish agent

1. Read today's PASS pieces from the Content Log.
2. Check the **kill switch**: a Drive doc called `LB AUTOPILOT` with one line, `ON` or `OFF`. If it's OFF, or the doc is missing, schedule nothing and send the email.
3. Per platform (separate captions):

| Platform | Asset | Time (Central) | Caption | First comment |
| --- | --- | --- | --- | --- |
| TikTok | The video, as a reel | 7:00 p.m. (test 7 a.m. vs 7 p.m. for 2 weeks) | TikTok caption from the skill | "DM me FOAM for the link 🛒" |
| Instagram | The same video as a reel; the carousel as a post on carousel days | 12:00 p.m. | IG caption + "Comment FOAM" | "Comment FOAM and I'll DM you the link ☕" |
| Facebook | The same video as a reel | 6:00 p.m. | FB caption + price | Same as IG |
| Pinterest | Carousel slide 2 or 4 as a pin, plus the video pin | 8:00 p.m. | Pin title + description from the skill | (not supported) |

4. Links use `dm-bot/build_links.py` UTMs (`utm_source=<platform>&utm_medium=organic&utm_campaign=<date>-<product>`), so stage 4 can tie sales to posts.
5. Limits: at most 2 posts per platform per day, nothing between 10 p.m. and 6 a.m., and never the same video on the same platform twice.
6. Log each Ayrshare post ID in the Content Log, and send one daily email: what got scheduled, when, and how to cancel it (mark VETO in the log, or delete it in the Ayrshare dashboard).
7. TikTok posts always go out with `isAIGenerated: true`, and every caption also carries a plain disclosure.

## Autonomy levels (move up only on evidence)

| Level | What the agent does | What Cameron does | Move up when |
| --- | --- | --- | --- |
| **L0** (today) | Generates and saves to Drive | Reviews, posts by hand, logs views | The review agent is built and running |
| **L1 Approve** | Reviews, then writes each PASS piece into the Content Log with an empty **Approve** checkbox. The 11:30 publish run only schedules pieces Cameron has ticked. | Ticks Approve in the Content Log sheet, on his phone (about 10 s a post) | 2 weeks in which Cameron agreed with ≥ 90% of the agent's PASS verdicts |
| **L2 Veto** | Schedules PASS posts **at least 4 h ahead** automatically, then emails a preview | Marks VETO in the Content Log (a check before publishing deletes that scheduled post) or deletes it in Ayrshare | 2 more weeks with ≤ 1 veto a week |
| **L3 Full** | Schedules and publishes on its own. HOLDs still go to Cameron. | Reads the daily and weekly summaries | Ongoing. Drops back to L2 automatically after any post Cameron deletes after it's live. |

Levels can differ by platform (for example, Pinterest at L3 while TikTok stays at L1).

## Stage 4: learning loop

The next morning, before generation runs:
- Ayrshare post analytics for the past day's posts: views, likes, comments, shares, saves.
- Shopify (connector required on this scheduled task): orders and sessions by `utm_campaign` and `utm_source`. DM asks come from ManyChat tags (`dm-<keyword>`), entered weekly until ManyChat data can be pulled automatically.
- These get written into the Content Log rows, filling the views and notes columns Cameron fills in by hand today.
- The generation skill already favors "angles and products with the best logged views." This changes it to rank by **orders and DM asks per 1,000 views** first, then views.
- Every Monday, a weekly summary email: top 3 posts, what to make more of, what to stop.

## Disclosure

The videos are AI-generated and realistic. TikTok requires an AI-generated label on realistic AI content, and Meta labels AI content too.
- **TikTok:** Ayrshare's `isAIGenerated: true` on every post. This is required, and the publish agent refuses to post to TikTok without it. The label can't be removed after posting, which is fine.
- **Instagram and Facebook:** a plain disclosure in the caption ("AI-generated product demo"), plus Meta's own "AI info" label when it's available through the API. Check this during the build.
- **All platforms:** never present AI footage as a real customer, review or testimonial.

## Prerequisites (Cameron)

1. **Sign up for Ayrshare** (or one of the alternatives) and link **TikTok (@luckybarista_)**, the **Instagram** professional account, the **Facebook Page** and **Pinterest** (business account). Create 3–5 Pinterest boards (for example "Coffee Gift Ideas", "Home Coffee Bar", "Espresso at Home").
2. **Create a Lucky Barista cloud environment** with the Ayrshare API key as a secret and `api.ayrshare.com` allowed in its network settings. Claude can walk you through it.
3. **Attach the Shopify connector** to the Lucky Barista scheduled tasks (review and learn need it), alongside Higgsfield, Google Drive and Gmail.
4. **Check that Higgsfield links last.** Posts are scheduled hours ahead, so the media URL has to stay valid. If Higgsfield links expire, the publish agent uploads the file to Ayrshare first.
5. **Sign off on the rubric and the posting times** (edit this file).
6. **Create the `LB AUTOPILOT` doc** in Drive with the word `ON` when you want posting to begin.

## Build plan (Claude)

| Step | Deliverable | Depends on |
| --- | --- | --- |
| 1 | `lucky-barista-content-review` skill + a 10:30 a.m. scheduled task. Runs in "shadow mode" (logs verdicts only) for 1 week. | Nothing. Can start now. |
| 2 | Calibrate: compare the agent's verdicts with what Cameron would have posted, and tune the rubric | 1 week of shadow results |
| 3 | `lucky-barista-publish` skill at **L1** (Approve checkbox) + an 11:30 a.m. scheduled task | Prerequisites 1, 2, 4 |
| 4 | Test post on each platform: confirm the caption, first comment, link, disclosure and timing came out right | Step 3 |
| 5 | `lucky-barista-performance` skill + a morning scheduled task. Generation reads the results. | Step 3 |
| 6 | Move up a level, per the table | Evidence |
| 7 | Update the generation skill: keyword CTA ("Comment FOAM") replaces "link in bio", IG/FB captions, impulse lineup | DM bot live |

## Things that need watching

- **Credits:** review retries (FIX) come out of the same reserve. The generation skill's 150-credit floor applies to every stage.
- **Posting runs unattended.** Confirm that scheduled sessions can reach Ayrshare with the stored key and post without a permission prompt; this gets tested in step 4.
- **Account health:** a new account posting a lot of AI content can get less reach. Start at 1 post a day per platform, and watch reach in the weekly summary.
