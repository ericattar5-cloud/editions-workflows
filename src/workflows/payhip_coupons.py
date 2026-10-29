"""Workflows Payhip — coupons LOT3 / LOT10 pour Les Editions du Discernement.

Utilise la cle PAYHIP_API_KAY (workspace secret) pour :
- payhip-list-coupons : lister les coupons (valide aussi la cle)
- payhip-create-lot-coupons : creer LOT3 (-15%, min 2.97 EUR) et LOT10 (-40%, min 9.90 EUR)
  sur une collection Payhip (le tome I en est exclu car hors collection).
"""

import os

from pydantic import BaseModel

import mistralai.workflows as workflows

# httpx n'est utilise que dans les activities ; il faut le declarer
# pass-through pour la sandbox des workflows.
with workflows.workflow.unsafe.imports_passed_through():
    import httpx  # noqa: F811

PAYHIP_BASE = "https://payhip.com/api/v2"

# Montants en centimes (regle decidee par Eric, 26/10)
LOT3_MIN_CENTS = 297    # 2,97 EUR
LOT10_MIN_CENTS = 990   # 9,90 EUR


def _headers() -> dict:
    return {"payhip-api-key": os.environ["PAYHIP_API_KEY"]}


class ListCouponsInput(BaseModel):
    limit: int = 100


@workflows.activity()
async def list_coupons(limit: int) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(
            f"{PAYHIP_BASE}/coupons",
            params={"limit": limit, "offset": 0},
            headers=_headers(),
        )
        r.raise_for_status()
        return r.json()


@workflows.workflow.define(
    name="payhip-list-coupons",
    workflow_display_name="Payhip — Lister les coupons",
    workflow_description="Liste tous les coupons Payhip et valide la cle API du coffre.",
)
class ListCouponsWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, input: ListCouponsInput) -> dict:
        return await list_coupons(input.limit)


class CreateLotCouponsInput(BaseModel):
    collection_id: str
    lot3_percent: float = 15.0
    lot10_percent: float = 40.0


@workflows.activity()
async def create_coupon(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(f"{PAYHIP_BASE}/coupons", data=payload, headers=_headers())
        if r.status_code not in (200, 201):
            return {"error": True, "status_code": r.status_code, "body": r.text}
        return {"error": False, "coupon": r.json().get("data")}


@workflows.activity()
async def coupon_codes_exist(codes: list[str]) -> dict:
    existing = await list_coupons(100)
    found = []
    items = (existing.get("data") or {}).get("coupons") or []
    for it in items:
        if it.get("code") in codes:
            found.append(it.get("code"))
    return {"existing": found}


@workflows.workflow.define(
    name="payhip-create-lot-coupons",
    workflow_display_name="Payhip — Creer les coupons LOT3 / LOT10",
    workflow_description=(
        "Cree les coupons LOT3 (-15% des 2,97 EUR d'achat) et LOT10 (-40% des 9,90 EUR) "
        "sur la collection 'recits courts'. Idempotent : ne recree pas un coupon existant."
    ),
)
class CreateLotCouponsWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, input: CreateLotCouponsInput) -> dict:
        existing = (await coupon_codes_exist(["LOT3", "LOT10"]))["existing"]
        created = {}
        if "LOT3" not in existing:
            created["LOT3"] = await create_coupon({
                "code": "LOT3",
                "coupon_type": "collection",
                "collection_id": input.collection_id,
                "percent_off": input.lot3_percent,
                "minimum_purchase_amount": LOT3_MIN_CENTS,
                "notes": "Palier 3 titres : -15% (regle Eric 26/10)",
            })
        if "LOT10" not in existing:
            created["LOT10"] = await create_coupon({
                "code": "LOT10",
                "coupon_type": "collection",
                "collection_id": input.collection_id,
                "percent_off": input.lot10_percent,
                "minimum_purchase_amount": LOT10_MIN_CENTS,
                "notes": "Palier 10 titres : -40% (regle Eric 26/10)",
            })
        return {"already_existing": existing, "created": created}
