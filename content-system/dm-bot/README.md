# The DM Link Bot ("Comment FOAM and I'll send you the link")

**The problem:** a bio holds one link, so organic posts can only push one product at a time.
**The fix:** every post gets its own keyword. When someone comments that keyword or DMs it ("I want it", "link?"), a bot automatically sends them **that post's product link** in their DMs. The bio link stops being the bottleneck, and every interested buyer gets a one-tap checkout link in their inbox.

```
 Post (one product, one keyword)       e.g. "Comment FOAM ☕ and I'll DM you the link"
        │
        ├─ Comment contains FOAM / "want" / "link" / "how much" ─┐
        ├─ Story reply / DM containing the same ─────────────────┤
        │                                                        ▼
        │                      BOT ── 1. public comment reply: "Sent! Check your DMs ☕"
        │                          ── 2. private DM: hook line + price + [Buy now] button
        │                                (one-tap checkout link, UTM-tagged)
        │                          ── 3. tag contact in CRM: interested-foam, source=ig
        │                                                        ▼
        │                      Buyer taps → Shopify checkout (Shop Pay) → Order
        │                                                        ▼
        └────────── no purchase in 3 h? ── follow-up DM (inside the 24-h window)
                                          + ask for email → abandoned-interest email flow
```

## Which tool runs the bot on each platform

| Platform | Comment → DM | DM keyword → link | Tool | Notes |
| --- | --- | --- | --- | --- |
| **Instagram** | ✅ Fully automatic | ✅ | **GoHighLevel** (you already have it, through Ripple Automations). ManyChat is the backup. | Meta allows **one private reply per comment** (within 7 days), and then unlimited messages for **24 h after the person last messaged**. The bot is designed around this. |
| **Facebook** | ✅ Fully automatic | ✅ | GoHighLevel (same workflows) | Same Meta rules as Instagram |
| **TikTok** | ⚠️ No open DM API for automated comment-to-DM. GHL can only reply **publicly** to TikTok comments (150 characters max). | ⚠️ TikTok Business accounts have built-in **auto-messages and keyword replies** in the DM settings. Confirm this in your app. | TikTok Business Suite + **TikTok Shop product tags** | The TikTok Shop channel is already connected in Shopify. **Tag the product in every video**, so every TikTok post has its own buy button and the bio link isn't needed. |

**Recommendation:** run Instagram and Facebook through GoHighLevel. It's already your CRM, so every person who asks for a link becomes a contact you can follow up with by email or SMS. On TikTok, use product tags plus the built-in keyword auto-reply. If GHL's Instagram comment trigger turns out to be unreliable in testing, set up the same flows in ManyChat (an official Meta partner, from about $15/mo) and send contacts to GHL by webhook.

## Step-by-step build (GoHighLevel)

Workflows are built in the GHL interface (the API can send messages but can't create workflows), so these are the click-steps.

### Step 0: connect the accounts (one time, ~10 min)
1. GHL → **Settings → Integrations → Facebook & Instagram**: connect the Lucky Barista Facebook Page and the Instagram professional account linked to it.
2. Instagram app → Settings → **Messages and story replies → Connected tools → Allow access to messages: ON**. Without this, the bot can't send DMs.
3. GHL → **Settings → Custom Fields**: add `interested_product` (text) and `dm_source` (dropdown: instagram, facebook, tiktok).
4. GHL → **Settings → Custom Values**: add one value per product, holding its link (from `products.csv` / `build_links.py`), for example `{{custom_values.link_foam}}`. Changing a link then updates every workflow at once.

### Step 1: the comment-to-DM workflow (one per active product keyword)
**Automation → Workflows → Create → Start from scratch** → name it `DM Bot · FOAM`.

| Part | Setting |
| --- | --- |
| **Trigger** | *Instagram Comment(s) On A Post* (add a second trigger: *Facebook Comment(s) On A Post*). Filters: **Post** = the posts featuring this product (or "any post"). **Contains phrase** = the keyword list below. Turn on **track first-level comments only**. |
| **Action 1** | *Reply in Comments* (public): rotate 3 versions so it doesn't look spammy: "Sent! Check your DMs ☕" · "Just DM'd you 🙌" · "In your inbox now!" |
| **Action 2** | *Instagram DM* / *Facebook Messenger* (private reply): **Message A** below |
| **Action 3** | *Update Contact Field*: `interested_product = FOAM`, `dm_source = instagram`. *Add Tag*: `dm-foam`, `q4-dm-bot`. |
| **Action 4** | *Wait* 3 hours |
| **Action 5** | *If/Else*: the contact has tag `purchased` (set by the Shopify order trigger in Step 3)? → End. Otherwise, did they reply after Message A? → send **Message B** (allowed, because their reply reopened the 24-h window). If they didn't reply → End. Never message outside the window. |

**Keyword list for "contains phrase"** (the product keyword, plus generic buying intent):
`FOAM, foam, link, want, want it, want one, need, need this, how much, price, where, buy, 🙋, 🙋‍♀️, 🙋‍♂️, me, 🔗, ☕`
Each post features one product, so generic words like "link" or "want" on a FOAM post always mean FOAM. Use **post-specific triggers** when you're running several products at once.

### Step 2: the DM keyword workflow (people who message you directly)
New workflow `DM Bot · inbound keywords`.
- **Trigger:** *Customer Replied* → channel = Instagram / Facebook → filter "message contains" the product keywords (FOAM, MUG, SHOT, FLICK, FROTH…).
- **Branch** (If/Else on the keyword) → send that product's **Message A** and tag the contact.
- **Fallback branch** (message says "link" or "price" but no product name): "Which one caught your eye? ☕ Reply FOAM for the milk foamer, MUG for the self-stirring mug, SHOT for the shot mirror." When they answer, the keyword branch runs.
- **Story replies** come in as DMs, so this same workflow covers Story link requests.
- Optional: turn on **GHL Conversation AI** (bot mode, *suggestive* first, then *auto-pilot*) with `products.csv` as its knowledge base, so it can answer things like "does it work with oat milk?". Keep the keyword workflow as the main path, because it's predictable.

### Step 3: close the loop with Shopify
- GHL → Integrations → **Shopify**: connect luckybarista.com.
- Workflow `DM Bot · purchased`: trigger *Shopify Order Placed* → find the contact by email/phone → add tag `purchased` + `bought-<product>` → stop all DM Bot follow-ups → day 10: "How's the foam? Send us a clip for $10 off your next order" (this feeds the UGC loop).
- Attribution check every Friday: Shopify orders with `utm_medium=dm` (component 11).

### Step 4: TikTok setup
1. In every product video, tag the product from TikTok Shop (the orange cart). **This is the main buy path on TikTok.**
2. TikTok → Business Suite → **Direct messages → Keyword replies**: add each product keyword (FOAM, MUG…) with Message A text and the TikTok-UTM link. Add an **auto-message** for first-time DMs: "Hey! Reply with the product word from the video (like FOAM) and I'll send the link ☕"
3. Caption CTA on TikTok: "Tap the cart 🛒, or DM me FOAM for the link". (Not "comment": TikTok comments can't trigger a DM.)
4. Optional GHL workflow: public reply to TikTok comments containing the keyword: "DM us FOAM and the link comes right back 🙌" (150 characters max).

## The messages

**Message A, first DM (sent automatically, under 300 characters, one link):**
> Here you go ☕ The **NanoFoamer V2**: café microfoam in about 20 seconds, no steam wand. $59.95.
> 👉 Tap to buy (Shop Pay, 1 tap): {{custom_values.link_foam_checkout}}
> Want the product page with photos first? Reply PAGE

Use the **checkout link** (Shopify cart permalink, goes straight to Shop Pay) for single-variant products. That's the fewest taps from "I want it" to an order. For products with variants (MUG black/white), ask "Black or white? 🖤🤍" and send the matching checkout link.

**Message B, follow-up (only if they replied, within 24 h):**
> Quick one: most people pair the foamer with the NanoScreen Kit ($20) for finer foam. Want me to add it? Reply YES and I'll send a bundle link. Questions? Just ask, a real person reads these 🙂

**Email capture (optional, Message A2 during BFCM week):**
> Drop your email and I'll send you early Black Friday access + 10% off 🎁

**Human handoff:** if the message contains "?", "broken", "refund", "order", or "shipping", don't send the link. Assign the conversation to Cameron in the GHL inbox and reply "Got it, I'll get back to you personally within a couple of hours."

## Building the links

```bash
cd content-system/dm-bot
python3 build_links.py --platform instagram --campaign q4-w1-foam
python3 build_links.py --platform tiktok --campaign q4-w4-bfcm --discount TTBF15
```
For each keyword the script outputs a product-page link and a one-tap checkout link, both UTM-tagged. Paste them into the GHL Custom Values. Tested on 2026-11-01: the product pages return 200, and the checkout link `luckybarista.com/cart/<variant>:1` redirects straight to a live Shop Pay checkout.

## Launch test (do this before the first post)
- [ ] From a personal IG account, comment "FOAM" on a test post. You should get the public reply plus a DM within 60 s.
- [ ] Comment "link pls": same result. Comment "nice video": **no** DM.
- [ ] DM "MUG" directly: you should get the mug message and the black/white question.
- [ ] Tap the checkout link on a phone: it opens Shop Pay with the right product and a $ total. Abandon the checkout.
- [ ] Place a $0 test order (100% test discount): the contact gets tagged `purchased` and the follow-ups stop.
- [ ] Repeat on Facebook. Then check the TikTok keyword reply from a second account.

## Rules (Meta + TikTok policy, and staying out of spam filters)
- Only message people who commented or messaged first. **No cold DMs**, and no messages outside the 24-h window. (Meta's `HUMAN_AGENT` tag allows human replies up to 7 days later, but never automated promos.)
- One link per message. No link shorteners (they hurt deliverability). Use the luckybarista.com links directly.
- Rotate the public comment replies, and limit the bot to the posts it's set up for.
- Keep a "STOP" keyword that tags `dm-optout` and ends every DM workflow for that contact.
