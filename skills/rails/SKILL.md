---
name: rails
description: Build or review Rails changes using the application's actual Rails conventions and tests.
---

# Rails

Make idiomatic Rails changes that fit the application already in front of you. Treat the repository's Rails version, frontend stack, test framework, and deployment constraints as authoritative.

## Inspect before choosing tools

- Read project instructions and inspect `Gemfile`, application configuration, existing models, controllers, views, jobs, tests, and lint configuration.
- Reuse established conventions for Hotwire, JavaScript bundling, CSS, authentication, background jobs, and testing. Do not assume Rails 8, Importmaps, Tailwind, Minitest, fixtures, or the absence of Node tooling.
- Use Rails generators when they match the project workflow and improve consistency; do not force them for a small targeted edit.

## Design and implement

- Keep controllers focused on HTTP concerns; place reusable domain behavior where the existing application places it. Avoid introducing service objects merely by default.
- Keep database access and non-trivial presentation logic out of templates. Use explicit dependencies in jobs and reusable domain code rather than ambient request state when feasible.
- For behavior changes, add focused tests in the project's existing style before or alongside the change. Include authorization, validation, unhappy paths, and background behavior when relevant.
- Make migrations reversible and safe for the application's database and deployment practices; inspect existing migration conventions before adding one. A migration is a one-way door under `decision-gate`.

## Verify

- Run the narrowest relevant Rails test first, followed by the project's appropriate broader checks (for example test suite, system tests, lint, or security checks) when practical.
- Report the Rails conventions followed, files changed, checks run, and any unverified deployment or migration risk.
- Do not commit, push, or alter environment configuration without explicit authorization.
