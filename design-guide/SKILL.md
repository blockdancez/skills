---
name: design-guide
description: Use when the user wants a polished UI and references a well-known product, brand, or aesthetic such as Figma, Apple, Linear, Stripe, Notion, Airbnb, Tesla, or asks for a premium, beautiful, product-grade interface. Loads only the most relevant design reference docs from references/ and turns them into implementation constraints.
metadata:
  short-description: Route UI requests to the right design references
---

# Design Guide

This skill helps an agent turn broad design requests into concrete implementation guidance by loading the most relevant brand or product design references from `references/`.

Use this skill when the user asks for a website, app, dashboard, landing page, tool UI, component, or redesign that should feel:
- like a known company or product
- premium, polished, elegant, refined, cinematic, minimal, futuristic, playful, product-grade, or "high-end"
- similar to phrases such as "像 Figma 一样", "参考 Apple", "做成 Linear 风格", "页面精美一点", "像大厂产品一样"

Do not use this skill for:
- backend-only tasks
- invisible infrastructure work
- bug fixes that do not affect presentation
- cases where the user explicitly wants to preserve an existing design system and does not want outside inspiration

## Goal

Pick the minimum number of reference docs needed, extract implementable constraints, and apply them to the user's request without loading the entire design library into context.

The references are already bundled in `references/`. Each file is a brand- or product-specific design guide derived from a real interface and usually includes:
- visual theme and atmosphere
- typography and spacing
- color system
- component patterns
- depth, motion, and interaction cues
- responsive behavior
- agent prompt guidance

## Reference Provenance

The markdown files under `references/` are sourced from the `getdesign.md` collection:
- https://getdesign.md/

They are included here so the skill can use them locally without fetching remote content at runtime.

## Directory Layout

```text
design-guide/
├── SKILL.md
└── references/
    ├── Figma.md
    ├── Linear.md
    ├── Apple.md
    ├── Stripe.md
    ├── Notion.md
    ├── ...
```

`references/` is a flat folder. Each markdown file represents one design reference. Filenames are the lookup keys.

Important naming notes:
- Many references are exact brand names: `Figma.md`, `Apple.md`, `Linear.md`
- Some names contain spaces: `Mistral AI.md`, `Together AI.md`
- Some names use underscores: `Cal_com.md`
- Preserve the existing filenames when reading them

## Reference Index

These are all files currently available under `references/`. Use these exact names when selecting and opening references:

- `Airbnb.md`
- `Airtable.md`
- `Apple.md`
- `BMW.md`
- `Cal_com.md`
- `Claude.md`
- `Clay.md`
- `ClickHouse.md`
- `Cohere.md`
- `Coinbase.md`
- `Composio.md`
- `Cursor.md`
- `ElevenLabs.md`
- `Expo.md`
- `Ferrari.md`
- `Figma.md`
- `Framer.md`
- `HashiCorp.md`
- `IBM.md`
- `Intercom.md`
- `Kraken.md`
- `Lamborghini.md`
- `Linear.md`
- `Lovable.md`
- `MiniMax.md`
- `Mintlify.md`
- `Miro.md`
- `Mistral AI.md`
- `MongoDB.md`
- `NVIDIA.md`
- `Notion.md`
- `Ollama.md`
- `OpenCode.md`
- `Pinterest.md`
- `PostHog.md`
- `Raycast.md`
- `Renault.md`
- `Replicate.md`
- `Resend.md`
- `Revolut.md`
- `Runway.md`
- `Sanity.md`
- `Sentry.md`
- `SpaceX.md`
- `Spotify.md`
- `Stripe.md`
- `Supabase.md`
- `Superhuman.md`
- `Tesla.md`
- `Together AI.md`
- `Uber.md`
- `Vercel.md`
- `VoltAgent.md`
- `Warp.md`
- `Webflow.md`
- `Wise.md`
- `Zapier.md`
- `xAI.md`

## How To Read References

Read only the files you need.

Preferred workflow:
1. Check whether the user named a brand, product, or aesthetic directly.
2. If yes, read that exact file first.
3. If the user did not name a reference, infer the closest 1-3 files from the routing guide below.
4. Extract 5-10 concrete design constraints before implementing.
5. Use those constraints to design and build the UI.

Never load all of `references/` into context.

### Exact-match examples

- "像 Figma 一样" -> read `references/Figma.md`
- "做成 Apple 官网那种感觉" -> read `references/Apple.md`
- "要有 Linear 那种产品感" -> read `references/Linear.md`
- "参考 Together AI 或 Mistral 的 AI 公司官网" -> read `references/Together AI.md` or `references/Mistral AI.md`
- "像 cal.com 那种排版" -> read `references/Cal_com.md`

### Reading examples

When opening files, use exact paths and quote names with spaces:

```text
references/Figma.md
references/Linear.md
references/Apple.md
references/Together AI.md
references/Mistral AI.md
references/Cal_com.md
```

If you need discovery first, list or search the folder and then open only the best matches.

## Selection Rules

Choose references in this order:

1. Explicit user mention
2. Product category match
3. Visual mood match
4. Interaction density match
5. Content model match

Default to:
- 1 primary reference
- 1 secondary reference for component language or motion
- optional 1 tertiary reference only if the first two are insufficient

Avoid mixing more than 3 references unless the user explicitly asks for a hybrid.

## Routing Guide

Use this as a starting point when the user does not give an exact brand.

### Creative tools and modern design software

Good defaults:
- `Figma.md`
- `Framer.md`
- `Webflow.md`
- `Miro.md`

Use when the user wants:
- creative tool UI
- sophisticated hero sections
- colorful visual output inside a restrained shell
- design-forward productivity software

### Productive, dense, high-craft SaaS

Good defaults:
- `Linear.md`
- `Raycast.md`
- `Superhuman.md`
- `Notion.md`
- `Airtable.md`

Use when the user wants:
- product precision
- premium dashboards
- compact tooling
- strong hierarchy and polished interaction states

### Developer tools and technical trust

Good defaults:
- `Stripe.md`
- `Vercel.md`
- `Supabase.md`
- `Mintlify.md`
- `MongoDB.md`
- `Sentry.md`
- `PostHog.md`
- `ClickHouse.md`
- `HashiCorp.md`

Use when the user wants:
- developer credibility
- documentation-heavy or product-led interfaces
- fintech/developer product hybrid
- clean technical storytelling

### AI-native and futuristic interfaces

Good defaults:
- `Claude.md`
- `Runway.md`
- `Replicate.md`
- `ElevenLabs.md`
- `Mistral AI.md`
- `Together AI.md`
- `MiniMax.md`
- `xAI.md`
- `Lovable.md`

Use when the user wants:
- AI lab aesthetics
- cinematic gradients
- futuristic interaction language
- model, agent, or media product presentation

### Premium hardware, automotive, and cinematic product pages

Good defaults:
- `Apple.md`
- `Tesla.md`
- `SpaceX.md`
- `BMW.md`
- `Ferrari.md`
- `Lamborghini.md`
- `Renault.md`

Use when the user wants:
- luxury presentation
- object-focused product showcase
- dramatic sections with large imagery and restrained UI chrome

### Consumer, marketplace, and lifestyle polish

Good defaults:
- `Airbnb.md`
- `Pinterest.md`
- `Spotify.md`
- `Uber.md`
- `Revolut.md`
- `Wise.md`

Use when the user wants:
- approachable but polished consumer design
- content browsing
- marketplace or travel product feel
- editorial or lifestyle-led presentation

### Finance, trust, and transaction-heavy products

Good defaults:
- `Stripe.md`
- `Revolut.md`
- `Wise.md`
- `Coinbase.md`
- `Kraken.md`

Use when the user wants:
- trust and clarity
- conversion-focused flows
- polished financial product UI

## Implementation Workflow

After selecting references:

1. Summarize the user's product, audience, and page type in one sentence.
2. Name the chosen references and why they fit.
3. Extract a compact design brief from the docs:
   - color direction
   - typography choices
   - spacing rhythm
   - border radius language
   - card, button, input, and navigation patterns
   - motion and depth
4. Convert that brief into implementation constraints for the actual UI.
5. Build the requested interface.
6. Ensure the result still fits the user's product and content, not just the reference aesthetic.

## Output Requirements

When using this skill, the resulting implementation should:
- feel intentionally designed, not generic
- preserve the main structural patterns of the user's existing product if one already exists
- borrow design principles, not copy trademarks, logos, or exact branded assets
- turn reference insights into CSS tokens, layout rules, and component constraints
- stay coherent if multiple references are combined

Before implementation, keep a short internal checklist:
- Which file(s) did I read?
- What 5-10 constraints did I extract?
- Which parts of the final UI come from the primary reference?
- Which parts, if any, come from the secondary reference?

## Conflict Resolution

If references conflict:
- prioritize the explicitly named reference
- prioritize the user's product category over visual novelty
- prefer one strong visual system over a muddy blend

Examples:
- "像 Figma 一样，但更像 Apple 一点" -> Figma for layout energy, Apple for restraint and polish
- "做个 AI 工具站，但不要太花" -> start with `Claude.md` or `Linear.md`, not the most gradient-heavy AI reference
- "做个漂亮的 todolist，像 Figma 一样" -> primary `Figma.md`, optional secondary `Linear.md` for productivity-app density

## Efficiency Rules

- Do not read the whole library
- Do not paraphrase entire reference files into the response
- Do not expose large excerpts unless needed
- Prefer extracting only the design constraints necessary to implement the user's request

This skill is successful when the agent can map vague design intent to the right references quickly and produce a UI that feels specific, credible, and implementation-ready.
