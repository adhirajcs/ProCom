# ProCom Architecture

ProCom (Product Commerce) is a product management and commerce platform.

## Phase 1: Backend and administration

- FastAPI provides REST and GraphQL APIs.
- Jinja2 renders the server-side admin panel.
- PostgreSQL stores application data.
- SQLAlchemy manages relational data access.
- Alembic manages database migrations.
- Cloudflare R2 stores product media.
- pytest validates application behavior.

## Phase 2: Storefront

- Next.js and TypeScript provide the customer storefront.
- The storefront consumes the FastAPI APIs.
- Google and Microsoft OpenID Connect sign-in
  provide passwordless customer authentication.

## Architectural principles

1. Keep business rules in the backend service layer.
2. Keep database access out of frontend applications.
3. Store media binaries in object storage, not PostgreSQL.
4. Enforce authorization on the server.
5. Test features and document important decisions.
6. Keep configuration and secrets outside application code.
