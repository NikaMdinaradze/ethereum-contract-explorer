from typing import Annotated

from fastapi import FastAPI, Query

from src.models import EthereumAddressModel
from src.etherscan import get_deployer_contract

app = FastAPI()


@app.get("/search-contract")
async def search_contract(contract_address: Annotated[EthereumAddressModel, Query()]):
    deployer = get_deployer_contract(contract_address.contract_address)
    return {"contract_address": contract_address.contract_address, "deployer": deployer}
