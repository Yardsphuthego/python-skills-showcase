"""
Portfolio version of payment-service logic adapted from a Django backend.

In the original project, deposits and withdrawals were tracked with payment
request models, provider configuration records, and wallet ledger references.
The service layer normalized phone numbers, calculated provider fees, enforced
provider limits, and prepared request metadata for later provider integration.

This demo keeps the same decision-making logic while removing the framework and
database details so the Python flow is easier to review publicly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Protocol
from uuid import uuid4


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PaymentError(Exception):
    """Base exception for payment flows."""


class ProviderUnavailableError(PaymentError):
    """Raised when the selected provider is not active."""


@dataclass(slots=True)
class PaymentProvider:
    name: str
    fee_percent: Decimal
    fee_flat: Decimal
    min_amount: Decimal
    max_amount: Decimal
    active: bool = True


@dataclass(slots=True)
class PaymentRequest:
    direction: str
    provider_name: str
    amount: Decimal
    fee: Decimal
    phone_number: str
    transaction_ref: str
    status: str = "pending"
    metadata: dict[str, str] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: f"PAY-{uuid4().hex[:10].upper()}")
    created_at: datetime = field(default_factory=_utc_now)


@dataclass(slots=True)
class SettlementResult:
    status: str
    provider_ref: str = ""
    message: str = ""
    raw: dict | None = None


class SettlementConnector(Protocol):
    def create_transfer(
        self,
        *,
        amount: Decimal,
        destination_phone: str,
        reference: str,
        metadata: dict[str, str],
    ) -> SettlementResult:
        ...


class NoopSettlementConnector:
    """Safe default that records intent without calling any live provider."""

    def create_transfer(
        self,
        *,
        amount: Decimal,
        destination_phone: str,
        reference: str,
        metadata: dict[str, str],
    ) -> SettlementResult:
        return SettlementResult(
            status="queued",
            message="No live connector configured yet.",
            raw={
                "reference": reference,
                "destination_phone": destination_phone,
                "amount": str(amount),
                "metadata": metadata,
            },
        )


def normalize_phone_number(value: str) -> str:
    raw = (value or "").strip()
    if not raw:
        return raw
    if raw.startswith("+"):
        digits = "".join(ch for ch in raw[1:] if ch.isdigit())
        return f"+{digits}" if digits else raw

    digits = "".join(ch for ch in raw if ch.isdigit())
    # These rules mirror a common Botswana formatting flow:
    # local 8-digit numbers become +267..., leading 0 is stripped, and
    # already-international values are normalized to a clean +<digits> shape.
    if digits.startswith("267"):
        return f"+{digits}"
    if len(digits) == 8:
        return f"+267{digits}"
    if len(digits) == 9 and digits.startswith("0"):
        return f"+267{digits[1:]}"
    return f"+{digits}" if digits else raw


def get_active_provider(providers: dict[str, PaymentProvider], provider_name: str) -> PaymentProvider:
    provider = providers.get(provider_name)
    if not provider or not provider.active:
        raise ProviderUnavailableError(
            f"Payment provider '{provider_name}' is not available. Please try a different provider."
        )
    return provider


def calculate_fee(amount: Decimal, provider: PaymentProvider) -> Decimal:
    variable_fee = amount * provider.fee_percent / Decimal("100")
    return variable_fee + provider.fee_flat


def initiate_deposit(
    *,
    user_phone: str,
    amount: Decimal,
    provider_name: str,
    providers: dict[str, PaymentProvider],
    transaction_ref: str | None = None,
) -> PaymentRequest:
    provider = get_active_provider(providers, provider_name)
    fee = calculate_fee(amount, provider)
    return PaymentRequest(
        direction="deposit",
        provider_name=provider.name,
        amount=amount,
        fee=fee,
        phone_number=normalize_phone_number(user_phone),
        transaction_ref=transaction_ref or f"LEDGER-{uuid4().hex[:10].upper()}",
        # Metadata gives downstream systems lightweight context without
        # bloating the main payment request fields.
        metadata={"initiated_at": _utc_now().isoformat()},
    )


def initiate_withdrawal(
    *,
    user_phone: str,
    destination_phone: str,
    amount: Decimal,
    provider_name: str,
    available_balance: Decimal,
    providers: dict[str, PaymentProvider],
    transaction_ref: str | None = None,
) -> PaymentRequest:
    provider = get_active_provider(providers, provider_name)

    # Provider limits are checked before balance so callers get the most useful
    # business-facing error first.
    if amount < provider.min_amount:
        raise PaymentError(f"Minimum withdrawal is {provider.min_amount}.")
    if amount > provider.max_amount:
        raise PaymentError(f"Maximum withdrawal is {provider.max_amount}.")

    fee = calculate_fee(amount, provider)
    total_debit = amount + fee
    if available_balance < total_debit:
        raise PaymentError("Insufficient balance for withdrawal and fees.")

    return PaymentRequest(
        direction="withdrawal",
        provider_name=provider.name,
        amount=amount,
        fee=fee,
        phone_number=normalize_phone_number(destination_phone),
        transaction_ref=transaction_ref or f"LEDGER-{uuid4().hex[:10].upper()}",
        metadata={
            # Keeping total debit in metadata makes reconciliation easier when
            # the ledger amount and provider amount need to be compared later.
            "initiated_by": normalize_phone_number(user_phone),
            "total_debit": str(total_debit),
        },
    )
