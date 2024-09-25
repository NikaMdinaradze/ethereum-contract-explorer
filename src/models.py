import re

from pydantic import BaseModel, field_validator


class EthereumAddressModel(BaseModel):
    contract_address: str

    @field_validator("contract_address")
    def validate_ethereum_address(cls, v: str) -> str:  # noqa
        if not re.match(r"^0x[a-fA-F0-9]{40}$", v):
            raise ValueError("Invalid Ethereum contract address")
        return v
