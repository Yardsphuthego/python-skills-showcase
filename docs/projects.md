# Selected Project Portfolio

[Back to the portfolio](../README.md)

My work spans Python backends, commerce, public-service workflows, developer tools, and full-stack applications. The summaries below describe features found in the project repositories. They are not claims of production deployment, external integration, or independently verified security.

Private projects are represented by summaries only. Demonstrations and selected code walkthroughs are available on request.

## Commerce and Payment Platform

**Semausu · Django · Python · Flutter**

A marketplace and payment application with backend modules for accounts, shops, orders, wallets, payment requests, messaging, and analytics.

- Wallet services cover transfers, spending limits, transaction history, and QR payment workflows.
- Marketplace modules cover inventory, point-of-sale workflows, and shop reporting.
- Separate service, model, serializer, and view layers organise backend responsibilities.
- The repository includes a Flutter mobile application alongside the Django backend.

**Skills illustrated:** business-rule modelling, relational application design, API development, monetary calculations, and backend service organisation.

**Public code to review:** [wallet transfers](../src/showcase/wallet.py), [payment requests](../src/showcase/payments.py), [reporting](../src/showcase/reporting.py), and [message encryption](../src/showcase/message_crypto.py). These are simplified examples; see the [walkthroughs and demo boundaries](python-examples.md).

**Access:** private full application; standalone examples available here.

## MedLocate

**Medicine availability and prescription workflow prototype · Python · Django · openpyxl · PostgreSQL/SQLite**

A Botswana-focused prototype for locating medicine stock at participating facilities and managing prescription workflows with synthetic demonstration data.

- Facility inventory maintenance and medicine search.
- Excel import previews with row-level validation before committing inventory changes.
- Multi-item prescriptions, QR token handling, and partial/full dispensing workflows.
- Transactional stock updates and audit records.
- Workflow tests cover invalid spreadsheet input, prescription access, expiry, and rollback when stock is insufficient.

**Skills illustrated:** data validation, database transactions, role-based workflows, audit trails, and testing of failure cases.

**Access:** private prototype; demonstration and selected walkthrough available on request. This is a software portfolio project, not a clinical service.

## TEBELO

**City safety and public-service operations · Python · Django · Django REST Framework · PostgreSQL/PostGIS · Docker**

An application for reporting incidents, routing work to organisations, and tracking public-service cases.

- Incident reporting with location data and evidence handling.
- Organisation-scoped work queues, incident state changes, and audit records.
- Public map output designed to exclude report descriptions and reporter identities.
- A service-delivery engine for policy matching, duty assignment, overdue notifications, and organisation handoffs.
- Workflow tests cover access boundaries, map redaction, routing, and repeat-safe escalation behaviour.

**Skills illustrated:** geospatial application design, workflow modelling, access control, background processing, and API development.

**Access:** private application; demonstration and selected walkthrough available on request. Implemented workflows do not imply live government or emergency-service integration.

## BOPA

**Visual programming and learning IDE · TypeScript · React · Tauri/Rust · Python**

A local-first development environment that connects a visual canvas, generated source, and preview output through a versioned Visual Intermediate Representation (VIR).

- Canvas components, drawing and recognition tools, and editable project structure.
- Code adapters that generate Django project files and React output.
- Local project persistence and portable project import/export.
- Native commands for running Python and JavaScript learning exercises.
- Tests for project generation, canvas behaviour, recognition, and project structure.

**Skills illustrated:** schema design, code generation, frontend state management, desktop integration, and automated testing.

**Access:** private application; demonstration and selected walkthrough available on request.

## CARMAVUNAPARTS

**Car-parts search and shop management · Python · FastAPI · SQLAlchemy · Redis · React**

A car-parts platform combining a web interface with USSD search workflows.

- Multi-step USSD sessions for location selection and part searches.
- Session storage using Redis with database fallback logic.
- Shop and inventory management, subscriptions, and payment-confirmation workflows.
- Search logging, analytics services, and application health endpoints.
- Tests for branch inventory access, dashboard queries, and shop relationships.

**Skills illustrated:** stateful menu workflows, API design, caching, relational data modelling, and web/backend integration.

**Access:** private application; demonstration and selected walkthrough available on request. USSD implementation does not by itself establish a live telecom integration.

## Student Voting System

**THUTO · Python · FastAPI · SQLAlchemy · React · TypeScript**

A student voting application with backend modules for elections, candidates, voter rolls, users, and votes, alongside election and administration interfaces.

- API routes for casting votes, checking voter status, and retrieving election votes.
- Election and candidate management modules.
- React interfaces for elections, user profiles, and administration.

**Skills illustrated:** REST API development, relational modelling, frontend/backend integration, and application workflow design.

**Public code to review:** [voting routes](https://github.com/Yardsphuthego/thabang_new/blob/HEAD/Backend/routes/votes.py), [election routes](https://github.com/Yardsphuthego/thabang_new/blob/HEAD/Backend/routes/elections.py), and [election interface](https://github.com/Yardsphuthego/thabang_new/blob/HEAD/Frontend/src/pages/Elections.tsx).

The public repository's main README describes an earlier document-sharing application; the links above point directly to its voting implementation. This summary describes code structure, not an election-security assessment.

**Access:** a public implementation is available in [thabang_new](https://github.com/Yardsphuthego/thabang_new); the related THUTO repository is private.

## TAIMS Platform

**Water-storage asset management · TypeScript · Next.js · React/Vite · PostgreSQL**

A tank asset integrity management application with API routes and interfaces for assets, inspections, work orders, and reports.

- Asset records and inspection workflows.
- Work-order tracking and portfolio reporting.
- Authentication, administration, document, and audit modules.
- Separate API and frontend applications backed by PostgreSQL.

**Skills illustrated:** full-stack application structure, REST APIs, operational data modelling, and reporting.

**Access:** [Browse the public repository](https://github.com/Yardsphuthego/taims-platform).

## Food Inflation Forecasting

**AI forecasting project · Project summary from my CV**

I worked on an AI project focused on forecasting food inflation. A project walkthrough is available on request.

The implementation, dataset, model details, and evaluation results are not included in this showcase. No accuracy or performance claim is made here.

## Request a Walkthrough

Contact [ns24-035@thuto.bac.ac.bw](mailto:ns24-035@thuto.bac.ac.bw) with the project you would like to discuss.
