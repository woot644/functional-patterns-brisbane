# Reply to Keriann — April 2026

**Subject:** Re: FP Brisbane site — fixes pushed

---

Hey Keriann,

Thanks heaps for the feedback — really glad the flow is landing well, and massive thanks for flagging the 404s. You were right, there was a genuine bug.

**Blog 404s — fixed:** All the blog post cards on `/blog-page` were using relative links, which broke when combined with how Vercel serves the page. Clicking any post was sending you to the root domain instead of the blog folder. I've rewritten all 141 links to absolute paths, so every post should now click through cleanly once the new build deploys.

**Online training → Calendly — fixed:** The hero, Path A "Book Now", and bottom CTA on `/online` were pointing at the 1-on-1 assessment page. They now open your Calendly directly in a new tab:

`https://calendly.com/d/cxcf-xg5-99f/initial-biomechanics-consultation-90`

If you'd rather route online enquiries through the individual trainer meet-and-greets (Pietro / Gavin / Steve) just say the word.

**SEO:** Hearing you — plenty of room to move here. I've got the pre-cutover baseline and will do a proper pass once the blog migration has had a week or two to get indexed. Internal linking from the conditions pages into the relevant blogs is the easiest win, and I'll also look at AI-engine-specific structured data so your content has a better shot at surfacing there.

Cheers,
Zac
