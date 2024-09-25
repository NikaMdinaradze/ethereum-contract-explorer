from typing import Annotated

from fastapi import FastAPI, Query

from src.etherscan import ContractScanner
from src.models import ContractInfoResponse, EthereumAddressModel

app = FastAPI()


@app.get("/search-contract", response_model=ContractInfoResponse)
async def search_contract(contract_address: Annotated[EthereumAddressModel, Query()]):
    """
    Endpoint to search for contract information based on the given contract address.
    """
    contract = ContractScanner(contract_address.contract_address)
    return {
        "contract_address": contract_address.contract_address,
        "deployer": contract.get_deployer_address(),
        "other_deployments": contract.get_other_deployments(),
        "top_interactors": contract.get_top_interactors(),
    }
