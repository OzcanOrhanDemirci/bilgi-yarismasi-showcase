# Updating this page

This repository presents Bilgi Yarışması, a private project. `README.md` is the page,
written by hand, English first and the Turkish section at the bottom. No source code of
the app is here: the pictures are shots of the running app, and `tools/` holds only the
scripts that turn those shots into the page's images.

The app speaks Turkish and English, so every picture of it comes in both: the English part
of the page shows `-en` images of an English run, the Turkish section `-tr` images of a
Turkish run (lead loop, diagram, lobby, phones, panel). Alt texts are in their section's
language and quote what their own picture shows.

| What | Where | Rebuild |
| --- | --- | --- |
| Page text, both languages | `README.md` | nothing |
| Section numbers, accent colour | `media/headings/headings.json` | `python tools/headers.py` |
| Architecture diagram, English and Turkish, light and dark | `tools/diagram.py` (boxes and both label sets are in the script) | `python tools/diagram.py` |
| Lead loop per language (projector, one question and the podium) | `media/lead.json`: per language, the recording and the segments kept (the same beats) | `python tools/lead.py` |
| Lobby, phone and panel stills per language | the shot lists in `tools/screens.py` | `python tools/screens.py` |

## Where the shots come from

Every picture comes from two local runs of the app on this PC (2026-11-22), one in each
language, never from the live site: the app's own `wrangler dev` and Vite dev server on
127.0.0.1, a 1920x1080 projector page and 361x782 phone pages in Playwright, with three
scripted phones and twelve bots. Nicknames are plain first names (the phones play as
Çağrı, Işıl and Gökhan). The address under the QR code is the local one, and each PIN
belonged to its local game only.

- Turkish run: browser locale tr-TR, the app's own Turkish sample quiz from its local seed.
- English run: browser locale en-US (the app follows the browser), and an English
  translation of the same sample quiz (same questions in the same order, same answers),
  loaded into a separate local state folder so the app's own local database is untouched.
  The staff panel and the PDF result sheet are English in this run too.

The raw material is in `yerel/` (gitignored, on this PC only): the Turkish recording and
shots in `yerel/host-run.webm` and `yerel/shots/`, the English ones in `yerel/en/` under
the same names. The driver scripts are beside them: `yerel/drive.py` (a copy of the app's
own `scripts/morning-game.py` with the output paths and nicknames changed) and
`yerel/panelphone.py` (the staff panel at phone size), their English copies
`drive-en.py` and `panelphone-en.py` (English locale, labels and quiz), and
`seed-local.mjs` (the app's seed script taking a quiz file and a state folder). They talk
to the app's local dev server and carry its local dev password, so they stay out of git.
To shoot again: start the app's dev servers locally, seed the quiz, run the two scripts of
that language, turn page 1 of the downloaded PDF into `pdf-1.png` (130 dpi), copy the
results into `yerel/` or `yerel/en/`, find the same beats in the new recording for
`media/lead.json`, rebuild. Nothing here ever runs against the live site.

## Before pushing

- `python C:/dev/OzcanOrhanDemirci/tools/preview.py <out> --repo . OzcanOrhanDemirci/bilgi-yarismasi-showcase`
  renders the page through GitHub's renderer on a desktop and a phone, light and dark.
  The phone shots are the measure.
- Keep it light: each language's pictures are about 2 MB, 1.4 MB of it the lead loop.
  The Turkish set sits inside the collapsed section.
- What never goes on this page: the live address, names of the app's Cloudflare
  resources or their IDs, daily limits and caps, password details beyond "one shared
  staff password with an owner override", the deploy guard, known small issues, real
  people's names, anything about the shared Cloudflare account or other projects on it.

## Rules that hold

- Animations are WebP, never animated SVG. GitHub strips JavaScript and CSS.
- Fonts in the images: IBM Plex (SIL Open Font License, `media/fonts/OFL.txt`), as on the
  profile page.
- The Alsancak Gençlik Merkezi logo appears only where the app itself shows it, with the
  ownership notice at the bottom of the page. No ministry logo.
- No LICENSE: nothing here is licensed for reuse.
