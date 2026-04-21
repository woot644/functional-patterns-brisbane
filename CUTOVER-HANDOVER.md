# Squarespace → Vercel Cutover — Post-Cutover Summary

**Status:** ✅ Live on `www.functionalpatternsbrisbane.com` as of 2026-04-20.
**DNS flip performed:** 2026-04-20 evening (AEST). Propagation + SSL issuance completed within minutes.
**Verification:** 268/268 old URLs return 200 on the live domain.

---

## Final DNS configuration (at Squarespace)

Only two records changed from the original Squarespace setup. All email/verification records stay as they were.

| Type | Name | Value |
|---|---|---|
| A | `@` | `216.150.1.1` |
| CNAME | `www` | `e7eb037fabed336b.vercel-dns-017.com.` |

**Deleted:** the "Squarespace Defaults" DNS preset (4 A records + CNAME `www` → `ext-sq.squarespace.com`).
**Untouched:** Google Workspace MX (`smtp.google.com`), Amazon SES DKIM/MX on `mail.` subdomain, Brevo code, HubSpot `go.` + `www.go.` CNAMEs, DMARC, SPF, all `_cf-custom-hostname` + `google-site-verification` TXT records.

---

## What was completed

### Pre-cutover build + redirects (committed before 2026-04-20)
- 15 missing blog posts ported from original migration (blog drives ~87% of organic traffic)
- 95 explicit 301 redirects in `vercel.json` covering every structural slug change
- All canonical / og:url / JSON-LD / sitemap / robots.txt / llms.txt references updated to `www.functionalpatternsbrisbane.com`
- Full Squarespace backup at `backup-squarespace/` (gitignored) — 282 pages, 5,645 assets
- End-to-end verifier `scripts/verify-redirects.py` passing 268/268

### DNS cutover + verification (2026-04-20)
- DNS records swapped at Squarespace
- Both real domains flipped to "Valid Configuration" in Vercel + SSL cert issued within minutes
- 268/268 verifier pass against live domain (via `scripts/_verify_with_google_dns.py` pattern to bypass stale ISP cache)
- Redirect verifier rate-limit tweaks committed

### Search Console + Analytics (2026-04-20)
- GSC property added as URL-prefix `https://www.functionalpatternsbrisbane.com` (auto-verified via existing Google account association)
- Sitemap submitted: `sitemap.xml` — 178 pages discovered
- GA4 tag `G-6XPMFN4H62` swept across the 15 blog posts that were missing it — all 193 HTML pages now track
- Old Google Ads conversion tag deliberately *not* ported — it was firing sitewide on every pageview (broken setup), so any data in the Ads account was meaningless

### Content corrections (2026-04-21)
- Balance & Symmetry instructor: Harj → Emmanuel (bio, avatar initial, image alt, trainer card)
- Real trainer photos wired up for the 3 active programs:
  - `src/images/emmanuel.webp` → Balance & Symmetry
  - `src/images/keriann.webp` → Bells & Bands
  - `src/images/skye.webp` → Rise & Realign (pulled from the old `/chronicpainexperts` staff page)
- 3 paused programs hidden from nav + listing (pages kept live for direct-link access):
  - Functional Fundamentals
  - Core & Mobility
  - Human Foundations Course
  - Stripped from desktop + mobile nav dropdowns on all 193 HTML pages
  - Removed cards from `/programs`, schema ItemList trimmed, sitemap + llms.txt cleaned
  - Trainer cards on `/programs` page retained (Sam, Keriann, Emmanuel) so the "coaches" section still feels populated
- Fixed pre-existing wrong meta description on `balance-and-symmetry.html` (was describing Bells & Bands)

---

## Currently running programs

| Program | Instructor | Schedule | Page |
|---|---|---|---|
| Rise & Realign | Skye Ashton | Wednesdays 6am | `/programs/rise-and-realign` |
| Balance & Symmetry | Emmanuel | Wednesdays 6pm | `/programs/balance-and-symmetry` |
| Bells & Bands (ladies) | Keriann Zipperer | Thursdays 10am | `/programs/bells-and-bands` |

Paused (pages live but unlinked): Functional Fundamentals, Core & Mobility, Human Foundations. Easy to re-surface by re-adding their nav/listing entries when a program returns.

---

## Monitoring checklist — first 2 weeks

- **GSC → Indexing → Pages** — daily. Expect some temporary "Not indexed" while Google re-crawls. Persistent 404s need investigation.
- **GSC → Performance** — clicks + impressions should hold within ±15% of baseline. Larger drop = investigate.
- **GSC → Sitemaps** — watch "Discovered" → "Indexed" progression over days.
- **GA4 → Reports → Realtime** — sanity check tracking is firing on all page types (home, blog, program, condition).
- **GA4 organic sessions** — week-over-week vs pre-cutover baseline.
- **Spot-check 5–10 high-traffic blog URLs in a browser** over first 3 days.

---

## Rollback plan (still valid if something breaks)

**Fast rollback (DNS):** restore the original Squarespace DNS records. Screenshots of the original DNS state are in the conversation trail from 2026-04-20. DNS reverts within minutes to an hour.

**Partial rollback (redirect or content):** edit `vercel.json` or the relevant page, push to master — Vercel redeploys in under 60 seconds.

**Full site recovery:** Squarespace backup at `backup-squarespace/` has 282 HTML pages + 5,645 assets. Not a live site, but restorable content.

---

## Open follow-ups

1. **GA4 property decision** — currently landing in `G-6XPMFN4H62` (new property, no history). Old Squarespace site used `G-EJGMV7FME4`. If Louis wants multi-year continuity, swap the tag ID site-wide. If the new property was deliberate, leave it.
2. **Google Ads conversion tracking** — the old broken sitewide-firing tag was not ported. If Louis actively runs Ads and needs real conversion attribution, set up proper event-based tracking on actual conversion moments (booking confirmations, contact form submits, ebook downloads).
3. **Blog post CTA in `explosive-power-is-built-on-mechanics-not-just-intensity.html`** still has a "Register for Functional Fundamentals at FP BNE" link (line 151) pointing at the now-hidden program page. Repoint to `/programs` or `/contact` when convenient.

---

## Useful commands

```bash
# Re-run verifier against any host
python scripts/verify-redirects.py https://www.functionalpatternsbrisbane.com

# If local ISP DNS is stale, use the Google-DNS override script pattern
# (create scripts/_verify_with_google_dns.py using dnspython → 8.8.8.8)

# Port additional blog posts later
# 1. Add slug to scripts/blog-urls.txt
python scripts/scrape_blog.py
python scripts/transform_blog_post.py <slug>
python build-blog-seo-pass.py
python build-blog-alt-text.py
```

---

## Known gotchas (kept for reference)

- **Local ISP resolvers lag Vercel's anycast DNS by 10–60 min post-flip.** Symptom: browser shows `DNS_PROBE_FINISHED_NXDOMAIN`, but `dnschecker.org` shows green globally. Fix: switch to `8.8.8.8` or wait for TTL.
- **Vercel DDoS auto-challenges** on bursty verifier traffic. Verifier now runs with 2 workers and 0.4s delay between submissions to stay under the threshold.
- **Blog `amp` slugs** — some old blog URLs contain the literal string `amp` (from `&amp;` in Squarespace title-to-slug transform). Preserved exactly; do not "fix" them.
- **Squarespace email interface** would stop working post-cutover, but Louis uses Google Workspace (MX `smtp.google.com`) so real email was unaffected. Webmail via Squarespace wasn't in use.

---

## Project refs

- **Client:** Louis Ellery (Functional Patterns Brisbane)
- **Repo:** `github.com/woot644/functional-patterns-brisbane` — `master` branch auto-deploys to Vercel
- **Vercel project:** `woot644s-projects/functional-patterns-brisbane` (Pro plan)
- **Live site:** https://www.functionalpatternsbrisbane.com
- **Local path:** `C:\Users\Zac\Python\vibe_coding\functional-patterns-brisbane`
