# Content stress

Use explicit fictional fixtures to test selected boards on disposable copies. Start with actual file/page/board and text IDs. Select a specific question: long labels, many records, no records, unknown import outcome, missing artwork or enlarged text. Do not infer new product behavior while constructing cases.

For text probes write JSON with `name`, `changes: [{shapeId, characters}]`, and optional `fontScale` between 0.5 and 3. IDs refer to text descendants of one source board. Reuse the same content across directions. Use `review.py stress` for a dry run, then `--apply` under the user's scoped stress-test request. Optional `--width` resizes only the copy. It does not emulate device font scaling or prove responsive behavior.

The helper checkpoints the file, clones a top-level board without main components and edits the clone. It groups changes for undo and labels the copy. Keep returned IDs and inspect after layout settles. Missing-art and busy/empty structural cases need explicit native edits on the created copy; the text helper does not implement those automatically.

Check wrapping, reading order, practical action visibility, keyboard space and status meaning on rendered exports. Record defects against the copy IDs with fixture revision and capture conditions. Preserve source boards and fixture originals. Do not delete another person's manual work when cleaning up.
