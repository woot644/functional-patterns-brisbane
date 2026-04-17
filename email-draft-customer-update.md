# Customer Email — Progress Update + Migration Risk Flag

**To:** [Louis / Keriann]
**From:** Zac, Arclight Digital
**Subject:** FP Brisbane site — audit items complete + an important finding before we switch domains

---

Hey [name],

Thanks for sending through the HubSpot form — that's now live on both the Contact page and the Book page (same pattern as your Squarespace site, with the enquiry form sitting alongside the Cliniko "Book Online" button).

While I was in there I knocked over the rest of the items from the April audit. Quick rundown below, plus **one important finding** I want to flag before we talk about switching the domain across.

### What's now live on the new Vercel build

**From this week's work:**
- **HubSpot lead form** embedded on `/contact` and `/book`
- **WebP image pipeline** — every image on the site is now served as WebP (with JPG/PNG fallback for older browsers). Total image weight 5.2 MB → 3.1 MB, a 40% drop. Pages will feel noticeably faster, especially on mobile.
- **Custom social preview images** — 13 branded 1200 × 630 cards so when someone shares a page on Facebook, LinkedIn, or messaging apps, it renders with a proper preview instead of your logo. Different cards for the homepage, book, results, team, contact, and the top condition pages.

**Earlier sprint items (now also live):**
- Schema structured data (JSON-LD) embedded on every page — the big one for Google AI Overviews and rich results
- Medical disclaimers site-wide
- Author attribution + "Last reviewed" dates on every condition page
- FAQ sections on all 11 condition pages
- Privacy policy page
- Robots.txt, sitemap.xml, and llms.txt deployed
- Meta descriptions, canonical tags, OG tags, Twitter card tags on every page
- Team bios expanded
- Google Maps embed on contact
- Pricing transparency on `/book` (both tiers listed)
- Address unified to 45 Michael Street, Bulimba across the site

The new site would go from roughly 55/100 to 75+/100 on the SEO scorecard once it's live on the real domain.

---

### ⚠️ Important finding — we need to talk before switching domains

I ran a baseline SEO snapshot of the live Squarespace site before the cutover so we'd have a "before" to measure against. The results show you're doing better than I expected — but also uncovered one issue we have to address first.

**The good news:**
- 478 keywords ranking in Google Australia top 100
- 227 of those in the top 10 (47% of the ranked set)
- 11 keywords in position 1
- Roughly $2,350/month in estimated organic traffic value
- You're competing at the content-authority level with Cleveland Clinic, NIH, and Mayo Clinic for queries like "tensor fasciae latae" and "transverse abdominis" — genuinely impressive for a local business
- Backlink profile is clean (134 backlinks, 71 referring domains, low spam) — the strongest single source is your Burleigh Biomechanics sister site

**A surprise upside I didn't expect to find:**

Your site is **completely invisible on ChatGPT.** Zero mentions — even for queries like "tensor fasciae latae" where ChatGPT gets 2,693 searches a month and you already rank #9 on Google for the same query. The cause: your Squarespace site's `robots.txt` has been blocking ChatGPT, Perplexity, and Claude from crawling you since they launched. Your excellent content has been invisible to AI tools the entire time.

The new Vercel build allows all AI crawlers (and includes an `llms.txt` file to help them understand the site). Once we switch domains, the site becomes crawlable by ChatGPT for the first time — and 4–8 weeks after that, you should start appearing in AI answers for queries like "how to fix a neck hump," "scapular winging exercises," and "tensor fasciae latae tight." That's net-new traffic, not just recovered Google traffic.

**The issue:**
**87% of your organic traffic comes from blog articles on `/blog-page/*` URLs — and those articles don't exist on the new Vercel build.**

The top traffic drivers are posts like:
- `/blog-page/posture-workouts-that-actually-work-a-complete-guide` (rank #2 for "posture workout")
- `/blog-page/why-is-my-tensor-fascia-lata-tfl-always-tight` (25 keywords ranking)
- `/blog-page/exercises-for-hyperextended-knees-a-guide-to-strength` (rank #1 for several variations)
- `/blog-page/how-to-fix-scapular-winging-typical-exercises-dont-work` (23 keywords)
- `/blog-page/how-to-fix-neck-humps-a-biomechanical-approach` (rank #3 for "exercises neck hump")

If we switch DNS tomorrow, all of these would 404 on the new site and we'd lose an estimated 80–90% of organic traffic overnight.

**Three options to handle it:**

1. **Port the blog content to the new site.** Best outcome — we keep the URLs (or 301-redirect them) and you don't lose anything. Most work. Realistic: 15–20 hours to port your top 20 articles, or 40+ hours for all 60 or so posts.

2. **301-redirect each blog URL to a thematically similar new page.** For example, `/blog-page/how-to-fix-neck-humps...` → `/conditions/hunchback-posture`. Cheaper — maybe 4–6 hours of mapping and redirect config. We'd keep some of the authority but lose the exact-match rankings (someone searching "exercises neck hump" won't land on a page actually about neck humps).

3. **Run both sites in parallel for now.** Keep the Squarespace blog content live at a subdomain (e.g. `blog.functionalpatternsbrisbane.com`), with the new Vercel build running as the main site at the apex domain. Zero SEO loss, but you keep paying Squarespace a while longer, and the two sites look different from each other.

**My recommendation:** option 3 as a stopgap to get the new site live without risk, then option 1 over the following month — porting your top-performing articles to the new site one at a time, 301-redirecting the old URLs as they land. That way we get the fresh, fast site live immediately without gambling your search traffic.

Happy to jump on a call to talk through it — also happy for you to think on it and come back to me. Either way, we shouldn't switch DNS until we've picked a path.

I've attached a full baseline report (PDF) so you can see exactly what's ranking, where the traffic comes from, what the backlinks look like, and where the AI visibility gap sits. The raw keyword and backlink CSVs are also attached if you want to sort through them yourself.

Cheers,
Zac

---

**Attachments referenced:**
- `baseline-seo-functionalpatternsbrisbane-com-apr2026.pdf` — branded Arclight PDF report (at `C:/Users/zacen/Python/vibe_coding/arclight_digital/audit-reports/`)
- `baseline-keywords-apr2026.csv` — all 478 ranking keywords with position, search volume, landing URL, and estimated traffic value
- `baseline-backlinks-apr2026.csv` — top 30 referring domains

---

**Notes for Zac before sending:**
- Replace `[name]` with Louis or Keriann
- Consider whether to send the full baseline report + CSV as attachments or link via Google Drive. CSV is 478 rows — fine as an attachment.
- Request GSC + GA4 + GBP access in a follow-up (not in this email — keeps the focus on the decision that needs making). Real first-party data will beat DataForSEO estimates for the next pull.
- If she asks for a cost on option 1 (content port): rough estimate 15–20 hrs to port top 20 articles at your hourly rate.
- Vercel build from commit `72fac4c` is live at `functional-patterns-brisbane.vercel.app` — confirm before sending.
