# Python Skills Showcase

This repository is a small, standalone portfolio project built to demonstrate how I use Python for backend and product logic without exposing my full private codebase.

The examples here are adapted from patterns I have used in real work, then simplified into framework-light modules so they are easy to review on their own.

Each module now also includes context about how the same logic worked in the
original project, so reviewers can see both the standalone Python example and
the real backend scenario it was adapted from.

## What This Shows

- Business logic design separated from transport or UI concerns
- Wallet-style balance handling and transfer validation
- Payment workflows with provider rules, fee calculation, and request tracking
- Reporting logic that aggregates orders into useful business summaries
- Secure message encryption and decryption using `cryptography`
- Basic automated testing with `pytest`

## Repository Structure

```text
python-skills-showcase/
├── README.md
├── pyproject.toml
├── src/showcase/
│   ├── wallet.py
│   ├── payments.py
│   ├── reporting.py
│   └── message_crypto.py
└── tests/
    ├── test_wallet.py
    ├── test_payments.py
    ├── test_reporting.py
    └── test_message_crypto.py
```

## Module Highlights

### `wallet.py`

Shows how I structure transactional business logic:

- custom exceptions for clear failure modes
- transfer validation with PIN checks
- balance updates with before/after snapshots
- configurable daily and monthly spending limits

Original project context:
In the source application, this logic lived in a Django service layer behind
wallet and transfer API endpoints. The real version used database transactions
and wallet models so sender balances, recipient balances, and transaction
history stayed consistent.

### `payments.py`

Shows how I model payment workflows:

- provider lookup and availability checks
- fee calculation from percentage and flat charges
- phone number normalization
- deposit and withdrawal request tracking
- connector abstraction for future live integrations

Original project context:
In the source application, this sat between the wallet system and Botswana
mobile money providers. It prepared payment requests, applied provider rules,
tracked fees, and stored metadata needed for reconciliation and callbacks.

### `reporting.py`

Shows how I turn raw order data into business reporting:

- monthly filtering
- daily sales summaries
- refund and cancellation tracking
- product performance ranking
- inventory and customer metrics

Original project context:
In the source application, this reporting service summarized marketplace shop
activity into monthly business reports. It was designed for operational review,
shop-owner dashboards, and finance-oriented reporting outputs.

### `message_crypto.py`

Shows a simple secure-by-default messaging helper:

- Fernet-based encryption and decryption
- support for environment keys or explicit keys
- graceful fallback behavior when a key is missing

Original project context:
In the source application, message content was encrypted before database
storage and decrypted when shown back inside the chat experience. The public
demo keeps that same idea in a smaller utility module.

## Test Files

The `tests/` folder does more than verify behavior. Each test file also
explains how the public example maps back to the original private project:

- `test_wallet.py` explains the wallet transfer and tier-limit flow
- `test_payments.py` explains the provider-fee and withdrawal checks
- `test_reporting.py` explains the monthly shop-report aggregation
- `test_message_crypto.py` explains the encrypt-at-rest message flow

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Example Test Run

```bash
pytest -q
```

## Why I Made This Repo

My main application repositories are private, so I created this separate showcase to illustrate the kind of Python backend work I do:

- domain logic
- data processing
- security-minded utilities
- testing

This lets reviewers see my coding style and problem-solving approach without exposing proprietary project details.
