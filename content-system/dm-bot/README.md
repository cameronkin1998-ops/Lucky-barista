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

Lucky Barista runs on **Shopify**, separate from Ripple Automations' GoHighLevel, so the bot runs on **ManyChat**. It's an official Meta partner for Instagram and Messenger automation, and it has a Shopify integration. The Pro plan starts at about $15/month for up to 500 contacts; check current pricing.

| Platform | Comment → DM | DM keyword → link | Tool | Notes |
| --- | --- | --- | --- | --- |
| **Instagram** | ✅ Fully automatic | ✅ | **ManyChat** | Meta allows **one private reply per comment** (within 7 days), then unlimited messages for **24 h after the person last messaged**. The bot is designed around this. |
| **Facebook** | ✅ Fully automatic | ✅ | ManyChat (Messenger channel, same flows) | Same Meta rules as Instagram |
| **TikTok** | ⚠️ No automated comment-to-DM | ⚠️ Use TikTok Business Suite's built-in **keyword replies** (confirm in your app). ManyChat's TikTok support is limited; check whether your account qualifies. | TikTok Business Suite + **TikTok Shop product tags** | The TikTok sales channel is already connected in Shopify. **Tag the product in every video**, so every TikTok post has its own buy button. |

The links themselves come from Shopify (`build_links.py`), so every sale is tracked in Shopify Analytics by UTM, whichever bot sends the link.

## Step-by-step build (ManyChat)

### Step 0: connect (one time, ~15 min)
1. Create a ManyChat account → connect **Instagram** (the professional account linked to the Lucky Barista Facebook Page), then add the **Messenger** channel for the Facebook Page.
2. Instagram app → Settings → **Messages and story replies → Connected tools → Allow access to messages: ON**. Without this, the bot can't send DMs.
3. ManyChat → Settings → **Integrations → Shopify**: connect luckybarista.com (Pro plan).
4. ManyChat → Settings → **Fields**: add user fields `interested_product` (text) and `dm_source` (text). Add **bot fields** (global values) holding each product's link, for example `link_foam_checkout`, filled from `build_links.py`. Changing a bot field updates every flow at once.

### Step 1: the comment-to-DM automation (one per active product keyword)
Automation → **New Automation** → name it `DM Bot · FOAM`.

| Part | Setting |
| --- | --- |
| **Trigger** | *User comments on your Post or Reel* → **specific posts** featuring this product (or "any post" when only one product is running) → **comment contains** the keyword list below. Add a second trigger for *Facebook comments* on the same posts. |
| **Public reply** | Turn on "reply to the comment" and rotate 3 versions: "Sent! Check your DMs ☕" · "Just DM'd you 🙌" · "In your inbox now!" |
| **Message A** | DM with the text below and a **button** "Buy now 🛒" → URL `{{link_foam_checkout}}`. Add a second button "See photos first" → the product page link. |
| **Actions** | Set field `interested_product = FOAM` and `dm_source = instagram`. Add tag `dm-foam`. |
| **Smart Delay** | 3 hours |
| **Condition** | They replied, or tapped a button, within the 24-h window, **and** they don't have the `purchased` tag → send **Message B**. Otherwise stop. Never message outside the window. |

**Keyword list for "comment contains"** (the product keyword, plus general buying intent):
`FOAM, foam, link, want, want it, want one, need, need this, how much, price, where, buy, 🙋, 🙋‍♀️, 🙋‍♂️, me, 🔗, ☕`
Each post features one product, so "link" or "want" on a FOAM post always means FOAM. Use **post-specific triggers** whenever more than one product is running.

### Step 2: the DM keyword automation (people who message you directly)
- **Trigger:** *User sends a message* containing a product keyword (FOAM, MUG, SHOT, FLICK, FROTH…), one automation per keyword, each reusing that product's Message A. Story replies arrive as DMs, so this also covers Stories.
- **Default reply** (Automation → Default Reply): "Which one caught your eye? ☕ Reply FOAM for the milk foamer, MUG for the self-stirring mug, SHOT for the shot mirror."
- Optional: ManyChat **AI** (intent recognition / AI step) with `products.csv` as the reference, for questions like "does it work with oat milk?". Keep keyword flows as the main path, because they're predictable.

### Step 3: close the loop with Shopify
- With the ManyChat Shopify integration: when an order matches the subscriber, add tags `purchased` + `bought-<product>` and stop the follow-up. If the integration can't match DM subscribers to orders, skip the tag and rely on the 24-h window. Attribution still works through UTMs.
- Day-10 review and UGC ask: send it with **Shopify Email** (Shopify Marketing automations → post-purchase), not DMs.
- Every Friday: in Shopify Analytics, check orders where `utm_medium=dm` (component 11).

### Step 4: TikTok setup
1. In every product video, tag the product from TikTok Shop (the orange cart). **This is the main way people buy on TikTok.**
2. TikTok → Business Suite → **Direct messages → Keyword replies**: add each product keyword (FOAM, MUG…) with the Message A text and the TikTok-UTM link. Add an **auto-message** for first-time DMs: "Hey! Reply with the product word from the video (like FOAM) and I'll send the link ☕"
3. TikTok caption CTA: "Tap the cart 🛒, or DM me FOAM for the link". (Not "comment": TikTok comments can't trigger a DM.)

## The messages

**Message A, first DM (sent automatically, under 300 characters, one link):**
> Here you go ☕ The **NanoFoamer V2**: café microfoam in about 20 seconds, no steam wand. $59.95.
> 👉 Tap to buy (Shop Pay, 1 tap): {{link_foam_checkout}}
> Want the product page with photos first? Reply PAGE

Use the **checkout link** (Shopify cart permalink, goes straight to Shop Pay) for single-variant products. That's the fewest taps from "I want it" to an order. For products with variants (MUG black/white), ask "Black or white? 🖤🤍" and send the matching checkout link.

**Message B, follow-up (only if they replied, within 24 h):**
> Quick one: most people pair the foamer with the NanoScreen Kit ($20) for finer foam. Want me to add it? Reply YES and I'll send a bundle link. Questions? Just ask, a real person reads these 🙂

**Email capture (optional, Message A2 during BFCM week):**
> Drop your email and I'll send you early Black Friday access + 10% off 🎁

**Human handoff:** if the message contains "?", "broken", "refund", "order", or "shipping", don't send the link. Route it to the ManyChat Live Chat inbox for Cameron (an "Assign to" action plus a notification) and reply "Got it, I'll get back to you personally within a couple of hours."

## Building the links

```bash
cd content-system/dm-bot
python3 build_links.py --platform instagram --campaign q4-w1-foam
python3 build_links.py --platform tiktok --campaign q4-w4-bfcm --discount TTBF15
```
For each keyword the script outputs a product-page link and a one-tap checkout link, both UTM-tagged. Paste them into the ManyChat bot fields. Tested on 2026-11-01: the product pages return 200, and the checkout link `luckybarista.com/cart/<variant>:1` redirects straight to a live Shop Pay checkout.

## Launch test (do this before the first post)
- [ ] From a personal IG account, comment "FOAM" on a test post. You should get the public reply plus a DM within 60 s.
- [ ] Comment "link pls": same result. Comment "nice video": **no** DM.
- [ ] DM "MUG" directly: you should get the mug message and the black/white question.
- [ ] DM "hello": you should get the default "which one?" reply.
- [ ] Tap the checkout link on a phone: it opens Shop Pay with the right product and a $ total. Abandon the checkout.
- [ ] Place a $0 test order (100% test discount): check that the order shows the right UTM in Shopify, and (if the Shopify integration matches) that the subscriber gets tagged `purchased`.
- [ ] Repeat on Facebook. Then check the TikTok keyword reply from a second account.

## Rules (Meta + TikTok policy, and staying out of spam filters)
- Only message people who commented or messaged first. **No cold DMs**, and no messages outside the 24-h window. (Meta's `HUMAN_AGENT` tag allows human replies up to 7 days later, but never automated promos.)
- One link per message. No link shorteners (they hurt deliverability). Use the luckybarista.com links directly.
- Rotate the public comment replies, and limit the bot to the posts it's set up for.
- Keep a "STOP" keyword that unsubscribes the contact (ManyChat has this built in) and ends every flow for them.
