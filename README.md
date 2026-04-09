# Skills Repository

This repository stores local agent skills and their supporting reference files.

## Structure

- `design-guide/`: a skill for routing UI and visual design requests to the most relevant product or brand design references
- `design-guide/references/`: bundled markdown reference documents used by the skill at runtime

  ```
  npx skills add blockdancez/skills
  ```

## Included Skill

### `design-guide`

`design-guide` helps an agent translate high-level UI requests into concrete implementation constraints. Instead of loading an entire reference library, it selects only the most relevant design documents for the requested style, brand, or product aesthetic.

Typical use cases:
- "Make it feel like Figma"
- "Use an Apple-like landing page style"
- "Build a polished SaaS dashboard with a Linear-style product feel"

## Documentation Source

The reference documents bundled under `design-guide/references/` are sourced from the `getdesign.md` collection:

- https://getdesign.md/

As of April 9, 2026, that site describes itself as a collection of "Design system inspirations from popular websites." The local copies in this repository are kept so the skill can work without depending on a live network fetch.
