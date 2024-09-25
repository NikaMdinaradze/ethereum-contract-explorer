from typing import Annotated

from fastapi import FastAPI, Query

from src.etherscan import get_contracts_by_deployer, get_deployer_contract
from src.models import EthereumAddressModel

app = FastAPI()


@app.get("/search-contract")
async def search_contract(contract_address: Annotated[EthereumAddressModel, Query()]):
    deployer = get_deployer_contract(contract_address.contract_address)
    other_deployments = get_contracts_by_deployer(deployer)
    return {
        "contract_address": contract_address.contract_address,
        "deployer": deployer,
        "other_deployments": other_deployments,
    }
