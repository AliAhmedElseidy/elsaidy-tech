# ELSAIDY TECH

Independent, bilingual, production-oriented **static corporate website** for `https://tech.elsaidy.org`.

- 34 standalone semantic HTML pages in Arabic and English
- Responsive custom interface, no account, database, API or admin panel
- SEO: unique metadata, canonical URLs, hreflang, XML sitemap, Organization structured data
- Case studies link to supplied real project websites, without invented metrics or testimonials
- Minimal JavaScript: **none** (native mobile menu)

## Cloudflare Pages deployment

1. In Cloudflare Pages connect **only** `AliAhmedElseidy/elsaidy-tech`.
2. Framework preset: **None**. Build command: **leave blank**. Output directory: **site**.
3. Preview the Pages temporary domain, test both languages and mobile navigation.
4. Add custom domain `tech.elsaidy.org` *only when you approve deployment*. Do not modify family site DNS.
5. Verify Search Console, submit `https://tech.elsaidy.org/sitemap.xml`.

## Content editing

Edit the HTML in `site/` directly, and `site/assets/styles.css` for design. No build tools are required.

## Before going live

- **Verify that `info@elsaidy.org` receives enquiries.** It appears in contact CTA until confirmed or replaced.
- Confirm consent to showcase client projects and verify their website URLs.
- Replace conceptual project panels with approved real screenshots where available; no fake images are included.
- Update KFATA link after the client's domain transfer.
- Confirm Saudi legal entity and address information before claiming registration; current copy identifies a founder-led brand only.
- Review legal pages for business-specific requirements.
- Current pages use Google Fonts CSS; for maximum privacy/performance, self-host licensed fonts or use a system stack.

## Validation

All HTML is already rendered and crawlable; no SSR service required. Can be served locally:
```bash
python3 -m http.server 8000 --directory site
```

## Automated site validation

On push and pull requests, `.github/workflows/site-check.yml` runs `python3 scripts/check_site.py` to validate all generated HTML pages, title/description metadata, canonical/hreflang links, local navigation and sitemap consistency. Run it locally before publishing. A passing static check does not replace browser or Lighthouse testing.

## Content quality

Four article pages now include extended bilingual practical guidance, without unverified client results, ratings or fabricated testimonials. The portfolio uses brand-style typographic panels rather than screenshots; replace these with genuine approved screenshots before presenting them as site captures.
