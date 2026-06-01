# jobops

AI-powered job search command center. The system is modeled with [Domain-Driven Design (DDD)](https://martinfowler.com/bliki/DomainDrivenDesign.html): bounded contexts, each with its own ubiquitous language, communicate through events and APIs rather than shared databases.

Design documentation lives in [`.design/`](.design/).

## Overview

**jobops** decomposes the job-search workflow into cohesive capabilities: discovering postings, scoring fit, generating ATS-optimized resumes, submitting applications, tracking pipeline status, researching companies, outreach, interview prep, training, career strategy, and analytics.

The target architecture is a **modular monolith or microservices** layout with **event-driven integration** and **AI sub-agents per bounded context**, so modes and providers can evolve without a single monolithic agent.

## Design docs

| Document | Contents |
|----------|----------|
| [`.design/context-map.md`](.design/context-map.md) | Bounded contexts, relationships, CLI mode mapping, architecture notes, boundary risks |
| [`.design/domain-models.md`](.design/domain-models.md) | Context breakdown, Mermaid interaction diagram, mode mapping, OpenAPI 3.1 skeletons per context |

## Bounded contexts

Each context owns its models and terms. Cross-context integration uses domain events and explicit APIs (with anti-corruption layers for external job boards, LinkedIn, etc.).

| Context | Responsibility |
|---------|----------------|
| **Opportunity Discovery** | Crawl and aggregate job postings from portals and boards |
| **Job Evaluation** | Score and rank jobs (e.g. multi-dimensional / A–F fit model) |
| **Resume / CV Generation** | Tailor ATS-optimized resumes and PDFs per role |
| **Application Execution** | Auto-fill and submit application forms |
| **Pipeline & Tracking** | Source of truth for applications, statuses, follow-ups, deduplication |
| **Company Research** | Company profiles, culture, news for fit and interviews |
| **Contact / Outreach** | Contacts, templates, LinkedIn/email outreach |
| **Interview Preparation** | Story bank (STAR), questions, negotiation scripts |
| **Training & Projects** | Courses, certifications, portfolio projects vs skill gaps |
| **Career Strategy (North Star)** | Goals, archetype, preferences that personalize scoring and CVs |
| **Analytics & Patterns** | Rejection patterns, pipeline metrics, insights back to strategy |

[`domain-models.md`](.design/domain-models.md) also describes a consolidated **Application Management** view (apply + pipeline + follow-up), **Offer Evaluation** (compensation-focused scoring for received offers), and **User/Profile** (auth, preferences, shared profile data).

### Typical flow

```text
Opportunity Discovery → Job Evaluation → Pipeline
                              ↓
         Career Strategy ──→ Resume Generation → Application Execution
                              ↓
              Company Research / Interview Prep / Analytics
```

## CLI modes

Command modes map to bounded contexts (see [context-map §4](.design/context-map.md) and [domain-models §4](.design/domain-models.md) for detail).

| Mode | Primary context(s) |
|------|----------------------|
| `scan` | Opportunity Discovery |
| `batch` | Opportunity Discovery + Job Evaluation (orchestrated) |
| `ofertas` | Opportunity Discovery / Job Evaluation (filter & score listings) |
| `oferta` | Job Evaluation (listing fit) or Offer Evaluation (compensation package) |
| `pdf` | Resume / CV Generation |
| `apply` | Application Execution (or Application Management) |
| `pipeline`, `tracker`, `followup` | Pipeline & Tracking |
| `deep` | Company Research |
| `contacto` | Contact / Outreach |
| `training`, `project` | Training & Projects |
| `interview-prep` | Interview Preparation |
| `update` | Career Strategy / User Profile |
| `patterns` | Analytics & Patterns |

Example invocations (from design): `/jobops scan`, `/jobops apply`, `/jobops interview-prep`.

## Architecture (summary)

- **Service boundaries** — One deployable or module per bounded context; database-per-service where possible.
- **Integration** — Async domain events (e.g. `JobFound`, `JobEvaluated`, `ApplicationSubmitted`, `ResumeGenerated`) plus REST/OpenAPI for on-demand queries; AsyncAPI for event contracts.
- **AI agents** — Scoped to a single context (evaluation, form fill, interview coach, etc.); outputs validated before pipeline updates where needed.
- **APIs** — OpenAPI 3.1 specs in [`openapi-core/src/`](openapi-core/src/) (one spec pair per bounded context); originated from [`.design/domain-models.md`](.design/domain-models.md).

## Repository layout

| Path | Purpose |
|------|---------|
| [`.design/`](.design/) | DDD context map, domain models, CLI mode mapping |
| [`openapi-core/`](openapi-core/) | OpenAPI 3.1 specs per bounded context (see [`openapi-core/README.md`](openapi-core/README.md)) |
| [`EXAMPLE_openapi-core/`](EXAMPLE_openapi-core/) | Reference layout for spec authoring (upstream template) |

## Status

**Design and API contracts** are in place under `.design/` and `openapi-core/`. Runtime implementation (services, agents, CLI) is not yet present.

## License

This project is licensed under the [MIT License](LICENSE).
