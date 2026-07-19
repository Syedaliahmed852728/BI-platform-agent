from __future__ import annotations

from business.entity_config.domains.customer_finance import customer_finance
from business.entity_config.domains.inventory import inventory
from business.entity_config.domains.purchase_orders import purchase_orders
from business.entity_config.domains.sales import sales
from business.entity_config.models import DomainConfig


ENTITY_CONFIG: dict[str, DomainConfig] = {
    "sales": sales,
    "purchase_orders": purchase_orders,
    "inventory": inventory,
    "customer_finance": customer_finance,
}


def get_domain(name: str) -> DomainConfig | None:
    return ENTITY_CONFIG.get(name)
