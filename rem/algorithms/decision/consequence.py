"""Consequence descriptors z_t and tier map kappa (Chapter 3, Tables 3.7, 3.10, 3.11).

Status: CHAPTER 3 ILLUSTRATIVE POLICY, PENDING SUPERVISOR APPROVAL (SD-2).
Chapter 3 Table 3.11 is labelled "Illustrative consequence tiers (policy
pending supervisor approval)" and the amount limit is "declared". All values are
supplied by the caller; there is no default tier map or limit.

Consequence descriptors never enter the probability model (Chapter 3 Sec. 3.6.2
design rule 2); they affect the verdict only through the loss.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Sequence

__all__ = ["ConsequenceDescriptors", "ConsequenceTierMap", "STATUS"]

STATUS = "CHAPTER 3 TABLE 3.11 (ILLUSTRATIVE) — PENDING SUPERVISOR APPROVAL (SD-2)"


@dataclass(frozen=True)
class ConsequenceDescriptors:
    """z_t for one proposed action (Table 3.10)."""

    category: str
    amount: Optional[float]
    recurring_payment_change: bool
    credential_change: bool


@dataclass(frozen=True)
class ConsequenceTierMap:
    """kappa(z_t) -> k_t.

    Args:
        categories: Category name -> tools (Table 3.7).
        tier_of: Tier per tier-map key: ``read``, ``profile_change``,
            ``value_transfer_at_or_below_limit``, ``value_transfer_above_limit``,
            ``payment_modification``, ``credential_change``.
        amount_limit: Declared amount limit for value transfers.
    """

    categories: Mapping[str, Sequence[str]]
    tier_of: Mapping[str, int]
    amount_limit: float

    def __post_init__(self) -> None:
        required = {
            "read",
            "profile_change",
            "value_transfer_at_or_below_limit",
            "value_transfer_above_limit",
            "payment_modification",
            "credential_change",
        }
        missing = required - set(self.tier_of)
        if missing:
            raise ValueError(f"Tier map is incomplete; missing {sorted(missing)}.")

    def category_of(self, tool: str) -> str:
        """Action category of ``tool``.

        Raises:
            KeyError: If the tool belongs to no declared category.
        """
        for name, tools in self.categories.items():
            if tool in tools:
                return name
        raise KeyError(f"Tool {tool!r} is not in any declared action category.")

    def descriptors(self, tool: str, args: Mapping[str, Any]) -> ConsequenceDescriptors:
        """Extract z_t from the action itself."""
        category = self.category_of(tool)
        amount = None
        raw = args.get("amount")
        if raw is not None:
            try:
                amount = float(raw)
            except (TypeError, ValueError):
                amount = None
        return ConsequenceDescriptors(
            category=category,
            amount=amount,
            recurring_payment_change=category == "payment_modification",
            credential_change=category == "credential_change",
        )

    def tier(self, tool: str, args: Mapping[str, Any]) -> int:
        """k_t = kappa(z_t).

        A value transfer whose amount is absent or unparseable is assigned the
        above-limit tier: an unknown amount is not treated as a small one.
        """
        z = self.descriptors(tool, args)
        if z.category == "value_transfer":
            if z.amount is not None and abs(z.amount) <= self.amount_limit:
                return int(self.tier_of["value_transfer_at_or_below_limit"])
            return int(self.tier_of["value_transfer_above_limit"])
        return int(self.tier_of[z.category])

    def describe(self) -> Dict[str, Any]:
        """Serialisable summary for audit records."""
        return {
            "categories": {k: list(v) for k, v in self.categories.items()},
            "tier_of": dict(self.tier_of),
            "amount_limit": self.amount_limit,
            "status": STATUS,
        }
