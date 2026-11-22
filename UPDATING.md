# Updating this page

This repository presents Bilgi Yarışması, a private project. `README.md` is the page,
written by hand, English first and the Turkish section at the bottom. No source code of
the app is here: the pictures are shots of the running app, and `tools/` holds only the
scripts that turn those shots into the page's images.

| What | Where | Rebuild |
| --- | --- | --- |
| Page text, both languages | `README.md` | nothing |
| Section numbers, accent colour | `media/headings/headings.json` | `python tools/headers.py` |
| Architecture diagram, light and dark | `tools/diagram.py` (boxes and labels are in the script) | `python tools/diagram.py` |
| Lead loop (projector, one question and the podium) | `media/lead.json`: the recording and the segments kept | `python tools/lead.py` |
| Lobby, phone and panel stills | the shot lists in `tools/screens.py` | `python tools/screens.py` |

## Where the shots come from

Every picture comes from one local run of the app on this PC (2026-11-22), never from
the live site: the app's own `wrangler dev` and Vite dev server on 127.0.0.1, the sample
quiz from its local seed, a 1920x1080 projector page and 361x782 phone pages in
Playwright, with three scripted phones and twelve bots. Nicknames are plain first names
(the phones play as Çağrı, Işıl and Gökhan). The address under the QR code is the local
one, and the PIN belonged to that local game only.

The recording and the raw shots are in `yerel/` (gitignored, on this PC only), with the
two driver scripts that made them: `yerel/drive.py` (a copy of the app's own
`scripts/morning-game.py` with the output paths and nicknames changed) and
`yerel/panelphone.py` (the staff panel at phone size). They talk to the app's local dev
server, so they stay out of git. To shoot again: start the app's dev servers locally,
seed the sample quiz, run the two scripts, copy the results into `yerel/`, rebuild.
Nothing here ever runs against the live site.

## Before pushing

- `python C:/dev/OzcanOrhanDemirci/tools/preview.py <out> --repo . OzcanOrhanDemirci/bilgi-yarismasi-showcase`
  renders the page through GitHub's renderer on a desktop and a phone, light and dark.
  The phone shots are the measure.
- Keep it light: the whole page is about 2 MB, 1.4 MB of it the lead loop.
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
