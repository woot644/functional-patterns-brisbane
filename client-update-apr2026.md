# Functional Patterns Brisbane — Site Update April 2026

## Fixed: Blog 404 Bug

Every blog post was returning a 404 when clicked from the blog index. Traced it to a link-path issue interacting with Vercel's URL handling. Rewrote all 141 blog card links to absolute paths — every post now loads correctly.

## Fixed: Online Training Calendly Links

The hero, Path A "Book Now", and bottom CTA on the Online Training page were sending visitors to the in-person assessment page instead of the Calendly booking. All three now open the correct Calendly link directly in a new tab.

## SEO — Internal Linking

Added a "Further Reading" section to all 11 condition pages linking out to 3 hand-picked, topically relevant blog posts each. Prioritised Brisbane-local articles where possible so they compound the local SEO signal. Result: 33 new high-intent internal links pushing authority from condition pages into the blog (which drives 87% of organic traffic).

## SEO — Structured Data (Schema)

Previously, only the chronic pain page and a handful of others had schema. Now the whole site is covered:

- 10 remaining condition pages — full MedicalWebPage, Service, and FAQPage schema
- Programs hub + 6 program pages — CollectionPage and Service schema
- Team page — AboutPage plus Person schema for all 14 practitioners, including qualifications
- 9 research pages — ScholarlyArticle with author attribution to Louis
- What We Treat, How We Work, Online Training — WebPage, AboutPage, and Service schema with pricing

Coverage is now 35 of 36 non-blog pages (privacy page intentionally skipped). This is what Google's rich results and AI engines like ChatGPT and Perplexity read to understand and cite the business accurately.

## SEO — AI Engine Optimisation

Expanded the site's `llms.txt` file (the file AI engines read to understand a business) from 43 lines to 90. It now includes a full URL list of all condition pages, all research pages, services with pricing, 14 named practitioners with credentials, and a Common Questions section. When ChatGPT, Perplexity or Claude summarise FP Brisbane, they'll have clean, structured source material to cite.

## What This Sets Up

Once old Squarespace URLs are 301'd across to the Vercel site, the existing link equity transfers cleanly onto a site with meaningfully better structured data, internal linking, and AI-discoverability than before.
