STATUS: Retained source exports; not loaded by the current site.
The runtime notes below describe the optional renderer if it is re-enabled.

Source: supplied FINAL_MARC/02_BLENDER/MARC_FINAL.blend.
Snowman: MK_snowman_* mesh/curve objects, excluding the powder detail duplicates.
Crystal: V19 / embedded crest crystal 00 / branched hexagonal ice core.
Original geometry retained. Procedural materials replaced by lightweight blue/white
vertex colors; snowman's scarf adapted from red to blue to match the LP.
These are real meshes rendered with WebGL, not rotating image cards.

Reproduce with scripts/export-winter-decor.py (Blender, four CPU threads).
Binary format, little endian: uint32 vertex count + uint32 index count;
16-byte vertex: 3 x signed normalized int16 position, 3 x snorm16 normal,
3 x unorm8 RGB + 1 padding byte; then uint16 triangle indices.
Both assets total 793,264 bytes, loaded only near their section.
Decorations pause offscreen/in background and follow the page motion control.
WebGL unavailable: decorative canvases remain hidden; all content stays readable.
