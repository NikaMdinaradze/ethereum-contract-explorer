from typing import Annotated

from fastapi import FastAPI, Query

from src.etherscan import (
    get_contracts_by_deployer,
    get_deployer_contract,
    get_top_interactors,
)
from src.models import EthereumAddressModel

app = FastAPI()


@app.get("/search-contract")
async def search_contract(contract_address: Annotated[EthereumAddressModel, Query()]):
    deployer = get_deployer_contract(contract_address.contract_address)
    other_deployments = get_contracts_by_deployer(deployer)
    top_interactors = get_top_interactors(contract_address.contract_address)
    return {
        "contract_address": contract_address.contract_address,
        "deployer": deployer,
        "other_deployments": other_deployments,
        "top_interactors": top_interactors,
    }
