from decimal import Decimal

import pytest

from showcase.payments import (
    PaymentError,
    PaymentProvider,
    initiate_deposit,
    initiate_withdrawal,
    normalize_phone_number,
)


def _providers() -> dict[str, PaymentProvider]:
    return {
        "orange": PaymentProvider(
            name="orange",
            fee_percent=Decimal("1.50"),
            fee_flat=Decimal("2.00"),
            min_amount=Decimal("10.00"),
            max_amount=Decimal("3000.00"),
        )
    }


def test_normalize_phone_number_handles_local_botswana_format():
    assert normalize_phone_number("71234567") == "+26771234567"


def test_initiate_deposit_calculates_fee_and_tracks_metadata():
    request = initiate_deposit(
        user_phone="71234567",
        amount=Decimal("100.00"),
        provider_name="orange",
        providers=_providers(),
        transaction_ref="LEDGER-123",
    )

    assert request.phone_number == "+26771234567"
    assert request.fee == Decimal("3.50")
    assert request.transaction_ref == "LEDGER-123"


def test_initiate_withdrawal_blocks_when_balance_is_too_low():
    with pytest.raises(PaymentError):
        initiate_withdrawal(
            user_phone="+26771234567",
            destination_phone="071234567",
            amount=Decimal("100.00"),
            provider_name="orange",
            available_balance=Decimal("50.00"),
            providers=_providers(),
        )
