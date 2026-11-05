# 7 · Production Workflow (UGC-first)

## Where the content comes from

| Source | Share | Cost | Speed | Use for |
| --- | --- | --- | --- | --- |
| **Cameron / in-house UGC** (phone, own counter) | 30% | $0 | Same day | Daily demos, replies to comments, BTS, founder story |
| **Paid UGC creators** (micro, 2k–50k followers, or UGC-only creators) | 35% | $50–$200 per video, plus free product | 5–10 days | Reviews, unboxings, gift guides, ad creative |
| **TikTok Shop affiliates / gifted seeding** | 15% | Commission only, plus product | 1–3 weeks | Volume, social proof, posts on creators' own accounts |
| **Customer UGC** (post-purchase ask) | 10% (grows) | Discount code or feature | Ongoing | Proof and People pillar |
| **Higgsfield AI** (existing TikTok skill) | 10% | Credits | Hours | B-roll, carousels, waitlist teasers for out-of-stock items. **Always labeled as AI.** Never used as a fake "customer". |

## Creator pipeline (a simple Google Sheet; Lucky Barista stays separate from Ripple's GHL)

`Sourced → Contacted → Agreed → Product shipped → Draft received → Approved → Posted → Paid → Re-book?`

1. **Source** 15 creators a week. TikTok search for `#homebarista #latteart #coffeecorner #espressoathome`, Instagram Reels on the same tags, and Billo / Insense / TikTok Creator Marketplace. Look for: good light, a real coffee setup, average views ≥ 2× their follower median, and comments that are real people.
2. **Contact** using [`templates/creator-outreach.md`](templates/creator-outreach.md). Expect 20–30% replies.
3. **Agree** on deliverables, rate, usage rights (organic plus 90-day paid whitelisting), deadline, and the FTC disclosure requirement.
4. **Ship** the product from Shopify as a $0 draft order tagged `ugc-seeding` (this keeps inventory accurate).
5. **Brief** using [`templates/ugc-brief.md`](templates/ugc-brief.md). Include one reference ID from `style-references/`.
6. **Review** against the approval checklist in component 3. Allow 1 round of revisions.
7. **Post / whitelist.** Use a Collab post on IG, Spark Ads code on TikTok, and partnership ads on Meta.
8. **Pay and log performance.** Re-book the top 30% of creators automatically.

**Deadline for BFCM:** creators must be shipped product by **Nov 10** so drafts arrive by Nov 20.

## The weekly production line

| Stage | Owner | Output | Tool |
| --- | --- | --- | --- |
| 1. Plan | Cameron (Mon) | 2 hero products, theme, 10–14 post slots | This repo + scorecard |
| 2. Brief | Cameron / Claude | 3 hero briefs + creator briefs | `templates/ugc-brief.md` |
| 3. Capture | Cameron + creators | Raw vertical footage. Get 3+ angles per product: hands, overhead, wide. | Phone |
| 4. Gap-fill | Claude (daily skill) | AI b-roll or carousel for 1 slot a day | Higgsfield `lucky-barista-tiktok-video` skill |
| 5. Edit | Cameron | Cuts per the repurposing matrix (component 4) | CapCut / Edits app |
| 6. QA | Cameron | Checklist passed | Component 3 checklist |
| 7. Caption + UTM | Cameron / Claude | Caption per platform, UTM link | `templates/caption-formulas.md`, component 8 |
| 8. Schedule | Cameron (Wed) | Week scheduled | Meta Business Suite (IG + FB), TikTok drafts / scheduler |
| 9. Publish & engage | Daily | Live posts, replies in the first 60 min | Native apps |
| 10. Log | Fri | Scorecard rows | `templates/weekly-scorecard.md` |

## File naming and storage

`LB_<YYYYMMDD>_<product-slug>_<format#>_<source>_<platform>_v<N>.mp4` (for example, `LB_20261104_nanofoamer-v2_F2_creator-jess_tt_v1.mp4`)

Store raw files and finals in a Google Drive folder `Lucky Barista / Q4 Content / <week>`. Keep creator usage-rights agreements in `/_rights`.
