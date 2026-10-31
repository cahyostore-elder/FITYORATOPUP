# FITYORATOPUP — new repository handoff

Target repository: `https://github.com/cahyostore-elder/FITYORATOPUP`
Previous repository backup: `https://github.com/cahyostore-elder/HANYABACKUP`

## What this package contains

- Application source from the Phase 61–64 candidate branch.
- A source version whose upstream GitHub Actions checks passed at commit
  `ba32ee307f789df1a83c3f841f046495706a08a7` (workflow run `41026808755`).
- 30 historical SQL migrations preserved under
  `supabase/archive/migrations-pre-baseline-20261030/`, with SHA-256 checksums.
- A fresh, secret-free Supabase CLI configuration for PostgreSQL 17.
- Regression/preflight scripts updated to read the archived historical SQL.

The repackaging changes (migration archival, config, and UI warning) must still be
revalidated in this new repository; the upstream CI result does not certify these
repackaging edits by itself.

## Important production status

This is a clean source repository, **not a declaration that production is ready to
receive orders**. The existing Supabase production project remains the intended backend.
Its current migration history is empty, while its live schema already contains parts
of the historical migration effects. Therefore:

- The active `supabase/migrations/` directory is intentionally empty.
- The 30 SQL files in `supabase/archive/` are historical evidence only. Do not execute
  them, do not restore them to the active folder, and do not run them as a batch.
- Do not run `supabase db push`, `supabase db reset --linked`, or migration repair
  against production until a baseline and forward-only migrations have been reviewed.
- A schema export is not a full backup of Auth, Storage bucket metadata/policies,
  project settings, or Storage object bytes.
- Phase 62 dual-maintenance and Phase 63 sample-cost functionality require reviewed
  forward migrations before production use. Do not disable maintenance or enable
  customer checkout until those database guards are confirmed live.

## Local setup

1. Clone this repository and open its root directory in Codespaces.
2. Run `npm ci`.
3. Copy `.env.example` to `.env.local` and supply the project's public Supabase URL
   and publishable key. Never use a service-role/secret key in a `VITE_*` variable.
4. Run `npm run check` and `node --test scripts/*.test.mjs`.
5. Link Supabase only when authorized: `supabase link --project-ref <project-ref>`.
   Do not put a PAT, database password, or connection URI in source files.

## Vercel

- Root Directory: `./`
- Framework: Vite
- Install Command: `npm ci`
- Build Command: `npm run build`
- Output Directory: `dist`
- Environment variables: `VITE_SUPABASE_URL` and `VITE_SUPABASE_PUBLISHABLE_KEY`

Deploy a Preview first. Production deployment and customer checkout remain gated on
successful database baseline, forward migrations, and end-to-end order/payment tests.
