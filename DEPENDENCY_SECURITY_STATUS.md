# Dependency security review — 2026-10-31

## Current finding

The initial GitHub Actions run stopped during automatic npm audit remediation.
The lockfile contains minimatch 10.2.6 under
@typescript-eslint/typescript-estree 8.72.1, as well as older minimatch
versions in the ESLint dependency tree.

The current advisory identifies versions below 11.0.1 as affected by
glob-parts amplification when optimizationLevel is 2 or higher.
Version 11.0.1 is the patched release.

A known typescript-eslint call does not explicitly set optimizationLevel.
That observation is not proof that every consumer in the dependency tree
is safe, and it does not remove the vulnerability finding.

## Temporary CI arrangement

The application verification and dependency audit run as separate jobs.

- verify: npm ci, typecheck, lint, production build, regression tests,
  release preflight, and source artifact packaging.
- dependency-audit: npm ci and full npm audit with a low severity threshold.

The dependency audit remains blocking. A passing application job alone
does not make the complete workflow green or authorize production release.

Do not force a major minimatch override or run npm audit fix --force.
Upgrade only after compatible upstream releases and toolchain tests are
available.

No production database migration or checkout activation is authorized
by this CI change.
