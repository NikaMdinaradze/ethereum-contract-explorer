# Ethereum Contract Scanner

## Overview

The Ethereum Contract Scanner is a FastAPI application that allows users to search for information related to Ethereum smart contracts. It retrieves details such as the deployer of a contract, other contracts deployed by the same entity, and the top interactors with the contract.

## Features

- Search for Ethereum contract information using contract addresses.
- Retrieve the deployer address of a contract.
- List other contracts deployed by the same deployer.
- Identify the top interactors with the contract.

## Requirements

- Docker
- Docker Compose

## Getting Started

### Clone the Repository

```bash
git clone git@github.com:NikaMdinaradze/ethereum-contract-explorer.git
cd ethereum-contract-scanner
```

### Add env variables
```text
  create env directory, copy files from env-pattern directory and fill the
  variables with appropriate values.
```
### Start project with docker
```bash
docker-compose build
docker-compose up
```
Visit SwaggerUI: http://localhost:8000/docs
### Examples

```bash
curl -X GET "http://localhost:8000/search-contract?contract_address=0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
```

```json
{
    "contract_address": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    "deployer": "0x1234567890abcdef1234567890abcdef12345678",
    "other_deployments": [
        "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
        "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
    ],
    "top_interactors": {
        "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd": 10,
        "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef": 5
    }
}

```