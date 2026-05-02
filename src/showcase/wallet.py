"""
Portfolio version of wallet business logic adapted from a Django service layer.

In the original project, this logic lived in a wallet services module behind API
views. Transfers verified a user's PIN, checked balance and limits, then wrote
both wallet updates and the transaction record inside a database transaction.

This standalone version keeps the same rule flow, but replaces Django models
with dataclasses so reviewers can read the core Python logic in isolation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class WalletError(Exception):
    """Base exception for wallet operations."""


class InsufficientFundsError(WalletError):
    """Raised when the wallet balance cannot cover a transfer."""


class LimitExceededError(WalletError):
    """Raised when a transfer would cross the configured limits."""


class InvalidPinError(WalletError):
    """Raised when the caller provides a bad PIN."""


class InvalidRecipientError(WalletError):
    """Raised when the sender and recipient are the same account."""


@dataclass(slots=True)
class Wallet:
    owner_id: str
    pin: str
    balance: Decimal = Decimal("0.00")
    daily_limit: Decimal = Decimal("500.00")
    monthly_limit: Decimal = Decimal("2000.00")
    spent_today: Decimal = Decimal("0.00")
    spent_this_month: Decimal = Decimal("0.00")
    status: str = "active"
    updated_at: datetime = field(default_factory=_utc_now)

    def can_spend(self, amount: Decimal) -> tuple[bool, str]:
        # Keep the validation result machine-friendly by returning a boolean
        # and a short reason string that callers can map to domain errors.
        if self.status != "active":
            return False, "wallet is not active"
        if amount <= Decimal("0.00"):
            return False, "amount must be positive"
        if self.balance < amount:
            return False, "insufficient funds"
        if self.spent_today + amount > self.daily_limit:
            return False, "daily limit exceeded"
        if self.spent_this_month + amount > self.monthly_limit:
            return False, "monthly limit exceeded"
        return True, ""


@dataclass(slots=True)
class Transaction:
    reference: str
    sender_id: str
    recipient_id: str
    amount: Decimal
    note: str
    sender_balance_before: Decimal
    sender_balance_after: Decimal
    recipient_balance_before: Decimal
    recipient_balance_after: Decimal
    created_at: datetime = field(default_factory=_utc_now)


def verify_pin(wallet: Wallet, provided_pin: str) -> None:
    if wallet.pin != provided_pin:
        raise InvalidPinError("Incorrect PIN.")


def upgrade_wallet_limits(wallet: Wallet, tier: str) -> Wallet:
    tiers = {
        "basic": (Decimal("500.00"), Decimal("2000.00")),
        "standard": (Decimal("5000.00"), Decimal("25000.00")),
        "premium": (Decimal("20000.00"), Decimal("100000.00")),
    }
    try:
        daily_limit, monthly_limit = tiers[tier]
    except KeyError as exc:
        raise WalletError(f"Unknown tier: {tier}") from exc

    wallet.daily_limit = daily_limit
    wallet.monthly_limit = monthly_limit
    wallet.updated_at = _utc_now()
    return wallet


def transfer(
    sender: Wallet,
    recipient: Wallet,
    *,
    amount: Decimal,
    pin: str,
    note: str = "",
) -> Transaction:
    """
    Execute a wallet-to-wallet transfer as one cohesive operation.

    In a production system this would run inside a database transaction.
    Here, the function keeps the validation and balance updates together so the
    flow remains easy to reason about in a portfolio example.
    """

    verify_pin(sender, pin)

    if sender.owner_id == recipient.owner_id:
        raise InvalidRecipientError("You cannot send money to yourself.")

    # Run cheap validation before mutating any balances.
    ok, reason = sender.can_spend(amount)
    if not ok:
        if "limit" in reason:
            raise LimitExceededError(reason)
        raise InsufficientFundsError(reason)

    # Capture both balances before the transfer so the transaction record tells
    # the full story of what changed.
    sender_before = sender.balance
    recipient_before = recipient.balance

    # Apply the transfer and update spending counters in one place so the
    # wallet state stays internally consistent.
    sender.balance -= amount
    recipient.balance += amount
    sender.spent_today += amount
    sender.spent_this_month += amount
    sender.updated_at = _utc_now()
    recipient.updated_at = _utc_now()

    return Transaction(
        reference=f"TXN-{uuid4().hex[:12].upper()}",
        sender_id=sender.owner_id,
        recipient_id=recipient.owner_id,
        amount=amount,
        note=note,
        sender_balance_before=sender_before,
        sender_balance_after=sender.balance,
        recipient_balance_before=recipient_before,
        recipient_balance_after=recipient.balance,
    )
