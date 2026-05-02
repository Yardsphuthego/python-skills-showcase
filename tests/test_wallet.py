from decimal import Decimal

import pytest

from showcase.wallet import InvalidPinError, Wallet, transfer, upgrade_wallet_limits


def test_transfer_updates_both_wallets_and_tracks_balances():
    sender = Wallet(owner_id="alice", pin="1234", balance=Decimal("250.00"))
    recipient = Wallet(owner_id="bob", pin="9999", balance=Decimal("50.00"))

    txn = transfer(sender, recipient, amount=Decimal("40.00"), pin="1234", note="Lunch split")

    assert txn.amount == Decimal("40.00")
    assert sender.balance == Decimal("210.00")
    assert recipient.balance == Decimal("90.00")
    assert txn.sender_balance_before == Decimal("250.00")
    assert txn.recipient_balance_after == Decimal("90.00")


def test_transfer_rejects_bad_pin():
    sender = Wallet(owner_id="alice", pin="1234", balance=Decimal("250.00"))
    recipient = Wallet(owner_id="bob", pin="9999", balance=Decimal("50.00"))

    with pytest.raises(InvalidPinError):
        transfer(sender, recipient, amount=Decimal("10.00"), pin="0000")


def test_upgrade_wallet_limits_changes_tier_thresholds():
    wallet = Wallet(owner_id="alice", pin="1234")

    upgrade_wallet_limits(wallet, "premium")

    assert wallet.daily_limit == Decimal("20000.00")
    assert wallet.monthly_limit == Decimal("100000.00")
