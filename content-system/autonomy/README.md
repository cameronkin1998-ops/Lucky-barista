# Autonomous Content Pipeline: Generate → Review → Post → Learn

The goal: Lucky Barista content gets made, checked, published to TikTok, Instagram, Facebook and Pinterest, and measured every day without Cameron touching it. Cameron sets the rules, gets a daily summary, and can stop anything at any point.

Status 2026-11-05: **design.** Stage 1 (generate) is live. Stages 2–4 need the setup listed under *Prerequisites*.

## The pipeline

```
 09:00  1. GENERATE   (live)   lucky-barista-daily-ugc skill → Higgsfield video + carousel → Drive folder + Content Log
          │
 10:30  2. REVIEW     (new)    lucky-barista-content-review skill
          │                    downloads each asset, pulls frames, checks it against the rubric below,
          │                    checks the caption against the guardrails, checks the product is in stock
          │                    → PASS / FIX (one automatic retry) / HOLD (Cameron decides)
          ▼
 10:45  3. PUBLISH    (new)    lucky-barista-publish skill → GHL Social Planner (CK ECOM LLC sub-account)
          │                    one post per platform with that platform's caption, scheduled at its best time,
          │                    keyword CTA as the first comment → feeds the DM bot (dm-bot/)
          ▼
 Daily  4. LEARN      (new)    lucky-barista-performance skill (next morning)
                               GHL statistics + Shopify UTM orders → Content Log → tomorrow's generation
                               favors the hooks, products and formats that sold
```

Each stage is its own skill and scheduled task, so one stage failing never takes down the others, and each can be paused separately.

## Why GHL Social Planner is the posting layer

Checked on 2026-11-05 against the GHL connector you already have (sub-account **CK ECOM LLC**, `oBjoE8Yn8uvoZuQ1JPyI`):

| Need | GHL supports it | Detail |
| --- | --- | --- |
| TikTok video posts | ✅ | `type: reel`. `tiktokPostDetails`: privacy, comments, duet/stitch, **`promoteYourBrand`** (brand disclosure) |
| Instagram Reels + carousels | ✅ | `instagramPostDetails.type: reel/post`, up to 10 images |
| Facebook Reels + posts | ✅ | `facebookPostDetails.type` |
| Pinterest pins | ✅ | `pinterestPostDetails`: title, **destination link**, board IDs. 1 image per pin. |
| Scheduling | ✅ | `status: scheduled` + `scheduleDate` |
| Approval step | ✅ | `status: in_review` + an approver. Cameron taps approve in the GHL app. This powers autonomy Level 1. |
| First comment | ✅ | `followUpComment` (not on Pinterest). Use it for "Comment FOAM and I'll DM you the link". |
| Performance data | ✅ | `get-statistics` (account-level, by date range) |
| Platform-specific captions | ✅ | One request per platform. Mixing platforms in one request trims the caption to the shortest platform limit. |

Other options considered: the Higgsfield TikTok connection (only stages drafts, which a person then has to submit, so it can't run unattended, and it's TikTok-only); posting to each platform's API directly (needs our own developer app and app review on Meta, TikTok and Pinterest, which takes weeks). GHL already handles those approvals.

**Current state:** `get-account` returns **0 connected social accounts** in CK ECOM LLC. Connecting them is the first prerequisite.

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
3. Per platform (separate requests):

| Platform | Asset | Time (Central) | Caption | First comment |
| --- | --- | --- | --- | --- |
| TikTok | The video, as a reel | 7:00 p.m. (test 7 a.m. vs 7 p.m. for 2 weeks) | TikTok caption from the skill | "DM me FOAM for the link 🛒" |
| Instagram | The same video as a reel; the carousel as a post on carousel days | 12:00 p.m. | IG caption + "Comment FOAM" | "Comment FOAM and I'll DM you the link ☕" |
| Facebook | The same video as a reel | 6:00 p.m. | FB caption + price | Same as IG |
| Pinterest | Carousel slide 2 or 4 as a pin, plus the video pin | 8:00 p.m. | Pin title + description from the skill | (not supported) |

4. Links use `dm-bot/build_links.py` UTMs (`utm_source=<platform>&utm_medium=organic&utm_campaign=<date>-<product>`), so stage 4 can tie sales to posts.
5. Limits: at most 2 posts per platform per day, nothing between 10 p.m. and 6 a.m., and never the same video on the same platform twice.
6. Log each GHL post ID in the Content Log, and send one daily email: what got scheduled, when, and the GHL link to cancel anything.

## Autonomy levels (move up only on evidence)

| Level | What the agent does | What Cameron does | Move up when |
| --- | --- | --- | --- |
| **L0** (today) | Generates and saves to Drive | Reviews, posts by hand, logs views | The review agent is built and running |
| **L1 Approve** | Reviews, then creates GHL posts as **`in_review`** with Cameron as approver | Taps approve or reject in the GHL app (about 10 s a post) | 2 weeks in which Cameron agreed with ≥ 90% of the agent's PASS verdicts |
| **L2 Veto** | Schedules PASS posts **at least 4 h ahead** automatically, then emails a preview | Deletes anything he doesn't like before it goes live | 2 more weeks with ≤ 1 veto a week |
| **L3 Full** | Schedules and publishes on its own. HOLDs still go to Cameron. | Reads the daily and weekly summaries | Ongoing. Drops back to L2 automatically after any post Cameron deletes after it's live. |

Levels can differ by platform (for example, Pinterest at L3 while TikTok stays at L1).

## Stage 4: learning loop

The next morning, before generation runs:
- `get-statistics` (GHL) for the past day's posts: views, likes, comments, shares, saves.
- Shopify: orders and sessions by `utm_campaign` and `utm_source`, plus DM-bot tags (`dm-<keyword>`).
- These get written into the Content Log rows, filling the views and notes columns Cameron fills in by hand today.
- The generation skill already favors "angles and products with the best logged views." This changes it to rank by **orders and DM asks per 1,000 views** first, then views.
- Every Monday, a weekly summary email: top 3 posts, what to make more of, what to stop.

## Disclosure (must be solved before any automatic TikTok posting)

The videos are AI-generated and realistic. **TikTok requires an "AI-generated" label on realistic AI content**, and Meta labels AI content too. GHL's TikTok fields include brand disclosure (`promoteYourBrand`) but **no AI-generated flag**, as far as the API description shows.

What to do: test one post through GHL. If the AI label can't be set through the API, TikTok stays at **L1**: GHL creates the post and Cameron switches on the AI label in the TikTok app before it goes live. Or TikTok posts keep going through the Higgsfield draft path, which does set `is_aigc`. Either way, every caption also carries a plain disclosure (for example "AI-generated product demo"). We never present AI footage as a real customer.

## Prerequisites (Cameron)

1. **Connect the social accounts in GHL:** CK ECOM LLC → Marketing → Social Planner → connect **TikTok (@luckybarista_)**, the **Instagram** professional account, the **Facebook Page**, and **Pinterest** (business account). Create 3–5 Pinterest boards (for example "Coffee Gift Ideas", "Home Coffee Bar", "Espresso at Home").
2. **Add the GHL connector** ("Ripple Automations – GHL Client") to the daily scheduled task and the new ones, next to Higgsfield, Google Drive and Gmail.
3. **Check that Higgsfield links last.** Posts are scheduled hours ahead, so the media URL has to stay valid. If Higgsfield links expire, the publish agent uploads the file to GHL's media library first.
4. **Decide on the AI label approach above.**
5. **Sign off on the rubric and the posting times** (edit this file).
6. **Create the `LB AUTOPILOT` doc** in Drive with the word `ON` when you want posting to begin.

## Build plan (Claude)

| Step | Deliverable | Depends on |
| --- | --- | --- |
| 1 | `lucky-barista-content-review` skill + a 10:30 a.m. scheduled task. Runs in "shadow mode" (logs verdicts only) for 1 week. | Nothing. Can start now. |
| 2 | Calibrate: compare the agent's verdicts with what Cameron would have posted, and tune the rubric | 1 week of shadow results |
| 3 | `lucky-barista-publish` skill at **L1** (in_review posts) + a 10:45 a.m. scheduled task | Prerequisites 1, 2, 4 |
| 4 | Test post on each platform: confirm the caption, first comment, link, disclosure and timing came out right | Step 3 |
| 5 | `lucky-barista-performance` skill + a morning scheduled task. Generation reads the results. | Step 3 |
| 6 | Move up a level, per the table | Evidence |
| 7 | Update the generation skill: keyword CTA ("Comment FOAM") replaces "link in bio", IG/FB captions, impulse lineup | DM bot live |

## Things that need watching

- **Credits:** review retries (FIX) come out of the same reserve. The generation skill's 150-credit floor applies to every stage.
- **The GHL connector asks for approval on writes.** Confirm that scheduled sessions can create posts without a person present; this gets tested in step 4.
- **Account health:** a new account posting a lot of AI content can get less reach. Start at 1 post a day per platform, and watch reach in the weekly summary.
