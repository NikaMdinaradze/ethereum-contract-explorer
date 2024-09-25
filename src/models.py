import re

from pydantic import BaseModel, field_validator


class EthereumAddressModel(BaseModel):
    """
    A Pydantic model to represent an Ethereum contract address.
    """

    contract_address: str

    @field_validator("contract_address")
    def validate_ethereum_address(cls, v: str) -> str:  # noqa
        """
        An Ethereum address is considered valid if it:
        - Starts with '0x'
        - Is followed by exactly 40 hexadecimal characters (0-9, a-f, A-F)
        """
        if not re.match(r"^0x[a-fA-F0-9]{40}$", v):
            raise ValueError("Invalid Ethereum contract address")
        return v
