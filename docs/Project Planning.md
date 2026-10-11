# ProCom — Project Planning

**Project name:** ProCom  
**Meaning:** Product Commerce  
**Document status:** Initial plan  
**Approach:** Build in small, testable milestones; keep Phase 1 independently useful and make Phase 2 a separate frontend consuming the same backend.

---

## 1. Vision and goals

ProCom is a product-management and commerce platform built as a learning project with production-minded engineering practices.

It will have two phases:

- **Phase 1 — Backend and admin:** A FastAPI application, a server-rendered Jinja2 admin panel, a PostgreSQL database, product media storage, REST and GraphQL APIs, authentication/authorization, automated tests, Docker, CI, and deployment.
- **Phase 2 — Storefront:** A separate Next.js + TypeScript storefront that consumes the Phase 1 APIs. Add customer-facing passwordless social sign-in using OAuth/OIDC providers such as Google and Microsoft.

The primary goal is to learn how these technologies fit together, not to add every possible technology at once. Each milestone should leave the repository runnable and tested.

## 2. Scope and non-goals

### Phase 1 scope

- Product, category, brand, and product-image management.
- Admin pages rendered with Jinja2; use HTMX for progressive interactions and Tailwind CSS for styling if desired.
- PostgreSQL persistence using SQLAlchemy 2.x.
- Alembic database migrations.
- REST API for management and operational endpoints.
- Strawberry GraphQL endpoint, initially focused on product/catalog queries and selected mutations.
- Users, roles, permissions, and explicit many-to-many relationships.
- Admin authentication and authorization.
- Cloudflare R2 media storage through an S3-compatible storage abstraction.
- Health/liveness/readiness endpoints and a health page.
- pytest unit, integration, API, auth, and GraphQL tests.
- Docker/Compose local development.
- GitHub Actions CI and a deployment workflow.
- Documentation in `docs/`.

### Phase 2 scope

- Separate Next.js App Router + TypeScript storefront.
- Product listing, product detail, category browsing, search/filtering, responsive UI, loading/error/empty states, and SEO metadata.
- Consume FastAPI APIs rather than reimplementing backend business rules.
- Customer account identity through OAuth 2.0 / OpenID Connect, using Google and Microsoft as initial providers.
- Passwordless customer sign-in: no local customer password is required when social sign-in is the chosen login method.
- Later commerce features can include carts, checkout, orders, and payment integration; do not treat payment handling as part of the initial catalog milestone.

### Not in the first release

- Microservices.
- Kubernetes.
- Redis or a background-worker system until a concrete requirement appears.
- Storing image binaries in PostgreSQL.
- A separate React admin application.
- Custom cryptography or custom OAuth protocol implementations.
- Payment-card data storage.

## 3. Technology stack and decisions

| Concern | Choice | Reason / implementation note |
|---|---|---|
| Language | Python 3.13+ | Modern Python baseline; choose a supported version available in the deployment environment. |
| API framework | FastAPI | Typed APIs, dependency injection, OpenAPI support, and async support. |
| ORM | SQLAlchemy 2.x | Widely used, explicit typed ORM patterns, and flexible relationship/query control. |
| Database | PostgreSQL | Relational constraints, transactions, indexes, and reliable many-to-many relationships. |
| Migrations | Alembic | Version-controlled schema changes; never rely on `create_all()` as the production migration strategy. |
| Validation/settings | Pydantic v2 and pydantic-settings | Request/response schemas and environment-based settings. |
| Templates | Jinja2 | Server-rendered admin pages. |
| Admin interactions/styles | HTMX + Tailwind CSS (progressively introduced) | Interactive admin UI without needing a second frontend app in Phase 1. |
| GraphQL | Strawberry GraphQL | Python type-friendly GraphQL integration with FastAPI. |
| Dependency/tool management | `uv` | Project dependencies, virtual environment management, lockfile, and repeatable installs. |
| Project configuration | `pyproject.toml` + committed `uv.lock` | Central project/tool configuration and reproducible dependency resolution. |
| Media | Cloudflare R2 via S3-compatible API | Start with R2; learn S3-compatible operations and keep the provider replaceable. |
| Object storage SDK | `boto3` initially | Mature S3 API client; configure the R2 endpoint and credentials. Keep provider details inside the storage adapter. |
| Authentication, Phase 1 | Secure admin session/cookie-based authentication, with a clearly documented implementation | Keep browser admin security practical. Avoid putting long-lived bearer tokens in browser local storage. |
| Authorization | RBAC with explicit association tables | Users can have multiple roles; roles can grant multiple permissions; optional direct user permissions can be added with clear precedence rules. |
| Password hashing, if local admin passwords are used | Argon2 via a maintained library | Never store plaintext passwords or implement hashing yourself. |
| Testing | pytest, HTTPX, pytest-asyncio as needed | Test behavior at unit and integration boundaries. |
| Lint/format | Ruff | Fast Python linting and formatting. |
| Type checking | mypy (or another selected checker) | Add checks gradually and keep the command stable in CI. |
| Containers | Docker + Docker Compose | Reproducible local services and a portable app image. |
| CI/CD | GitHub Actions | Pull-request checks and a controlled deployment workflow. |
| Phase 1 hosting | FastAPI Cloud or another container-capable Python host, after verifying current features and pricing | Prefer a conventional FastAPI runtime over forcing the full application into function-oriented hosting. |
| Phase 2 frontend hosting | A Next.js-compatible host | Select after confirming SSR, environment, domain, and pricing requirements. |
| Docs | Markdown in `docs/` | Version-controlled architecture, setup, operations, and decision records. |

### Important hosting note

Hosting choices are deployment targets, not architectural dependencies. Keep the application containerizable and configuration-driven so the API can move between providers. Verify current hosting capabilities, region availability, persistent-process support, database connectivity, and pricing before deployment.

## 4. High-level architecture

```text
Phase 1
Admin browser
    |
    v
FastAPI application
    |-- Jinja2 + HTMX admin pages
    |-- REST API (/api/...)
    |-- Strawberry GraphQL (/graphql)
    |-- Health endpoints (/health/...)
    |-- Authentication and authorization
    |-- Product/catalog services
    |-- Storage interface
    |
    +---- SQLAlchemy ---- PostgreSQL
    |
    +---- S3-compatible client ---- Cloudflare R2
                                      (image/object binaries)

Phase 2
Customer browser
    |
    v
Next.js + TypeScript storefront
    |
    +---- REST / GraphQL ---- FastAPI
    |
    +---- product image URLs ---- R2
    |
    +---- OAuth/OIDC redirects ---- Google / Microsoft
```

The API owns business rules and database access. The storefront must not connect directly to PostgreSQL or contain privileged storage credentials.

## 5. Repository layout (target shape)

The exact tree will grow incrementally; do not create empty files for every future feature on day one.

```text
ProCom/
├── app/
│   ├── main.py
│   ├── config/
│   ├── db/
│   │   ├── database.py
│   │   ├── models/
│   │   └── repositories/
│   ├── api/
│   │   ├── rest/
│   │   └── graphql/
│   ├── auth/
│   ├── services/
│   ├── schemas/
│   ├── storage/
│   ├── templates/
│   └── static/
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   ├── auth/
│   └── graphql/
├── docs/
│   ├── architecture.md
│   ├── development.md
│   ├── database.md
│   ├── authentication.md
│   ├── authorization.md
│   ├── media-storage.md
│   ├── graphql.md
│   ├── testing.md
│   ├── deployment.md
│   └── decisions/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── .env.example
├── .gitignore
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── uv.lock
└── README.md

Phase 2 can live in a separate `storefront/` directory or a separate repository. Start in a `storefront/` directory in this repository if a single-repository learning workflow is preferred; it still deploys independently.
```

## 6. Data model plan

Start with the smallest useful schema and evolve it through Alembic migrations.

### Catalog

- `products`: ID, SKU, name, slug, description, price, currency, status, timestamps.
- `categories`: ID, name, slug, optional parent category if hierarchy is needed.
- `product_categories`: association table if a product may belong to multiple categories. If the product should have exactly one category, use a foreign key instead; decide deliberately before implementing.
- `brands`: ID, name, slug, optional description.
- `product_media`: ID, product ID, object key, media type, MIME type, byte size, alt text, sort order, primary flag, timestamps.

Store prices as fixed-precision numeric values or integer minor units, not binary floating-point. Define currency and rounding behavior explicitly.

### Identity and access control

- `users`: ID, email (normalized), display name, active flag, timestamps.
- `roles`: ID, unique role name, description.
- `permissions`: ID, unique permission key (for example `product:create`), description.
- `user_roles`: composite primary key or unique pair `(user_id, role_id)`.
- `role_permissions`: composite primary key or unique pair `(role_id, permission_id)`.
- Optional `user_permissions`: direct grants/revocations only if the policy is clearly defined.

The relationship graph is many-to-many: a user can have multiple roles, a role can belong to multiple users, and a role can grant multiple permissions. Enforce uniqueness and foreign keys in PostgreSQL. Define whether a direct permission is a grant, an override, or a deny; avoid ambiguous precedence.

For OAuth/OIDC in Phase 2, do not identify accounts solely by an email string returned by a provider. Add an `external_identities` table with fields such as `user_id`, `provider`, `provider_subject`, and timestamps; enforce uniqueness on `(provider, provider_subject)`. Link a verified identity to an existing account only through a deliberate, secure account-linking flow.

## 7. Media storage design

### Principle

- PostgreSQL stores metadata and ownership relationships.
- R2 stores file bytes.
- Store a stable `object_key` such as `products/<product-id>/<opaque-file-id>.webp`; do not make a full public URL the only identifier.
- Generate a delivery URL from configuration or store an explicit URL only when it is a deliberate part of the media model.

### Implementation progression

1. Start with an `ObjectStorage` interface and a local/test fake implementation.
2. Implement the R2 adapter using `boto3` with an endpoint URL and credentials loaded from environment variables.
3. In the first upload milestone, accept `UploadFile` through FastAPI, validate file size and allowed image MIME/type, and upload to R2.
4. Save metadata in `product_media`; define cleanup/compensation behavior if the object upload succeeds but the database transaction fails, or vice versa.
5. Add deletion and product-image ordering/primary-image rules.
6. Later, issue short-lived presigned upload URLs so the browser can upload directly to R2 without sending large files through FastAPI.
7. Keep credentials server-side. Public storefront images can use a public bucket/custom domain if configured; private objects require signed URLs. Never expose the R2 secret access key in frontend environment variables.
8. Document allowed file types, size limits, object-key policy, cache behavior, and orphan cleanup.

R2's S3 compatibility makes the concepts transferable to AWS S3. Switching providers should require configuration and adapter changes, not edits throughout product services.

## 8. Authentication and authorization plan

### Phase 1 — Admin access

- Establish admin authentication before exposing mutation pages.
- Use secure cookies for browser sessions; set `HttpOnly`, `Secure` in production, an appropriate `SameSite` policy, expiry, and session invalidation.
- Protect state-changing browser forms against CSRF.
- Hash any local admin passwords with a maintained Argon2 implementation.
- Keep authorization checks on the server for every protected action, not only in templates.
- Add a small permission vocabulary, such as `product:read`, `product:create`, `product:update`, `product:delete`, `user:manage`, and `role:manage`.
- Test both allowed and denied access.
- Document the authentication choice and its limitations.

### Phase 2 — Customer passwordless OAuth/OIDC

Use a maintained OAuth/OIDC integration rather than hand-implementing the protocol.

- Initial providers: Google and Microsoft.
- Use Authorization Code flow with PKCE where applicable; validate state, nonce (for OIDC), issuer, audience, signature, and redirect URI according to the library/provider guidance.
- Use provider subject identifiers as stable external identity keys.
- Request minimal scopes (`openid`, `email`, `profile` only as needed).
- Do not collect or store customer passwords when social sign-in is the selected passwordless path.
- Create/link local ProCom user records after validating the provider identity.
- The backend remains authoritative for local user status and roles.
- Use secure server-managed sessions or a carefully designed short-lived access-token/refresh-token scheme; do not store long-lived tokens in browser local storage.
- Define logout behavior locally and explain that it does not necessarily log the user out of Google/Microsoft.
- Provide a recovery/account-linking plan before production launch.
- Test denied consent, cancelled login, expired state, provider errors, duplicate identity, unverified email, and account-linking edge cases.
- Keep admin and customer access policies distinct. Customer social login must not automatically grant admin roles.

OAuth is an authorization framework; OpenID Connect (OIDC) adds the identity layer used for sign-in. Prefer OIDC for Google/Microsoft login.

## 9. Health and observability

Implement separate endpoints with clear meanings:

- `GET /health/live`: the application process is alive; keep this lightweight.
- `GET /health/ready`: the instance can serve requests, including a bounded database connectivity check.
- `GET /health`: human-readable or structured summary for local diagnosis.

The Jinja admin health page can show application uptime, database connectivity, and any real background worker or dependency that exists. Do not display a fictional “worker uptime” before a worker process is actually implemented. Distinguish application uptime from dependency health. Avoid exposing secrets, internal stack traces, or sensitive infrastructure details publicly.

If deployment runs multiple instances, each instance has its own process start time. Use platform monitoring/logging for reliable uptime history rather than treating an in-memory timer as a durable monitoring system.

## 10. API boundaries: REST and GraphQL

Use REST first for conventional management operations and operational endpoints:

- `/api/products`
- `/api/categories`
- `/api/brands`
- `/api/admin/users`
- `/api/admin/roles`
- `/health/live`, `/health/ready`

Add Strawberry at `/graphql` for selected catalog queries and mutations, particularly to learn GraphQL and let the storefront request exactly the product fields it needs.

Avoid duplicating business rules between REST and GraphQL. Both should call the same service layer. Add authorization checks and query complexity/depth safeguards before exposing GraphQL publicly. Never expose unrestricted database models directly.

## 11. Step-by-step implementation roadmap

Every phase should have a working result, tests, and an update to the docs.

### Phase 0 — Project foundation

1. Create the `ProCom` repository and initial README.
2. Install `uv`; verify Python version.
3. Initialize the Python project and `pyproject.toml`.
4. Create and commit `uv.lock`.
5. Add `.gitignore` and `.env.example`; never commit `.env` or real secrets.
6. Configure Ruff and a type checker.
7. Create a minimal FastAPI app and a smoke test.
8. Add the initial `docs/development.md` and architecture overview.

**Exit criteria:** a clean checkout can install dependencies and run the app/test command using documented steps.

### Phase 1 — Backend foundation

1. Configure Pydantic Settings and environment validation.
2. Add SQLAlchemy 2.x engine/session management.
3. Add PostgreSQL to Compose and health checks.
4. Configure Alembic and the first migration.
5. Create catalog models and schemas.
6. Implement product/category CRUD through a service layer and REST routes.
7. Add filtering, pagination, validation, and consistent errors.
8. Add tests using an isolated test database or disposable PostgreSQL service.
9. Document schema choices and migration workflow.

**Exit criteria:** catalog CRUD works against PostgreSQL; migrations and tests pass.

### Phase 1 — Admin UI

1. Add Jinja templates, a base layout, and static assets.
2. Build product list/detail/create/edit pages.
3. Add server-side validation and safe error messages.
4. Add HTMX interactions only where they simplify the experience.
5. Add category and brand management.
6. Ensure every mutation is authorized and CSRF-protected.

**Exit criteria:** an admin can manage catalog data in a browser.

### Phase 1 — Authentication and RBAC

1. Define users, roles, permissions, and association tables.
2. Seed a small set of permission keys and an initial admin role through a deliberate bootstrap command.
3. Implement admin sign-in/session handling and logout.
4. Implement a reusable `require_permission(...)` dependency/service.
5. Apply permissions to API routes and admin handlers.
6. Add role/user/permission management pages.
7. Add tests for role combinations, missing permissions, inactive users, and privilege escalation attempts.
8. Document the authorization matrix.

**Exit criteria:** permissions are enforced server-side and negative tests prove denied actions fail.

### Phase 1 — Media

1. Add `product_media` and its Alembic migration.
2. Define the storage interface and fake storage for tests.
3. Create an R2 bucket and restricted credentials outside the codebase.
4. Configure R2 endpoint, bucket, access key, secret key, and public base URL as environment settings.
5. Implement upload, validation, listing, primary-image selection, and deletion.
6. Add tests for invalid file type, excessive size, upload failure, and database/storage failure handling.
7. Render images in the admin panel and product API.
8. Document R2 setup and safe secret handling.
9. Later, add presigned direct uploads.

**Exit criteria:** a product can have images whose metadata is in PostgreSQL and whose bytes are stored in R2.

### Phase 1 — GraphQL and health

1. Add Strawberry schema and `/graphql`.
2. Implement catalog queries and selected mutations using existing services.
3. Add authentication/authorization rules and query safeguards.
4. Add GraphQL tests.
5. Add liveness/readiness endpoints.
6. Add an admin health page that shows real checks and process uptime.
7. Document GraphQL examples and health semantics.

**Exit criteria:** REST and GraphQL share business logic; health status is accurate and tested.

### Phase 1 — Quality and containers

1. Finalize unit, integration, API, auth, and GraphQL test organization under `tests/`.
2. Add lint, format-check, type-check, and test commands.
3. Write a multi-stage or otherwise lean Dockerfile.
4. Add Compose services for API and PostgreSQL.
5. Make startup/migration order explicit; run migrations as a controlled step rather than blindly racing multiple application replicas.
6. Verify a clean local setup from documented instructions.
7. Add GitHub Actions CI for pull requests and pushes.

**Exit criteria:** CI passes on a clean checkout and the application runs in containers.

### Phase 1 — Deployment

1. Choose a container-capable FastAPI host and a managed PostgreSQL provider.
2. Verify region, connection limits, TLS, backups, costs, and deployment/runtime requirements.
3. Configure production environment secrets through the host's secret manager.
4. Configure R2 CORS/public delivery settings only as required.
5. Run migrations as a controlled release step.
6. Add deployment workflow after CI is reliable.
7. Test health endpoints, uploads, database persistence, logs, and rollback/recovery steps.
8. Document the deployment.

**Exit criteria:** a deployed admin/API works with a persistent database and R2 media.

### Phase 2 — Next.js storefront

1. Create `storefront/` using Next.js App Router and TypeScript.
2. Configure linting, formatting, environment variables, and a basic CI workflow.
3. Build shared layout, navigation, product listing, category browsing, and product details.
4. Consume the FastAPI REST/GraphQL API through a small typed API client.
5. Implement loading, empty, and error states.
6. Add search/filter/pagination based on backend capabilities.
7. Add SEO metadata, canonical URLs, sitemap/robots handling, and suitable rendering strategies.
8. Display product images using the configured media delivery URLs.
9. Add responsive/accessibility checks and end-to-end smoke tests.
10. Deploy independently from FastAPI.

**Exit criteria:** customers can browse a responsive, indexable catalog backed by the existing API.

### Phase 2 — OAuth/OIDC passwordless sign-in

1. Decide whether the Next.js server or FastAPI owns the login callback and session boundary; document the decision before coding.
2. Register development applications with Google and Microsoft; configure exact local and production redirect URIs.
3. Add provider configuration only through environment secrets.
4. Integrate a maintained OIDC client/library.
5. Validate callback state, nonce, issuer, audience, signatures, and redirect URIs through the library's supported validation.
6. Map provider subjects to `external_identities` and local users.
7. Add safe account linking, logout, and session expiry.
8. Add tests for success, cancellation, invalid/expired state, duplicate identities, and insufficient claims.
9. Ensure customers never receive administrative permissions by default.
10. Document provider setup and account recovery.

**Exit criteria:** users can sign in without a ProCom password using configured providers, and local authorization remains enforced by FastAPI.

### Later enhancements (only after core milestones)

- Cart and order lifecycle.
- Payment provider integration using hosted/tokenized payment flows.
- Inventory reservation and concurrency controls.
- Email notifications.
- Background tasks and Redis only if justified.
- Search engine integration if PostgreSQL search becomes insufficient.
- AWS S3 adapter and a documented R2-to-S3 migration exercise.
- Observability, rate limiting, backups, restore drills, and security review.

## 12. Testing strategy

- **Unit tests:** validation, business rules, permission evaluation, storage-key generation.
- **Integration tests:** SQLAlchemy/PostgreSQL behavior, migrations, storage adapter contract.
- **API tests:** status codes, response schemas, pagination, errors, auth.
- **Authorization tests:** each permission's allow/deny cases; users with multiple roles; inactive users.
- **GraphQL tests:** query/mutation results, denied access, invalid input, complexity safeguards.
- **Media tests:** MIME/size validation, failed uploads, deletion, orphan handling.
- **Phase 2 tests:** API client behavior and storefront end-to-end catalog smoke tests; OIDC callback edge cases.
- **CI:** run lint/format checks, type checking, and tests; build the Docker image. Do not deploy if checks fail.

Use a separate test database and never point tests at production data.

## 13. Environment and secret policy

`.env.example` contains variable names and safe placeholders, never real secrets. `.env` is local-only and ignored by Git.

Likely variables, added as features are implemented:

```dotenv
APP_ENV=development
APP_NAME=ProCom
SECRET_KEY=replace-for-local-development
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/procom

R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=
R2_ENDPOINT_URL=
R2_PUBLIC_BASE_URL=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
MICROSOFT_CLIENT_ID=
MICROSOFT_CLIENT_SECRET=
OAUTH_REDIRECT_BASE_URL=
```

Keep the example aligned with actual settings. Do not add unused settings merely because they are listed here. Production secrets belong in the deployment platform's secret manager. Rotate any secret that is accidentally committed.

## 14. Documentation plan

Maintain these docs as the implementation evolves:

- `docs/architecture.md` — components and data flow.
- `docs/development.md` — prerequisites, `uv` commands, local setup, common commands.
- `docs/database.md` — ERD, relationships, constraints, migration workflow.
- `docs/authentication.md` — session/OIDC flows and security choices.
- `docs/authorization.md` — roles, permission keys, precedence, test matrix.
- `docs/media-storage.md` — R2 setup, object keys, upload flow, presigned URL roadmap.
- `docs/graphql.md` — schema examples, authorization, query safeguards.
- `docs/testing.md` — test categories and how to run them.
- `docs/deployment.md` — environments, secrets, migrations, release and rollback.
- `docs/decisions/` — concise Architecture Decision Records (ADRs) explaining significant choices.

## 15. Definition of done

A feature is complete when:

1. It works locally using documented commands.
2. It has appropriate tests, including failure/authorization cases.
3. Database changes are represented by an Alembic migration.
4. Secrets and sensitive data are handled safely.
5. Lint/type/test checks pass.
6. Relevant docs are updated.
7. It does not bypass the service layer or duplicate business rules between REST and GraphQL.
8. Its deployment/configuration impact is understood.

## 16. First working session checklist

Start with foundation only—do not implement the database, OAuth, R2, or the storefront in the first session.

- [ ] Create the project directory and initialize Git.
- [ ] Install/verify `uv` and a supported Python version.
- [ ] Initialize `pyproject.toml`.
- [ ] Add FastAPI and Uvicorn.
- [ ] Create a minimal `app/main.py`.
- [ ] Add a smoke test under `tests/`.
- [ ] Add `.gitignore`, `.env.example`, and README.
- [ ] Add `docs/development.md` and `docs/architecture.md`.
- [ ] Run the app and tests locally.
- [ ] Make the first commit.

**Guiding principle:** build the simplest working version of each layer, test it, document it, and only then add the next layer.
