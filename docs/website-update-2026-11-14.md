# Website refresh: 14 November 2026

## Structure and preservation

GitHub Pages supports separate HTML pages. The homepage is now an overview rather
than the full portfolio. Six pages share navigation, with the current destination
marked and an existing collapsible mobile menu:

- index.html: Forbes hero, four enterprise highlights, IEA speaking photograph,
  Barclays panel update, two anonymous stakeholder summaries and visual links.
- work.html: all four detailed cases, executive engagements and all six feedback summaries.
- recognition.html: complete visual recognition, award archive and credentials.
- speaking.html: forums, the complete event gallery, videos, interviews and media filters.
- research.html: the Wiley book, large paper preview, independent impact, dated
  metrics, permanent PDF downloads and complete searchable publication list.
- profile.html: complete career records, detail disclosures and print controls.

All previous gallery photographs, public-media cards, full career details,
anonymised feedback and local PDFs are retained. Selected publications remain in
the complete research catalogue. Historical homepage deep links to moved cases,
media cards and research-impact entries route to their new destinations with
JavaScript; section previews and navigation remain normal HTML links.

Measured from generated HTML, excluding script/style text: homepage text reduced
from 5,439 to 583 whitespace-separated words (including the previous disclosures).
Image elements reduced from 38 to 4. This is not a measurement of rendered scroll
height. Full visual detail remains on the destination pages.

## Public discovery and updates

1. Barclays/Cyber London panel: changed from upcoming to completed, based on the
   12 November post-event account. Retained 10 November event date from the earlier
   announcement. Added the original panel collage, speaking entry and homepage
   update. Topic: agentic AI in factories, connected labs and tactical procurement.
   Source: https://bsky.app/profile/joyjitchat.bsky.social/post/3n24caf3iak25
2. Innovation Awards 2026: added Young Innovator of the Year finalist recognition,
   explicitly one of five finalists representing EPAM Systems. Not described as a
   winner or used as the hero. Added original award-screen photograph. The dated
   personal post supports finalist status; the organiser gallery also lists the
   nomination: https://innovation-awards.co.uk/gallery/
   Source: https://bsky.app/profile/joyjitchat.bsky.social/post/3n2azgtu67c2z
3. AAAI 2026: official committee page independently corroborates Program Committee
   membership with EPAM affiliation. Added sourced detail, not a new senior role.
   Source: https://aaai.org/conference/aaai/aaai-26/2026-program-committee/
4. Independent research impact: newly identified a 2023 Journal of Public Health
   commentary by Jan Gresil Kahambing (University of Macau). It references the
   Chatterjee/Dethlefs Patterns paper while discussing conversational AI and public
   health safeguards. Framed as scholarly discussion, not clinical deployment.
   Source: https://doi.org/10.1093/pubmed/fdad028
5. ResearchGate: 40,203 reads observed 14 November. Separate observation dates now
   prevent this update from changing the date of Google Scholar's older snapshot.
   Source: https://www.researchgate.net/profile/Joyjit-Chatterjee

Checked the public Bluesky feed, indexed LinkedIn/organiser coverage, the official
AAAI committee list, publisher sources and LDR publication listing. No new LDR
publication was identified during this pass. Google Scholar returned HTTP 403;
retained the clearly dated 3 November snapshot (964 citations, h-index 12, i10 14).
Existing independent-impact records retain their previous verification date; the
new public-health entry has its own 14 November date.

## Maintenance and verification

Updated AGENTS.md, coverage surfaces and README to preserve the concise homepage
on future updates. The CV importer reviews references on every page and protects
all six generated pages during rollback. CI checks all six committed outputs.

Automated checks cover local paths/anchors, headings, image alternatives, URL
schemes, evidence references, anonymous feedback, retained detail, navigation,
legacy links, filtering, media dialogs, printing and CV-import safeguards.
A deterministic rebuild and HTML nesting check were also performed.

Browser review was unavailable: the computer-use inventory returned no connected
apps or browsers. Mobile layout rules were reviewed in source; no claim of a
rendered desktop/mobile screenshot review is made.
