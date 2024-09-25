import os

import requests
from fastapi import HTTPException, status


class ContractScanner:
    """A class to interact with the Etherscan API for retrieving contract-related information."""

    ETHERSCAN_API_URL = "https://api.etherscan.io/api"

    def __init__(self, contract_address: str, api_key: str = None):
        """
        Initializes the ContractScanner with the contract address and API key.

        Args:
            contract_address (str): The address of the contract to analyze.
            api_key (str, optional): The Etherscan API key. If not provided, it will be fetched from the environment.
        """
        self.contract_address = contract_address
        self.api_key = api_key if api_key else os.environ.get("ETHERSCAN_API_KEY")

    def _make_request(self, params: dict) -> dict:
        """
        Makes a request to the Etherscan API, if access is failed raises internal server error.

        Args:
            params (dict): The parameters for the API request.

        Raises:
            HTTPException: If the API request fails.

        Returns:
            dict: The JSON response from the API.
        """
        response = requests.get(self.ETHERSCAN_API_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to fetch data from Etherscan: {response.status_code}",
            )
        return response.json()

    def get_deployer_address(self) -> str:
        """
        Retrieves the address of the deployer of the contract.

        Returns:
            str: The address of the contract creator, or None if not found.
        """
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
        """
        Retrieves a list of contracts deployed by the same deployer as the current contract.

        Args:
            start_block (int, optional): The starting block number for the transaction list. Default is 0.
            end_block (int, optional): The ending block number for the transaction list. Default is 99999999.

        Returns:
            list: A list of addresses of contracts deployed by the same deployer.
        """
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
        """
        Retrieves the addresses that have interacted the most with the contract.

        Args:
            start_block (int, optional): The starting block number for the transaction list. Default is 0.
            end_block (int, optional): The ending block number for the transaction list. Default is 99999999.

        Returns:
            dict: A dictionary of addresses and their interaction counts, sorted by interaction count in descending order.
        """
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
