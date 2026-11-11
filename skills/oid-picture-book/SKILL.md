---
name: oid-picture-book
description: Create talking-pen book pages or experimental OID2/OID3 dot patterns, layered print files, mapping plans, and printer tests; use for OID point-reading and custom audio stickers, not generic QR codes.
---

# Talking-pen picture books and OID experiments

Identify the pen model and firmware, code family, audio binding method, and printer if available. Make useful progress on page design without them. Never equate a sticker's visible label with a raw OID; never claim compatibility from the extension BNL or the label OID alone. Back up existing pen files before changing anything, and check before overwriting an audio assignment.

For illustrations use the environment's image-generation tool if available, with requested characters and style. Build full-bleed illustration first, then add exact text separately in the requested font in organic light space; keep text, art, and code independently editable. Preserve user-provided story wording unless changes are requested. Distinguish visual mockups from actually encoded, device-tested materials.

For research read [references/compatibility.md](references/compatibility.md). The bundled scripts/oid_lab.py generates candidate bitmaps by isolated emulation of specific routines in a user-supplied Windows film generator. It is not an independent, fully verified OID encoder. It requires Python, Pillow, Unicorn and a source ZIP/EXE matching the built-in SHA-256.

Run scripts/oid_lab.py with --source /path/to/original.zip --type 2 or 3 --code 1001 --output sample.png. Output is 1-bit PNG, 1200 dpi metadata, 64-pixel repeated cells and default width 1536 px. These are unverified research candidates: one tested OID2 reference differs at a marker after alignment; no complete OID3 film or device comparison has been completed. Deliver with these limits. Do not rescale, blur, alpha-fade, compress lossily, or bake microdots into a lower-resolution raster. Overlay only after resolving resolution, inks, layering, target device and control sample.

Separate code generation, print/optical recognition, and firmware/audio binding. A code image does not contain narration. Give a minimal print test with a known working manufacturer control, an unmodified code-only region and an illustrated region at original physical size. Back up and avoid changing pen data during recognition-only testing.

For 小彼恩毛毛虫, use the official DIY audio sticker workflow when the specific model supports it: REC plus actual complete sticker ID and .mp3 into DIYAUDIO; first test one unused sticker. Official USB instructions exclude the 2022 reading/listening all-in-one; verify the exact model. Albi BNL compatibility with 毛毛虫 is unverified. Do not write to a device as though compatible.
