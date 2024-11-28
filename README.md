# Policy Enforcement API - Stage 1

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python src.main
```

## Running Tests

```bash
pytest tests/
```

## API Endpoints

- POST /policies: Create a policy
- GET /policies: List all policies
- GET /policies/{id}: Read a specific policy
- PUT /policies/{id}: Update a policy
- DELETE /policies/{id}: Delete a policy

## Assumptions

- A rule type cannot be changed