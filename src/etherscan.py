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
    if not result:
        deployer_address = None
    else:
        deployer_address = result[0].get("contractCreator")
    return deployer_address

