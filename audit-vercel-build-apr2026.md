# Comprehensive Website Audit — Vercel Build
## Functional Patterns Brisbane
**functional-patterns-brisbane.vercel.app**
**Prepared by Arclight Digital** | 16 April 2026

---

## Executive Summary

**Overall Score: 55/100 — Needs Work (improving)**

The custom Vercel build scores **7 points higher** than the Squarespace site (48/100), with major structural wins: clean URL architecture (35 pages vs 258 with 30% junk), no AI crawler blocking, static HTML rendering, and well-written condition pages scoring 64-74 on E-E-A-T. However, the build has a critical "last mile" problem — **schema JSON-LD files are fully written but not embedded in any HTML page**, OG meta tags are completely absent, images have zero optimisation attributes, and the contact form doesn't actually submit. The good news: most fixes are deployment tasks, not content rewrites.

**Rating scale:**
- 80-100: Excellent — well-optimised, minor refinements available
- 60-79: Good — solid foundation with clear improvement opportunities
- 40-59: Needs Work — several issues limiting online performance
- 0-39: Critical — urgent issues requiring immediate attention

---

## Score Breakdown

| Category | Score | Status | vs Squarespace (48/100) |
|----------|-------|--------|------------------------|
| Technical SEO | 10/15 | Fair | +2 (cleaner URLs, no junk) |
| On-Page SEO | 10/15 | Fair | +1 (better titles, same OG gap) |
| Content Quality | 9/15 | Needs Work | +1 (stronger condition pages) |
| Speed & Performance | 7/12 | Fair | Same (no image optimisation) |
| Google Business Profile | 4/10 | Poor | Same (address conflict persists) |
| Backlink Profile | N/A | Not assessed | — |
| Keyword Visibility | N/A | Not assessed | — |
| Schema & Structured Data | 1/5 | Critical | Same (written but not deployed) |
| Mobile & Images | 2.5/5 | Poor | Same (zero OG, zero lazy load) |
| Sitemap & Crawl Health | 2.5/4 | Fair | +0.5 (clean sitemap created) |
| AI Search Readiness | 1.5/3 | Poor | +0.5 (crawlers not blocked) |
| **TOTAL (estimated)** | **55/100** | **Needs Work** | **+7 from Squarespace** |

*Backlink and keyword data requires DataForSEO API connection. Weight redistributed proportionally for estimated score.*

---

## Detailed Findings

### 1. Technical SEO — 10/15

**Improvements over Squarespace:**
- Clean URL structure: 35 purposeful pages vs 258 with 30% junk
- No "-old" duplicates, no hash-slug drafts, no utility pages in sitemap
- Static HTML — no JavaScript rendering dependency
- AI crawlers NOT blocked (Squarespace blocked all of them)
- Vercel provides HTTP/2, edge CDN, and HTTPS by default

**Issues found:**

| Issue | Severity | Detail |
|-------|----------|--------|
| No robots.txt on live site | High | Returns 404. Created in source repo during audit but not yet deployed. Default "allow all" applies, but explicit is better. |
| No sitemap.xml on live site | High | Returns 404. Created a 35-URL sitemap in source repo — needs deployment. |
| No canonical tags on any page | High | No `<link rel="canonical">` anywhere. Critical before production domain switch to prevent duplicate content between vercel.app and production domain. |
| No /research index page | Medium | 9 research sub-pages exist but /research returns 404. No hub page linking them. |
| Contact form doesn't submit | Critical | `action="#"` — form data goes nowhere. Must connect to a real endpoint before launch. |

**Recommendations:**
1. Deploy the new robots.txt and sitemap.xml (created during this audit in source repo)
2. Add canonical tags to every page before domain switch
3. Fix contact form with a real endpoint (Formspree, Netlify Forms, or backend handler)
4. Create a /research index hub page

---

### 2. On-Page SEO — 10/15

**Improvements over Squarespace:**
- All condition page titles include "Brisbane" (e.g., "Chronic Back Pain Treatment Brisbane | Functional Patterns Brisbane")
- Clean, descriptive meta descriptions on all key pages
- Logical H1 > H2 > H3 hierarchy on all pages
- 2-click depth maximum from homepage to any content page

**Issues found:**

| Issue | Severity | Detail |
|-------|----------|--------|
| Zero OG/social meta tags on all 20 pages | Critical | No og:title, og:description, og:image, or twitter:card on any page. Social shares render with no preview image or description. |
| Homepage H1 missing "Brisbane" | High | H1 is "Correct Your Pain & Posture at the Deepest Level" — no location keyword. |
| No privacy policy page | Medium | Required under Australian Privacy Act for sites collecting personal health data via contact form and booking system. |

**Title tag audit:**

| Page | Title | Status |
|------|-------|--------|
| Homepage | Functional Patterns Brisbane — Biomechanics & Posture Specialists | Good |
| Chronic Pain | Chronic Back Pain Treatment Brisbane \| Functional Patterns Brisbane | Good |
| Scoliosis | Scoliosis Treatment Brisbane — Without Surgery \| FP Brisbane | Good |
| Book | Book Assessment — Functional Patterns Brisbane | Good |
| Contact | Contact — Functional Patterns Brisbane | Adequate |
| Team | Our Team — Functional Patterns Brisbane | Adequate |
| Results | Results — Functional Patterns Brisbane \| Case Studies & Testimonials | Good |

**Recommendations:**
1. Add OG meta tags to all pages (duplicate existing title/description into og: equivalents)
2. Use fp-logo-full.jpg as fallback og:image until custom 1200x630 images are generated
3. Set twitter:card to summary_large_image on all pages
4. Add "Brisbane" to homepage H1
5. Create a privacy policy page and link from footer

---

### 3. Content Quality — 9/15

**Site-wide E-E-A-T: 64/100** (up from ~58 on Squarespace)

| Page | Words | E-E-A-T | AI Citation | Key Strength |
|------|-------|---------|-------------|-------------|
| Homepage | ~480 | 62/100 | 45/100 | Stats strip, 3 testimonials |
| Chronic Pain | ~950 | 65/100 | 65/100 | 4 named case studies with specific diagnoses |
| Scoliosis | ~950 | 66/100 | 68/100 | Cobb angle data, surgery comparison table |
| Team | ~700 | 57/100 | 28/100 | Weakest page — 7 boilerplate practitioner bios |
| Results | ~900 | 74/100 | 78/100 | Strongest page — measurable outcomes, named athletes |
| Book | ~550 | 63/100 | 42/100 | Below 800-word service page floor |
| Contact | ~250 | 60/100 | 20/100 | Strong trust signals, but broken form |

**Key issues:**

| Issue | Severity | Detail |
|-------|----------|--------|
| No medical disclaimers anywhere | Critical | YMYL site advising on surgery avoidance and paediatric scoliosis treatment with zero disclaimers. Google's QRG requires "clear information about who is responsible for the content and that appropriate care has been taken." |
| No publication/review dates on any page | High | No page carries any date. Critical for YMYL health content freshness signals. Copyright year 2026 is not a substitute. |
| Team page: 7 practitioners with boilerplate bios | High | Near-identical descriptions like "delivering biomechanics-based training to help clients move and feel better." No practitioner photos — initials-only avatars. Owner Louis Ellery's credentials underspecified ("former physiotherapy background" — no degree, registration, or years). |
| No author attribution on condition pages | High | Louis Ellery named only on research summaries. Condition pages making health claims have no byline. |
| No outbound research citations on condition pages | Medium | 9 research summaries cite peer-reviewed journals but aren't cross-linked from condition pages. The chronic pain page critiques massage, chiro, and acupuncture as ineffective without any supporting citation. |
| Book page below word floor | Medium | ~550 words vs 800-word minimum for service pages. No pricing transparency. |
| Duplicate intro paragraph on chronic pain page | Low | Hero section repeated verbatim as Section 1 opening. |

**Recommendations:**
1. Add medical disclaimer to footer and all condition pages
2. Add "Written by Louis Ellery | Last reviewed: April 2026" to condition pages
3. Expand team bios with individual-specific information and add real photos
4. Cross-link research pages from relevant condition pages
5. Add dates to all content pages
6. Add pricing info or price range to the book page

---

### 4. Speed & Performance — 7/12

**Improvements over Squarespace:**
- Static HTML = near-zero server response time
- No CMS framework overhead
- Vercel edge CDN provides global distribution
- No third-party script bloat
- Average image file size: 86KB (reasonable)

**Issues:**

| Issue | Severity | Detail |
|-------|----------|--------|
| Zero lazy loading | High | No `loading="lazy"` on any of 43+ images. Every image loads immediately. |
| Zero responsive srcset | High | Full-resolution images served to all devices. Mobile users download desktop-size images. |
| Zero WebP/AVIF | High | 100% JPEG/PNG. Expected 25-35% file size savings from WebP conversion. |
| Zero width/height on images | Medium | Causes Cumulative Layout Shift (CLS). Browser can't reserve space. |
| 2 images over 200KB | Low | gait-analysis.jpg (201KB), book-hero.jpg (204KB). |

**Recommendations:**
1. Add `loading="lazy"` to all below-the-fold images, `loading="eager"` for hero images
2. Add explicit `width` and `height` attributes to all `<img>` tags
3. Implement WebP conversion pipeline at build time (sharp or imagemin)
4. Add `srcset` and `sizes` with 4-5 breakpoints
5. Add `fetchpriority="high"` to hero images

---

### 5. Google Business Profile — 4/10

**Critical issues (same as Squarespace audit):**

| Issue | Severity | Detail |
|-------|----------|--------|
| Address conflict | Critical | This site: "3 Manilla Street, East Brisbane QLD 4169". Live Squarespace: "45 Michael Street, Bulimba QLD 4171". Must be resolved before domain switch. |
| Hours mismatch | High | This site: Mon-Fri 7am-8pm, Sat 7am-3pm, Sun 7am-1pm. Squarespace: Mon-Fri 6am-7pm, Sat 6am-3pm, no Sunday. |
| No Google Maps embed | High | Contact page has address text but no map — critical GBP reinforcement signal missing. |
| Contact form broken | Critical | `action="#"` — enquiries go nowhere. |
| No Google review widget | Medium | 130+ reviews claimed but displayed as static HTML, not live feeds. |
| Cliniko URL mismatch | Medium | Booking system references "impulse-rehab-centre" — different business name. |

**Improvement:** NAP is at least consistent across all pages within this build.

**NAP Consistency (within Vercel build):**

| Source | Address | Phone | Match |
|--------|---------|-------|-------|
| Homepage footer | 3 Manilla St, East Brisbane 4169 | 0433 801 181 | Consistent |
| Contact page | 3 Manilla St, East Brisbane 4169 | 0433 801 181 | Consistent |
| Book page footer | 3 Manilla St, East Brisbane 4169 | 0433 801 181 | Consistent |
| Schema files | 3 Manilla St, East Brisbane 4169 | +61433801181 | Consistent |

**Recommendations:**
1. Confirm correct address and update GBP + all citations before domain switch
2. Add Google Maps embed to contact page
3. Fix contact form with real endpoint
4. Add "Leave us a Google Review" CTA link

---

### 6-7. Backlink & Keyword Visibility — Not Assessed

DataForSEO MCP server not connected this session. To complete, reconnect and run domain overview, ranked keywords, backlink summary, and competitor analysis.

**Target keywords to track:**
- "functional patterns brisbane" (branded)
- "chronic pain brisbane" / "back pain brisbane"
- "posture correction brisbane"
- "scoliosis treatment brisbane"
- "biomechanics brisbane"
- "gait analysis brisbane"

---

### 8. Schema & Structured Data — 1/5

**The "last mile" problem:** Six well-constructed JSON-LD schema files exist in `/src/schema/` but are NOT embedded in any HTML page.

**Schema files in repo:**

| File | Types | Quality |
|------|-------|---------|
| schema-homepage.json | HealthAndBeautyBusiness, AggregateRating, WebSite | Good |
| schema-resolve-chronic-pain.json | MedicalWebPage, Service, FAQPage (3 Qs) | Good |
| schema-book-assessment.json | Service | Good |
| schema-case-studies.json | Reviews, AggregateRating | Good |
| schema-contact.json | LocalBusiness | Good |
| schema-blog-research.json | Article | Good |

**URL mismatches in schema (must fix before embedding):**

| Schema URL | Actual Page Path |
|------------|-----------------|
| /book-an-assessment | /book |
| /resolve-chronic-pain | /conditions/chronic-pain |
| /case-studies | /results |

**Missing schema not yet written:**
- BreadcrumbList (for all pages)
- Person (for team page practitioners)
- Service (for individual condition pages beyond chronic pain)

**Recommendations:**
1. Fix URL mismatches in schema files
2. Embed each schema file as `<script type="application/ld+json">` in corresponding page `<head>`
3. Generate BreadcrumbList and Person schema for remaining pages
4. Verify geo coordinates match exact building address (currently 4 decimal places — needs 5)

---

### 9. Mobile & Images — 2.5/5

**Image audit summary:**

| Metric | Value | Status |
|--------|-------|--------|
| Pages with OG images | 0/20 | Critical |
| WebP/AVIF adoption | 0% | Fail |
| Lazy loading | 0/43 images | Fail |
| Width/height attributes | 0/43 | Fail |
| Responsive srcset | 0/43 | Fail |
| Alt text present | 100% | Pass |
| Alt text meaningful | ~73% | Warn |
| Generic alt="Training" | 11 instances | Fail |
| Broken/truncated alt text | 2 (& character bug) | Fail |
| Average file size | 86KB | Pass |

**Broken alt text (& character bug):**
- `/programs/balance-and-symmetry`: `alt="Balance &amp; at Functional Patterns Brisbane"` — "Symmetry" is missing
- `/programs/core-and-mobility`: `alt="Core &amp; at Functional Patterns Brisbane"` — "Mobility" is missing

**OG image generation plan (20 images needed):**

| Priority | Pages | Count |
|----------|-------|-------|
| Critical | Homepage, /book, /results | 3 |
| High | /conditions/chronic-pain, /team, /contact, /conditions/scoliosis, /conditions/posture-correction | 5 |
| Medium | Remaining conditions (/joint-pain, /athletes, /hunchback-posture, /gait-running, /kids-teens, /diastasis-recti) | 6 |
| Low | /conditions/fascia, /conditions/winged-scapulas, 4 program pages | 6 |

**Recommendations:**
1. Fix broken alt text on program pages (& character issue)
2. Replace 11 generic alt="Training" with descriptive, page-specific text
3. Add `loading="lazy"` and `width`/`height` to all images
4. Generate OG images starting with Critical priority pages
5. Convert to WebP with JPEG fallback via `<picture>` elements

---

### 10. Sitemap & Crawl Health — 2.5/4

**Created during this audit (in source repo, not yet deployed):**

**robots.txt:**
```
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://functional-patterns-brisbane.vercel.app/sitemap.xml
```

**sitemap.xml:** 35 URLs across 4 sections:

| Section | Count |
|---------|-------|
| Core pages (/, /book, /contact, /how-we-work, /what-we-treat, /results, /team, /programs, /online) | 9 |
| Conditions | 11 |
| Programs (sub-pages) | 6 |
| Research | 9 |
| **Total** | **35** |

All 35 URLs return HTTP 200. lastmod dates sourced from git commit history. No duplicate or junk pages.

**vs Squarespace:** 35 clean URLs vs 258 URLs with 25 "-old" duplicates, 6 near-duplicate blog pairs, 8 hash-slug drafts, 12 thin tag pages, 5 utility pages, and 2 broken 404s.

---

### 11. AI Search Readiness — 1.5/3

**GEO Score: 54/100** (up from 29/100 on Squarespace)

**AI platform visibility:**

| Platform | Score | vs Squarespace |
|----------|-------|----------------|
| Google AI Overviews | 40/100 | +35 (not blocked) |
| ChatGPT Search | 52/100 | +47 (not blocked) |
| Perplexity | 58/100 | +53 (not blocked) |
| Bing Copilot | 38/100 | +26 |
| Claude | 52/100 | +47 (not blocked) |

**Key improvement:** AI crawlers are no longer blocked. Squarespace's robots.txt blocked GPTBot, ClaudeBot, PerplexityBot, Google-Extended, and OAI-SearchBot. This build allows all of them.

**Remaining gaps:**

| Issue | Severity | Detail |
|-------|----------|--------|
| No llms.txt | High | AI systems have no structured declaration of business identity or preferred citation format. |
| Schema not embedded | High | FAQPage schema for chronic pain exists in files but is invisible to crawlers. |
| No FAQ HTML markup | High | CSS for `<details>` elements exists in condition page stylesheets but no actual `<details>` elements in the markup. |
| Passage length suboptimal | Medium | Blog sections average 45-90 words — below 134-167 word optimal AI citation window. |
| No sitemap for AI crawlers | Medium | Created but not yet deployed. |

**Estimated score with easy fixes:** Embedding schema + deploying robots.txt/sitemap + creating llms.txt would push GEO score to approximately **72-75/100**.

---

## Squarespace vs Vercel Build — Full Comparison

| Factor | Squarespace (48/100) | Vercel Build (55/100) | Winner |
|--------|---------------------|----------------------|--------|
| AI crawler access | All blocked | All allowed | Vercel |
| URL structure | 258 URLs, 30% junk | 35 clean URLs | Vercel |
| Content rendering | SSR (Squarespace CMS) | Static HTML | Vercel |
| Schema markup | Zero | Written but not deployed | Tie (both zero effective) |
| OG/social tags | 2/6 pages (poor quality) | 0/20 pages | Squarespace |
| Image optimisation | Auto CDN (WebP, lazy, srcset) | Zero optimisation | Squarespace |
| Sitemap health | 258 URLs, 2 broken, 25 dupes | 35 clean URLs (not yet deployed) | Vercel |
| Content depth | Good on existing pages | Good, more structured | Vercel |
| E-E-A-T score | ~58/100 | ~64/100 | Vercel |
| Medical disclaimers | None | None | Tie |
| Privacy policy | None | None | Tie |
| Contact form | Works (Squarespace handles) | Broken (action="#") | Squarespace |
| Blog content | 65+ posts (live) | Zero blog posts | Squarespace |
| Local SEO score | 44/100 | 41/100 | Squarespace |
| GEO / AI readiness | 29/100 | 54/100 | Vercel |
| NAP consistency | Conflict between sites | Consistent within build | Vercel |

---

## Prioritised Action Plan

### Critical (Fix Before Launch)

1. **Embed schema JSON-LD into HTML pages** — The files exist in `/src/schema/`. Copy each into the corresponding page's `<head>` as `<script type="application/ld+json">`. Fix URL mismatches first (/book-an-assessment -> /book, /resolve-chronic-pain -> /conditions/chronic-pain, /case-studies -> /results). Estimated effort: 30 minutes. Single highest SEO impact.

2. **Fix the contact form** — `action="#"` sends enquiries nowhere. Connect to Formspree, Netlify Forms, or a backend handler. Users who submit get no confirmation and their message is lost.

3. **Add medical disclaimers site-wide** — YMYL site advising on surgery avoidance needs: "Individual results vary. This content is for educational purposes. Consult a qualified health professional before making changes to your health management."

4. **Resolve the address conflict** — Confirm whether the business is at 3 Manilla Street East Brisbane or 45 Michael Street Bulimba. Update GBP, all directory citations, and whichever site has the wrong address simultaneously. Do not let both addresses be live at the same time.

### High Priority (This Week)

5. **Deploy robots.txt and sitemap.xml** — Created during this audit in source repo. Push to trigger Vercel deployment.

6. **Add OG meta tags to all pages** — Each page has good `<title>` and `<meta description>`. Duplicate into og:title, og:description. Use fp-logo-full.jpg as fallback og:image. Set twitter:card to summary_large_image.

7. **Add canonical tags to every page** — `<link rel="canonical" href="https://[production-domain]/[path]">` — critical before domain switch.

8. **Add `loading="lazy"` and width/height to all images** — One attribute per tag. Biggest quick-win for CWV performance.

9. **Add Google Maps embed to contact page** — Use the GBP Place ID embed beneath the contact details card.

10. **Create and deploy llms.txt** — Draft provided by the GEO audit agent.

### Medium Priority (This Month)

11. **Add FAQ `<details>` sections to condition pages** — CSS already exists in the stylesheets, just needs HTML markup. 3-5 questions per page. Targets AI Overview and featured snippet eligibility.

12. **Expand team page bios** — Rewrite 7 boilerplate descriptions with individual-specific information. Add real practitioner photos. Specify Louis Ellery's full credentials (degree, registration, years).

13. **Add author attribution and dates to condition pages** — "Written by Louis Ellery | Last reviewed: April 2026"

14. **Convert images to WebP, add srcset** — Build pipeline with sharp or imagemin. Generate 4-5 size variants per image.

15. **Create a privacy policy page** — Required under Australian Privacy Act. Link from footer.

16. **Cross-link research pages from condition pages** — The 9 research summaries citing peer-reviewed journals are currently siloed and only reachable from the Results page sidebar.

### Quick Wins

- Add "Brisbane" to homepage H1
- Fix 2 broken alt texts (& character bug on balance-and-symmetry and core-and-mobility program pages)
- Replace 11 generic alt="Training" with descriptive text
- Fix duplicate intro paragraph on chronic pain page
- Create /research index hub page
- Add pricing transparency to /book page
- Clarify "impulse-rehab-centre" relationship on the booking page

---

## Path to 75+ Score

| Fix | Estimated Score Impact | Effort |
|-----|----------------------|--------|
| Embed schema JSON-LD | +6-8 points | 30 minutes |
| Deploy robots.txt + sitemap | +2-3 points | 5 minutes (git push) |
| Add OG meta tags | +3-4 points | 1-2 hours |
| Fix contact form | +1-2 points | 30 minutes |
| Add medical disclaimers | +1-2 points | 30 minutes |
| Add lazy loading + width/height | +2-3 points | 1 hour |
| Add canonical tags | +1 point | 1 hour |
| Add FAQ HTML sections | +2-3 points | 2-3 hours |
| Create llms.txt | +1-2 points | 30 minutes |
| **Total potential** | **+19-27 points → 74-82/100** | **~8-10 hours total** |

The site can reach 75+ with approximately one focused sprint of work. The foundations are strong — the remaining work is almost entirely technical deployment, not content creation.

---

*Audit conducted by Arclight Digital — arclightdigital.com.au*
*Contact: zac@arclightdigital.com.au*
