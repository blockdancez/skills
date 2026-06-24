# Skills Repository

This repository stores local agent skills and their supporting reference files.

## Structure

- `design-guide/`: a skill for routing UI and visual design requests to the most relevant product or brand design references
- `design-guide/references/`: bundled markdown reference documents used by the skill at runtime
- `collect-product-rankings/`: a skill for collecting current products from product launch boards and AI/tool directories into per-site JSON files
- `google-ads-campaign-operator/`: a skill for Google Ads campaign setup, optimization, CSV report triage, and growth strategy
- `glintskill/`: a Codex-focused bundle for project profile capture and automated backlink submission

## Installation

Install all skills from this repository into the current project:

```bash
npx skills add blockdancez/skills
```

Install only `google-ads-campaign-operator` into the current project:

```bash
npx skills add blockdancez/skills --skill google-ads-campaign-operator
```

Install only `google-ads-campaign-operator` globally:

```bash
npx skills add blockdancez/skills --skill google-ads-campaign-operator -g
```

Install the GlintSkill Codex bundle:

```bash
tmp_dir="$(mktemp -d)" && \
git clone --depth 1 https://github.com/blockdancez/skills.git "$tmp_dir/skills" && \
mkdir -p ~/.codex/skills && \
rm -rf ~/.codex/skills/project-profile-capture \
  ~/.codex/skills/backlink-publisher \
  ~/.codex/skills/humanizer && \
cp -R "$tmp_dir/skills/glintskill/skills/project-profile-capture" \
  "$tmp_dir/skills/glintskill/skills/backlink-publisher" \
  "$tmp_dir/skills/glintskill/skills/humanizer" \
  ~/.codex/skills/ && \
rm -rf "$tmp_dir"
```

## Included Skill

### `design-guide`

`design-guide` helps an agent translate high-level UI requests into concrete implementation constraints. Instead of loading an entire reference library, it selects only the most relevant design documents for the requested style, brand, or product aesthetic.

Typical use cases:
- "Make it feel like Figma"
- "Use an Apple-like landing page style"
- "Build a polished SaaS dashboard with a Linear-style product feel"

### `collect-product-rankings`

`collect-product-rankings` gathers current products from sites such as Product Hunt, BetaList, Uneed, DevHunt, Microlaunch, Peerlist Launchpad, Fazier, Startup Fame, Futurepedia, Toolify, AIToolHunt, and TopAI.tools.

It writes one JSON file per source site with this schema, using the product's original website as `url`:

```json
{ "title": "", "url": "", "description": "", "category": "" }
```

The `category` field is a normalized product/site type such as `SAAS`, `AI`, `CMS`, or `DEV`.

### `google-ads-campaign-operator`

`google-ads-campaign-operator` helps create and optimize Google Ads campaigns with evidence-based operating rules, practical Google Ads UI guidance, paste-ready keywords and ads, conversion checks, UTM setup, CSV report triage, market expansion, and growth experiment planning.

### `glintskill`

`glintskill` is a Codex-focused backlink automation bundle. It includes:

- `project-profile-capture`: captures product profile assets from a project URL.
- `backlink-publisher`: reads a backlink JSON queue and uses Chrome to submit projects to backlink and directory platforms.
- `humanizer`: rewrites submission copy so backlink descriptions sound more natural.

Recommended runtime: Codex, because the backlink publishing flow depends on local skills, Chrome operation, and agent-assisted copy generation.

## Documentation Source

The reference documents bundled under `design-guide/references/` are sourced from the `getdesign.md` collection:

- https://getdesign.md/

As of April 9, 2026, that site describes itself as a collection of "Design system inspirations from popular websites." The local copies in this repository are kept so the skill can work without depending on a live network fetch.
