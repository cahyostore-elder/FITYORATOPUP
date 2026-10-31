# Production schema snapshots

No declarative production schema snapshot is bundled in this clean repository because the
successful `supabase db pull --declarative` output was generated inside the previous
Codespaces workspace and was not part of the verified GitHub CI artifact used to build
this ZIP. Do not recreate it from an incomplete or terminal-copied function definition.

When the existing production project is available, create a fresh read-only snapshot to a
review folder and compare it to the database backup before using it as a baseline. Do not
run `db push`, `db reset --linked`, or migration repair merely to create this folder.
