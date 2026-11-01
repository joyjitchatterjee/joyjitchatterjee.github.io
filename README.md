# Joyjit Chatterjee — CV-driven personal website

A static, accessible portfolio for [joyjitchatterjee.github.io](https://joyjitchatterjee.github.io), with local LinkedIn and Bluesky photos, searchable publications and a printable career profile. No API key or server is exposed to visitors.

## The simplest update: attach your CV in Codex

Open **this repository** in Codex, attach your new PDF or DOCX and say:

> Refresh my website from this CV. Preserve historical achievements and the social-post gallery. Check the changes and publish them to GitHub Pages.

Codex reads `AGENTS.md`, extracts the CV, updates structured content, validates it, rebuilds the pages and follows the requested publishing step. If you only want a draft, say “prepare a draft update” instead. A short CV supplements the existing record; it does not wipe older publications and talks. Supply the full CV too when available.

## Optional single-command import

Requirements: Python **3.10+**, Poppler (`pdftotext`) for PDFs, and an installed, signed-in Codex CLI. Node **20+** runs the small interaction test suite. The build and Python tests need no pip packages. DOCX and text extraction need only Python.

```bash
# macOS: PDF text extraction
brew install poppler

# Generate a proposal and a readable change report
python3 scripts/refresh_cv.py '/path/to/new CV.pdf'

# Generate, validate and apply in one command (updates local files)
python3 scripts/refresh_cv.py '/path/to/new CV.pdf' --apply

# Short CV first, full CV as supporting detail
python3 scripts/refresh_cv.py '/path/to/short.pdf' '/path/to/full.pdf' --apply
```

The script uses your installed Codex CLI and its configured model/account. It sends extracted CV text and current public content to Codex, using a read-only sandbox and a structured response schema. Normal Codex usage limits apply. It needs no separate API key when your CLI is already signed in with a supported account. Set `CODEX_BIN` to your executable path if `codex` is not on PATH. See [OpenAI's non-interactive mode documentation](https://developers.openai.com/codex/noninteractive/).

For use inside an existing Codex chat, avoid starting another CLI process:

```bash
python3 scripts/refresh_cv.py '/path/to/CV.pdf' --prepare-only
```

Read the printed run folder's `prompt.txt`, then have Codex produce `candidate.json` using `content/refresh.schema.json`. Apply it with the actual printed path:

```bash
python3 scripts/refresh_cv.py --run '.cv-refresh/run-EXAMPLE' \
  --candidate '.cv-refresh/run-EXAMPLE/candidate.json' --apply
```

Each private, gitignored run contains the extracted text, baseline, candidate, report and full diff. Unresolved evidence conflicts, duplicate records, invalid links, removed history or a stale baseline stop application. `--allow-removals` is for deliberate, reviewed corrections. CV extraction is not OCR: scanned PDFs require a text-based PDF or DOCX.

**Application and publishing are separate.** The script does not commit or push. Ask Codex to publish, or review and commit the generated changes yourself. Pushing the approved files to `main` uses the existing GitHub Pages configuration. The CI workflow checks content, tests and generated-file consistency; it does not grant new repository permissions or change the hosting setup.

## Preview and verify

```bash
python3 scripts/build.py
python3 scripts/check_site.py
python3 -m unittest discover -s tests -v
node --test tests/site.test.cjs
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765`. Check the homepage, publication search/type filter, mobile menu and print preview. End the server with Ctrl+C. To produce an isolated public-only directory: `python3 scripts/build.py --output dist`. Never expose the repository's development server to the internet: it includes local files.

## Content and design

| Location | Purpose |
| --- | --- |
| `content/profile.json` | Biography, impact, roles, education, publications, talks, awards and other credentials |
| `content/profile.schema.json` | Profile structure and permitted values |
| `content/refresh.schema.json` | Codex response: profile plus notes and unresolved issues |
| `content/media.json` | Curated event photos, alt text, captions and source links |
| `content/sources.json` | Evidence IDs, document hashes and public URLs |
| `templates/base.html` | Shared accessible navigation, metadata and footer |
| `assets/site.css`, `assets/site.js` | Responsive design and progressive interactions |
| `scripts/build.py` | Deterministic, escaped HTML generation |

Publications and the career record are rendered into HTML: readers and search engines do not need JavaScript. Search and type filters work together. The mobile menu has keyboard support and an expanded state; motion respects system preferences. The profile page can be printed or saved as PDF. The existing historical HTML file is retained in Git for reference.

## Adding LinkedIn and Bluesky photos

No additional LinkedIn connection was needed for the initial portrait and Loughborough lecture image. They were downloaded from a public post and visually checked; original links are in the content files. Images are served locally so an expiring LinkedIn image URL cannot break the portfolio.

For more photos, give Codex a specific post URL. If LinkedIn blocks public access, open the post in a connected browser where you are already signed in, or provide the image and post link directly. Do not share passwords or cookies. The current LinkedIn people-search connector cannot read all your posts or download their images. There is no unattended LinkedIn scraper or scheduled feed synchronization in this project.

Bluesky is also a source: [joyjitchat.bsky.social](https://bsky.app/profile/joyjitchat.bsky.social).
Public posts and images were accessible without login. The gallery now includes
the GLOW/ISWC presentation, House of Lords visit and Queen Mary invited talk,
with direct source links and accurate attendance/speaking labels. The GLOW photo
confirms the presentation date as 25 October 2026. The existing Loughborough
LinkedIn photo is retained. Bluesky also corroborates that ReActV was an ABIS
workshop contribution, rather than a main-conference presentation.

Codex can consult Bluesky during later updates using the public author-feed API
documented in `AGENTS.md`. This is an on-demand evidence source, not a scheduled
feed mirror. Only relevant professional material is curated into the portfolio.

To add a photo manually: save it in `assets/images/`, add an entry to `content/media.json` matching the existing record, then build. Keep the event's actual date/role, an accurate alt description, the image width and height, and a link to the originating post. CV updates preserve this gallery.

## Initial update (1 November 2026)

The October short CV and supplied full CV informed this refresh. Added 2026 research contributions, the 2025 book chapter, August 2026 certifications and newer appearances. The 10 November 2026 Barclays/Cyber London panel is upcoming; the House of Lords entry is attendance as an invited guest. Financial benefits remain potential savings. Historical records were retained from the prior website, with their original source tracked where not individually reconciled.

Automated checks are not a factual guarantee: review the report for role/date changes, ambiguous publications and confidential material before publication. The raw CVs are deliberately not downloadable from the public website.

## Leadership positioning and coverage audit

The homepage now connects enterprise AI strategy, product development and
operational adoption to specific work at EPAM and Reckitt. It features the ETH
aptitude-colloquium invitation, British Data Awards finalist listing, Loughborough
appointment, public interviews, recordings, Wiley book and GitHub research.

- `content/showcase.json` and its schema: curated case studies and public appearances.
- `content/coverage.json`: selected important credentials protected against silent loss.
- `docs/content-audit.md`: CV coverage, corrections, public sources and deliberate omissions.
- `scripts/showcase.py`: homepage rendering; the existing three-page structure is retained.

For future updates, the Codex workflow also reviews the curated homepage against
the new CV. The standalone importer preserves curated cards and images, includes
them in the extraction context, and reports changed source records for editorial
review. It does not autonomously rewrite media or case-study prose. The record
checks prevent known highlights from disappearing; they do not replace reading
all sections of each newly supplied CV.

## Summaries with full detail

Each career record can contain sourced `details` groups (a heading and points).
Readers can open individual entries or use **Expand all details** on the profile.
Links from homepage case studies open the corresponding full career entry.
Printing expands all detail and restores the reader's previous state afterwards.
The native disclosures work without JavaScript; expanding all entries, automatic
opening from links and print-state restoration are progressive enhancements.

Homepage case-study details are rendered from the profile itself. Future CV
imports preserve these groups and reject silent reductions in their point counts,
as well as deleted historical records. Protected highlights remain in the coverage
ledger. The full archive now includes the CV's technical skills, named corporate
involvement, funding, CPD events and earlier awards alongside major achievements.

## Shareable publication PDFs

Visit [Publication downloads](https://joyjitchatterjee.github.io/research.html#downloads)
to read, download or copy a permanent link to selected papers. The GLOW 2026 paper
is stored unchanged at `assets/papers/glow-2026-power-line-om.pdf`, with its original
source and CC BY 4.0 attribution retained.

Give Codex a paper PDF or direct PDF URL and ask to add it to publication downloads.
It can save the file, inspect it, render a first-page preview and register metadata
in `content/downloads.json`. Builds check the publication reference, file location,
PDF signature, byte count and SHA-256. CV imports preserve this collection, and
isolated builds copy the PDFs with the other public assets.

GitHub is now a footer link and optional supporting resource on the research page.
It is no longer a primary navigation action or homepage section.
