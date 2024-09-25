import os

import requests
from fastapi import HTTPException, status

ETHERSCAN_API_KEY = os.environ.get("ETHERSCAN_API_KEY")
ETHERSCAN_API_URL = "https://api.etherscan.io/api"


def get_deployer_contract(contract_address: str) -> str:
    params = {
        "module": "contract",
        "action": "getcontractcreation",
        "contractaddresses": contract_address,
        "apikey": ETHERSCAN_API_KEY,
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)

    if not response.status_code == 200:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch data from Etherscan: {response.status_code}",
        )

    result = response.json().get("result")
    deployer_address = None if not result else result[0].get("contractCreator")
    return deployer_address


def get_contracts_by_deployer(
    deployer_address: str, start_block: int = 0, end_block: int = 99999999
) -> list:
    params = {
        "module": "account",
        "action": "txlist",
        "address": deployer_address,
        "startblock": start_block,
        "endblock": end_block,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY,
    }

    response = requests.get(ETHERSCAN_API_URL, params=params)

    if not response.status_code == 200:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch data from Etherscan: {response.status_code}",
        )

    result = response.json().get("result")

    deployed_contracts = [
        tx.get("contractAddress") for tx in result if tx.get("contractAddress") != ""
    ]

    return deployed_contracts
