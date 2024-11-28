import json
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.api import PolicyAPI
from src.models import PolicyModel, PolicyResponse

app = FastAPI()
policy_api = PolicyAPI()


class MessageResponse(BaseModel):
    message: str


@app.post("/policies", response_model=str, summary="Create a new policy")
def create_policy(policy_data: PolicyModel):
    try:
        policy_json = policy_data.model_dump_json()
        return policy_api.create_policy(policy_json)
    except HTTPException as e:
        raise e


@app.get("/policies/{policy_id}", response_model=PolicyResponse, summary="Get a policy by ID")
def read_policy(policy_id: str):
    try:
        return PolicyResponse(**json.loads(policy_api.read_policy(json.dumps(policy_id))))
    except HTTPException as e:
        raise e


@app.put("/policies/{policy_id}", response_model=MessageResponse, summary="Update a policy by ID")
def update_policy(policy_id: str, policy_data: PolicyModel):
    try:
        policy_api.update_policy(json.dumps(policy_id), policy_data.model_dump_json())
        return {"message": "Policy updated successfully"}
    except HTTPException as e:
        raise e


@app.delete("/policies/{policy_id}", response_model=MessageResponse, summary="Delete a policy by ID")
def delete_policy(policy_id: str):
    try:
        policy_api.delete_policy(json.dumps(policy_id))
        return {"message": "Policy deleted successfully"}
    except HTTPException as e:
        raise e


@app.get("/policies", response_model=List[PolicyResponse], summary="List all policies")
def list_policies():
    try:
        return [PolicyResponse(**policy) for policy in json.loads(policy_api.list_policies())]
    except HTTPException as e:
        raise e


def start_server():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start_server()
