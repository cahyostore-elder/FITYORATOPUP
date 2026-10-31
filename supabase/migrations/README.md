# Active migration directory — intentionally empty

The 30 historical migration files are preserved under
`supabase/archive/migrations-pre-baseline-20261030/` and are **not active migrations**.

Do not copy these old files back into this directory and do not run them against the
existing production database. Production is a mixed/manual state with an empty remote
migration ledger. A reviewed baseline and new forward-only migrations must be created
before `supabase db push` is permitted.

Only add newly reviewed migration files here after:
1. Comparing the live production schema with the retained SQL snapshot.
2. Testing the baseline against a disposable/local database.
3. Confirming the baseline does not replay catalogue seeds, selling-price updates,
   or existing security changes.
4. Reviewing every forward migration and backing up the production project.
