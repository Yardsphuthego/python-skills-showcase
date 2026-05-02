# Python Skills Showcase

This repository is a small, standalone portfolio project built to demonstrate how I use Python for backend and product logic without exposing my full private codebase.

The examples here are adapted from patterns I have used in real work, then simplified into framework-light modules so they are easy to review on their own.

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

### `payments.py`

Shows how I model payment workflows:

- provider lookup and availability checks
- fee calculation from percentage and flat charges
- phone number normalization
- deposit and withdrawal request tracking
- connector abstraction for future live integrations

### `reporting.py`

Shows how I turn raw order data into business reporting:

- monthly filtering
- daily sales summaries
- refund and cancellation tracking
- product performance ranking
- inventory and customer metrics

### `message_crypto.py`

Shows a simple secure-by-default messaging helper:

- Fernet-based encryption and decryption
- support for environment keys or explicit keys
- graceful fallback behavior when a key is missing

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
