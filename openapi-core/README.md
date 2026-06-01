# jobops OpenAPI

OpenAPI 3.1 specs for **jobops** bounded contexts, following the layout in `EXAMPLE_openapi-core/` and the domain model in [`.design/`](../.design/).

## Layout

| Path | Purpose |
|------|---------|
| `src/{domain}.yaml` | Paths, parameters, responses, `operationId`s |
| `src/{domain}.schemas.yaml` | Entity and DTO schemas for that domain |
| `src/common/` | Shared security, errors, parameters, and primitives |
| `src/.bundled/` | Bundled JSON (generated; resolved `$ref`s) |
| `domains.json` | Domain list for lint and bundle scripts |
| `docs/DOMAIN-COVERAGE-MATRIX.md` | Entity/operation coverage per bounded context |

## Domains (15)

Aligned with [`.design/domain-models.md`](../.design/domain-models.md) and [`.design/context-map.md`](../.design/context-map.md):

| Spec | Bounded context | `x-domain` |
|------|-----------------|------------|
| `discovery` | Opportunity Discovery | `disc` |
| `evaluation` | Job Evaluation | `eval` |
| `pipeline` | Pipeline & Tracking | `pip` |
| `application-execution` | Application Execution (form submit) | `aex` |
| `resume` | Resume / CV Generation | `res` |
| `company` | Company Research | `co` |
| `interview` | Interview Preparation | `int` |
| `contacts` | Contacts & Outreach | `con` |
| `training` | Training & Projects | `trn` |
| `offer` | Offer Evaluation | `off` |
| `analytics` | Analytics & Insights | `anl` |
| `profile` | User / Profile | `prf` |
| `strategy` | Career Strategy (North Star) | `str` |
| `ai` | AI (models, prompts, inference, agent runs) | `aia` |
| `platform` | Health and context catalog | `plt` |

Each domain spec may include `x-cli-modes` on `info` for CLI mapping (`scan`, `apply`, `pdf`, etc.).

### URL migration (from merged `application` spec)

| Former path | New path |
|-------------|----------|
| `GET/POST /applications` | `GET/POST /pipeline/applications` |
| `PUT /applications/{appId}/status` | `PUT /pipeline/applications/{appId}/status` |
| `POST /applications/followups` | `POST /pipeline/followups` |
| `POST /applications/{appId}/submit` | `POST /execution/submissions` |

## Scripts

From this directory:

```bash
pnpm install
pnpm test            # lint + bundle (recommended)
# or separately:
pnpm lint:domains    # redocly lint path specs in domains.json
pnpm bundle:domains  # write src/.bundled/*.json
pnpm lint:all        # lint every YAML under src/ (extra unused-component warnings on *.schemas.yaml)
```

## Conventions

- **JWT**: `bearerAuth` from `src/common/security.yaml` on protected routes.
- **Errors**: `400` / `401` / `403` / `404` via `src/common/responses.yaml`.
- **Schemas**: Defined in `{domain}.schemas.yaml`; path specs alias them under `components.schemas`.
- **Entities**: Persisted aggregates use `x-entity: true`; shared value objects use `x-value-object: true` (see `src/common/primitives.yaml`).
- **URLs**: Single gateway `https://api.jobops.dev` with path prefixes (`/discovery/...`, `/pipeline/...`, `/execution/...`).

## Reference

See [`EXAMPLE_openapi-core/`](../EXAMPLE_openapi-core/) for the upstream Virial template (tooling patterns only; jobops specs are independent).
