import os

import requests
from fastapi import HTTPException, status


class ContractScanner:
    ETHERSCAN_API_URL = "https://api.etherscan.io/api"

    def __init__(self, contract_address: str, api_key: str = None):
        self.contract_address = contract_address
        self.api_key = api_key if api_key else os.environ.get("ETHERSCAN_API_KEY")

    def _make_request(self, params: dict) -> dict:
        response = requests.get(self.ETHERSCAN_API_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to fetch data from Etherscan: {response.status_code}",
            )
        return response.json()

    def get_deployer_address(self) -> str:
        params = {
            "module": "contract",
            "action": "getcontractcreation",
            "contractaddresses": self.contract_address,
            "apikey": self.api_key,
        }
        result = self._make_request(params).get("result")
        return result[0].get("contractCreator") if result else None

    def get_other_deployments(
        self, start_block: int = 0, end_block: int = 99999999
    ) -> list:
        params = {
            "module": "account",
            "action": "txlist",
            "address": self.get_deployer_address(),
            "startblock": start_block,
            "endblock": end_block,
            "sort": "asc",
            "apikey": self.api_key,
        }
        result = self._make_request(params).get("result")
        return [tx.get("contractAddress") for tx in result if tx.get("contractAddress")]

    def get_top_interactors(
        self, start_block: int = 0, end_block: int = 99999999
    ) -> dict:
        params = {
            "module": "account",
            "action": "txlist",
            "address": self.contract_address,
            "startblock": start_block,
            "endblock": end_block,
            "sort": "asc",
            "apikey": self.api_key,
        }
        result = self._make_request(params).get("result")

        interactions = {}
        for tx in result:
            from_address = tx.get("from")
            if from_address:
                interactions[from_address] = interactions.get(from_address, 0) + 1

        return dict(sorted(interactions.items(), key=lambda x: x[1], reverse=True))
