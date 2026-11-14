# Visual homepage restoration: 14 November 2026

The user rejected the shortened multi-page presentation. Restored the preceding
homepage renderer, navigation and CSS, including the large feedback, recognition,
media, research and speaking sections. Retained compact enterprise cards and all
verified November content updates. The three temporary topic URLs now return to
corresponding homepage sections and preserve deep links. Research/profile remain.

## Full-post and photograph review

Fetched the Bluesky public author feed with limit=100. It returned 15 own posts,
from 27 November 2025 to 14 November 2026, and no continuation cursor. Read the
full text of all 15 returned posts. Reviewed attachment metadata for images and
multi-image galleries, including October GLOW, Lloyds and Parliament posts.
Earlier events and the published ReActV/NLDB announcements were already covered;
this restoration does not assert a new exhaustive audit of every older image.

For the two new November events, checked their complete post text and all three
attached photographs:

- Barclays/Cyber London: one panel/audience collage, already downloaded and
  inspected in the preceding update. Now displayed directly in the homepage's
  latest-event area, with a full-post link.
  https://bsky.app/profile/joyjitchat.bsky.social/post/3n24caf3iak25
- Innovation Awards: two images. The awards-screen image was previously included;
  downloaded and visually inspected the omitted portrait at the event backdrop.
  Both are now visible on the homepage: portrait in latest events and screen in
  recognition. Finalist status is retained accurately. No association with other
  sponsor/backdrop logos is inferred.
  https://bsky.app/profile/joyjitchat.bsky.social/post/3n2azgtu67c2z

These are original images from the user's own posts, not generic image-search
results. Added local portrait asset and full provenance/dimensions in media.json.
`spotlight.recent_media` selects the latest event photographs. A link from the
opening goes directly to these photos. The Forbes hero remains unchanged.

Repeated name/event searches surfaced public LinkedIn organiser/profile coverage
and the Innovation Awards nomination list. LinkedIn search results corroborate
context but do not constitute access to the complete authenticated post feed.
No claim of exhaustive LinkedIn, Facebook or X retrieval is made for this focused
restoration. Full Bluesky posts provided the direct event and image evidence.

## Persistent requirements and validation

AGENTS.md explicitly records rejection of the short multi-page design. Added
website-refresh-checklist.md and linked it from the CV refresh report and README.
The required future workflow covers CV completeness, full social posts and all
attachments, awards, speaking/executive events, media, publications/PDFs, dated
metrics and independent research references. Audits must record access gaps and
selection decisions; no claim of literally complete internet coverage is allowed.

41 Python and 13 JavaScript tests passed, including full-homepage content retention,
original event images/source links and compatibility redirects. All six generated
files pass local link/anchor/image checks. Rebuild is deterministic and HTML nesting
is valid. No connected browser was available; rendered visual QA remains unavailable.

## Follow-up: keep the award photographs together

The standing portrait was present under Recent events, but Recognition showed
only the screen photograph. Added the standing portrait beside the screen in
Recognition and made it the lead image in the detailed award entry. The Recent
events portrait remains. Recorded the placement requirement in AGENTS.md.
