import json
from collections import defaultdict
from typing import Dict, Set

from fastapi import HTTPException

from .models import PolicyModel, PolicyType


class PolicyAPI:
    def __init__(self) -> None:
        self._policies: Dict[str, PolicyModel] = {}
        self._taken_policies_names: Dict[PolicyType, Set[str]] = defaultdict(set)
        self._unique_policies: Set[PolicyType] = {PolicyType.ARUPA}

    def _get_policy(self, policy_id: str) -> PolicyModel:
        policy = self._policies.get(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        return policy

    def _parse_json(self, json_input: str):
        try:
            return json.loads(json_input)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON input")

    def _check_unique_name(self, name: str, policy_type: PolicyType):
        if name in self._taken_policies_names[policy_type]:
            raise HTTPException(status_code=400, detail=f"{policy_type.value} policy names must be unique")

    def _reserve_name(self, name: str, policy_type: PolicyType):
        if policy_type in self._unique_policies:
            self._check_unique_name(name, policy_type)
            self._taken_policies_names[policy_type].add(name)

    def _release_name(self, name: str, policy_type: PolicyType):
        if policy_type in self._unique_policies:
            self._taken_policies_names[policy_type].discard(name)

    def create_policy(self, json_input: str) -> str:
        policy_dict = self._parse_json(json_input)
        policy = PolicyModel(**policy_dict)
        self._reserve_name(policy.name, policy.type)
        policy_id = str(hash(json_input))
        self._policies[policy_id] = policy
        return json.dumps(policy_id)

    def read_policy(self, json_identifier: str) -> str:
        policy_id = self._parse_json(json_identifier)
        policy = self._get_policy(policy_id)
        return json.dumps({
            "policy_id": policy_id,
            "name": policy.name,
            "description": policy.description,
            "type": policy.type.value
        })

    def update_policy(self, json_identifier: str, json_input: str) -> None:
        policy_id = self._parse_json(json_identifier)
        existing_policy = self._get_policy(policy_id)
        update_dict = self._parse_json(json_input)

        if existing_policy.type != update_dict.get('type', existing_policy.type):
            raise HTTPException(status_code=400, detail="Cannot change policy type")

        new_name = update_dict.get('name', existing_policy.name)
        if new_name != existing_policy.name:
            self._reserve_name(new_name, existing_policy.type)
            self._release_name(existing_policy.name, existing_policy.type)

        updated_policy = PolicyModel(
            name=new_name,
            description=update_dict.get('description', existing_policy.description),
            type=existing_policy.type
        )
        self._policies[policy_id] = updated_policy

    def delete_policy(self, json_identifier: str) -> None:
        policy_id = self._parse_json(json_identifier)
        policy = self._policies.pop(policy_id, None)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        self._release_name(policy.name, policy.type)

    def list_policies(self) -> str:
        return json.dumps([
            {
                "policy_id": policy_id,
                "name": policy.name,
                "description": policy.description,
                "type": policy.type.value
            } for policy_id, policy in self._policies.items()
        ])
