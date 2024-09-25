from typing import Annotated

from fastapi import FastAPI, Query

from src.models import EthereumAddressModel

app = FastAPI()


@app.get("/search-contract")
async def search_contract(contract_address: Annotated[EthereumAddressModel, Query()]):
    return contract_address
