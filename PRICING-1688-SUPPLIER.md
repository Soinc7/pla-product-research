# Pricing: 1688 factory price and the supplier agent delivered quote

Two numbers decide the cost gate. They are different things.

| Number | What it is | Where it comes from |
|---|---|---|
| **Counter price** | Factory price for the item only, in CNY (or USD on Fabulk) | Any 1688 route: Fabulk, 1688order or 1688.com |
| **Delivered cost** | Everything to get one unit to the US, in USD | The supplier agent |

Only the delivered cost is compared to the **under $8** gate.

## Prices on every row (standard from v1.8.0)

Every row on the sheet gets a price, whether it is Green, Orange or Yellow. Two separate numbers:

| Column | What it shows |
|---|---|
| **1688 / Fabulk item cost** | The item cost for the closest product found, as a link to the offer, with a match label (below). "—" only when nothing was found (`NOT_FOUND`). |
| **Est. delivered (standard)** | Item cost + **$5.00 flat**. A planning number, labeled "est." until a real supplier-agent quote replaces it. |

Match labels:

| Label | Meaning |
|---|---|
| `EXACT` | Same product, design, variant and pack |
| `CLOSE` | Same product type and look, a small difference (brand, color, size) |
| `SIMILAR` | Same function, different design. Rough guide only |
| `NOT_FOUND` | No usable match. Show "—" |

Rules:
- The $5.00 flat is a stand-in for China freight, agent fee, packaging and US freight. Replace it as soon as a real quote exists, and then write `QUOTE` next to the number.
- The estimate **ranks** products (cheaper first, among equals). It never releases a Green by itself. The gate below still needs an exact match and a real delivered quote under $8.
- Never write the estimate in the `supplier_landed_cost_usd` field. That field is for real quotes only.


---

## Part A — Find the exact 1688 match

Needs preflight check A = PROVEN on **any one route**:

| Route | Login | Notes |
|---|---|---|
| **Fabulk** (fabulk.com) | Not needed | USD price + MOQ on results. Keyword: `/searchlist?keyword=<words>`. Photo search: camera icon, upload the Kalo main photo. Agent prices include the agent's margin. Label them "Fabulk USD". |
| **1688order.com** | Free account | English agent site |
| **1688.com** | Needed for SKU tiers, image search and counter price | Public search shows CNY list prices without login |

When no route works, do not stop: ask the user to log in or make a free account on one route, and hold pricing only.

### Steps

1. **Start from the Kalo product.** Save its main photo. Write down brand, variant (size, color, material), pack size and what is in the box.
2. **Search 1688 by photo** *(PROPOSED — not in the source rules)*. Use 1688's image search with the product photo, then keyword search.
3. **Search 1688 by keyword too.** Use the product's plain name. Record the search words you used.
4. **Open the closest offers and compare, line by line:**

| Must match | Check |
|---|---|
| Product | Same item, same design, same material |
| Brand | Same brand or same unbranded factory item. If the brand differs, write "brand differs". |
| Variant | Same size, color, capacity |
| Pack / quantity | Same pack count (a 4-pack is not a single) |
| MOQ | Recorded, and workable for a test order |

5. **Compare several independent factories** for the identical spec, quantity and MOQ. Different storefronts of one factory count as one *(PROPOSED)*. Do not average them into an invented number. List each one.
6. **Record for each offer:**

| Field | Example or note |
|---|---|
| Offer ID | The number that identifies the 1688 offer |
| Price in CNY | The tier price at the quantity you would order |
| Price tiers and MOQ | As shown |
| FX rate and FX date | The rate you used, where it came from, and the date |
| USD item price | CNY ÷ rate. Label it "item-only". |
| Excluded charges | What the price does not cover: China freight, packaging, agent fee, US freight, customs |
| Variant, weight, province | As shown |
| Match status | `EXACT`, `BRAND_DIFFERS`, `VARIANT_DIFFERS` or `NO_MATCH`. On the sheet these show as `EXACT` / `CLOSE` / `SIMILAR` / `NOT_FOUND` |

7. **Set the 1688 source status.**

| Status | Meaning | Result |
|---|---|---|
| Verified exact match, 2+ independent factories | Counter price is PROVEN | Go to Part B |
| One exact factory only | PARTIAL | HOLD until more factories are compared (source says "multiple"; 2+ is a PROPOSED minimum) |
| Similar but brand or variant differs | PARTIAL | HOLD |
| No verified exact 1688 match | MISSING | HOLD |

### What past records looked like

From Draft 35 (2026-09-27). Each was a public offer with an **item-only** price, and each row stayed HOLD because the brand differed and there was no delivered quote.

| Product | Offer ID | Item-only price |
|---|---|---|
| Gap brush | 860708953126 | $2.12 |
| Socket adapter, 4-pack | 1010100615485 | $4.31 |
| 90° drill attachment | 568709140093 | $6.69 |
| Honey dispenser, 300 ml | 1032269045841 | $5.08 |
| Drywall clips, 10 pc | 981221169908 | $2.77 |

These are examples of the record format, not current prices.

---

## Part B — Supplier-agent delivered quote

### What to ask for

The human sends the request to the supplier agent. The research agent prepares it and records the answer. Give the agent:

- The 1688 offer ID(s) and product photo.
- Exact variant, pack size and quantity.
- Destination: US.
- A request for the price **split into parts** and what is included.

### The parts of a delivered cost

| Part | Note |
|---|---|
| 1. Factory merchandise | The exact 1688 item price |
| 2. China freight | Factory to the agent's warehouse, per unit |
| 3. Agent margin / service fee | The supplier agent's markup |
| 4. Packaging / handling | Per unit |
| 5. US freight / customs and outbound fulfillment | To the customer's door |

Confirm what the quote includes so nothing is counted twice or left out.

### Record

| Field | Rule |
|---|---|
| `delivered_low_usd` / `base` / `high` | Three numbers. Past example of the shape: $7.50 / $10.50 / $14.00. |
| Type | `QUOTE` (the agent priced this exact product) or `ESTIMATE` (built from past anchors) |
| Method | For an estimate: which historical supplier anchors were used |
| Quote date and quantity | Required |
| Inclusions | Which of the 5 parts are inside the number |

### Estimating when there is no quote yet

- **Default estimate: item cost + $5.00 flat** (see "Prices on every row").
- A better estimate may be built from **historical anchors**: past factory price vs past supplier-agent price for the **same SKU, currency, quantity and services**.
- If there is no such history, the markup is `UNKNOWN`. Do not guess a percentage.
- Any estimate is a planning number. It can rank products. It **cannot release a green**.

---

## Decision rules

| Rule | Result |
|---|---|
| Item-only 1688 price ≠ delivered cost | Never compare an item-only price to the $8 gate |
| Alibaba ≠ 1688 proof | Alibaba comparisons are recorded separately and prove nothing for 1688 |
| No exact 1688 match | HOLD for launch. The research row still shows the closest item as `CLOSE` or `SIMILAR`; the research tier is unchanged. |
| Only one factory compared | HOLD for launch |
| No invented average | List each factory price as found |
| No exact delivered quote below $8 | No launch handoff (the research tier from `TIERS.md` is unchanged) |
| Delivered quote from $8 up to $10 | Stretch zone. Not a pass. HOLD for a better quote or an owner decision. |
| Perceived sale value above $30 | Fails economic fit |
| Markup with no same-SKU history | `UNKNOWN` |
| `supplier_landed_cost_usd` | Its own field. Never copied from the Kalo price. |

A product clears pricing only with **both**: a verified exact 1688 match and a current exact delivered quote below $8.
