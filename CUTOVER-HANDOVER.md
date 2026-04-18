# Squarespace → Vercel Cutover — Handover

**Paused:** 2026-04-18 evening — Squarespace login blocked (password reset needed).
**Resume trigger:** Squarespace admin access restored.

---

## Current state — what's done

### Content & build (all deployed to Vercel)
- **Full Squarespace backup** at `backup-squarespace/` (gitignored) — 282 pages, 5,645 assets. Restorable if needed.
- **15 missing blog posts ported** from the original migration. All old `/blog-page/<slug>` URLs now resolve on Vercel (blog = 87% of organic traffic, so slug parity is critical).
- **95 explicit 301 redirects** in `vercel.json` covering every old structural slug → new path (conditions, programs, research, team, booking flow, ebook pages, -old duplicates, tag pages, case studies).
- **All canonical / og:url / JSON-LD / sitemap / robots.txt / llms.txt / build-script references** swapped from `functional-patterns-brisbane.vercel.app` to `www.functionalpatternsbrisbane.com` — 2,055 occurrences across 206 files.
- **End-to-end verification:** 268/268 old URLs resolve to 200 on the Vercel deploy (via `scripts/verify-redirects.py`).

### Vercel project settings
- **Deployment Protection:** disabled on production (only preview deployments protected).
- **Domains added:**
  - `www.functionalpatternsbrisbane.com` → Production (primary)
  - `functionalpatternsbrisbane.com` → 308 Permanent Redirect → www
  - `functional-patterns-brisbane.vercel.app` → Production (still active as alias)
- Both real domains currently flag **Invalid Configuration** — expected, DNS hasn't been updated yet.
- **Firewall system bypass rule** active on IP `114.72.34.40` (dev machine) for the verifier.

### Git state
- Branch: `master`
- Latest commits on master, all pushed:
  1. `Squarespace -> Vercel cutover: port 15 blog posts, 95 301 redirects, full backup`
  2. `Fix /research-summaries-functional-patterns redirect`
  3. `Swap vercel.app placeholder to www.functionalpatternsbrisbane.com`
- All Vercel deploys passing.

---

## What's left — in order

### 1. DNS cutover at Squarespace (requires client credentials)

Log into Squarespace → **Settings → Domains** → `functionalpatternsbrisbane.com` → **DNS Settings**.

**Before changing anything, screenshot the existing DNS records** so we can restore in 30 seconds if needed.

Set these two records:

| Type | Name | Value |
|---|---|---|
| **A** | `@` | `216.150.1.1` |
| **CNAME** | `www` | `e7eb037fabed336b.vercel-dns-017.com.` |

**Delete** the existing A records at `@` (4 Squarespace IPs) and the existing CNAME at `www` (probably `ext-sq.squarespace.com`).

**Do NOT touch** MX records (email), TXT records (SPF/DKIM/domain verification), or any other CNAMEs on subdomains. Only A `@` and CNAME `www` change.

### 2. Wait for DNS propagation + SSL issuance
- Vercel auto-detects within minutes to an hour.
- "Invalid Configuration" badges flip to "Valid Configuration" when picked up.
- SSL certificates (Let's Encrypt) issue automatically after validation — another few minutes.

### 3. Re-run verifier against real domain

```bash
python scripts/verify-redirects.py https://www.functionalpatternsbrisbane.com
```

If Vercel's DDoS system challenges the verifier again, create another **System Bypass** rule:
- Firewall → Add New → System Bypass
- IP: `114.72.34.40/32`
- Domain: `www.functionalpatternsbrisbane.com`
- Save

Expected: 268/268 pass.

### 4. Submit sitemap to Google Search Console
- GSC → Sitemaps → Add `https://www.functionalpatternsbrisbane.com/sitemap.xml`
- Re-verify property ownership if needed (DNS TXT method cleanest post-migration).

### 5. Monitor — first 2 weeks
- **GSC Coverage report** daily — expect some temp crawl errors while Google re-indexes; persistent 404s need investigation.
- **GA4 + GSC sessions** — organic traffic should hold within ±15% of baseline. Larger drop = something broken.
- **Key redirects manual spot-check** — first 3 days, hit 5–10 high-traffic old URLs in browser and confirm they land correctly.

---

## Rollback plan (if something goes wrong post-DNS)

**Fast rollback:** restore the original Squarespace DNS records (the ones you screenshotted). DNS reverts within minutes to an hour. Vercel stays live at the `*.vercel.app` URL unaffected.

**Partial rollback:** if only certain redirects misbehave, edit `vercel.json` locally, push to master — Vercel redeploys in under 60 seconds.

**Full site recovery:** the Squarespace backup at `backup-squarespace/` has 282 HTML pages + 5,645 assets. Not a live site but recoverable content.

---

## Useful commands

```bash
# Re-run verifier against any host
python scripts/verify-redirects.py https://<hostname>

# Re-crawl Squarespace (resume-safe — skips already-saved)
python scripts/backup-squarespace.py

# Port additional missing blog posts, if discovered later
# 1. Add slug to scripts/blog-urls.txt
# 2. Scrape via Firecrawl:
python scripts/scrape_blog.py
# 3. Build HTML:
python scripts/transform_blog_post.py <slug>
# 4. Apply SEO passes:
python build-blog-seo-pass.py
python build-blog-alt-text.py
```

---

## Known issues / gotchas

- **Squarespace email:** if client uses `@functionalpatternsbrisbane.com` email through Squarespace, changing the A record doesn't break it — email runs off MX records which we're leaving alone. But if they use Squarespace's webmail interface, that stops working post-cutover. Confirm email setup before flip if unsure.
- **Vercel DDoS auto-challenges** on bursty traffic (~200+ requests/min from one IP). The verifier now runs slowly (2 workers, 0.4s delay) to stay under the threshold. If it fires anyway, the system bypass rule covers us.
- **Blog `amp` slugs:** some old blog URLs contain the literal string `amp` (from `&amp;` in the Squarespace title-to-slug transform). These are preserved exactly — don't "fix" them or you break the URL.
- **`/case-studies/blog-post-title-*`**: Squarespace placeholder test posts. Redirected to `/results`. Safe.
- **3 URLs 404 on Squarespace itself** (already dead at scrape time, no redirect added): `/small-group-class-programs`, `/fpresults`, `/back-pain-brisbane`. Ignored by verifier.

---

## Ambiguous redirects (pending client confirmation — currently pointing at closest topical page)

These were redirected on my lean since the client priority was blog preservation. Review if client wants different behavior:

| Old URL | Currently redirects to | Alternative |
|---|---|---|
| `/the-quiz` | `/book` | Build a quiz page |
| `/free-selfmassage-ebook` | `/blog-page` | Build an ebook landing |
| `/scoliosisebook` | `/conditions/scoliosis` | Build an ebook landing |
| `/case-studies` + `/case-studies/*` | `/results` | Build case-studies section |
| `/cart` | `/` (via implicit home handling) | Drop (410) if no commerce planned |
| `/terms-of-service-online-training` | `/privacy` | Build a `/terms` page |
| `/boxing-for-balance` | `/programs` | Drop |

---

## Contact / context

- **Client:** Louis Ellery (Functional Patterns Brisbane)
- **Project:** `C:\Users\Zac\Python\vibe_coding\functional-patterns-brisbane`
- **GitHub:** `github.com/woot644/functional-patterns-brisbane`
- **Vercel project:** `woot644s-projects/functional-patterns-brisbane` (Pro plan)
- **Squarespace backup:** `backup-squarespace/` (in repo, gitignored — 282 pages, 5,645 assets)
