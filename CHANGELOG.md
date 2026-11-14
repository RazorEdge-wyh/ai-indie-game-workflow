# Changelog

## v1.0.1 (2026-11-14)

- Remove persona presets from the review protocol. The agent must not invent player names, ages, jobs, or backstories; it asks the user for player information and uses only the neutral labels "target player / picky player".
- Delete `references/examples.md` (it contained named example personas).
- Rewrite `P5` from "generate two personas" to "ask the user, do not generate".

## v1.0.0 (2026-11-13)

- Initial release.
- Gate-based workflow: G0 seed, N narrative, A art direction, L blockout, C core loop, P atmosphere, T technical skeleton, V vertical slice, M production, R convergence.
- Four order presets: narrative / gameplay / experience / multiplayer.
- Dual-perspective review protocol with a hard output budget (400 chars review, 200 chars freeze card).
- A/B/C decision tiers (human / AI proposes / AI autonomous with weekly audit).
- Freeze card and change order templates.
- `scripts/init_workflow.py` and `scripts/check_gates.py` (tested: init, pass, missing-section fail, strict fail).
- Apache License 2.0.
