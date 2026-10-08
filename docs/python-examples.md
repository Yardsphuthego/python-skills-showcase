# Python Example Walkthroughs

[Back to the portfolio](../README.md)

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

Shows a simplified Fernet messaging helper:

- Fernet-based encryption and decryption
- support for environment keys or explicit keys
- plaintext fallback when a key is missing (demo behaviour, not a production security guarantee)

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

## Demo boundaries

These examples use in-memory objects rather than a live Django application or database.

- Wallet PINs are compared directly in this demo; there is no credential hashing, database transaction, concurrency control, or automatic spending-period reset.
- Payment requests use a no-op connector; this repository does not process live payments.
- The encryption helper can return plaintext without a configured key and reshapes invalid key input for convenience. Production code should require valid keys and use appropriate key management.

Read the [source](../src/showcase/) alongside the [tests](../tests/) to see exactly what each example implements.
