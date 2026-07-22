#!/usr/bin/env python3
# push_challenges.py
import os
import glob
import yaml
import requests

CTFD_URL = os.environ["CTFD_URL"]
CTFD_TOKEN = os.environ["CTFD_TOKEN"]

headers = {
    "Authorization": f"Token {CTFD_TOKEN}",
    "Content-Type": "application/json",
}

# Find all paths containing a `challenge.yml`
def load_challenges():
    return glob.glob("challenges/*/*/challenge.yml")

def sync_challenge(path):
    # Load `challenge.yml`
    with open(path) as f:
        chal = yaml.safe_load(f)

    # Check if the challenge should be pushed
    if not chal.get("visible", True):
        print(f"Skipping (not visible): {chal['name']}")
        return

    # Extract challenge information from `challenge.yml`
    payload = {
        "name": chal["name"],
        "category": chal["category"],
        "description": chal["description"],
        "value": chal["points"],
        "type": "standard",
        "state": "visible",
    }

    # Get challenges that already exist
    existing = requests.get(
        f"{CTFD_URL}/api/v1/challenges",
        headers=headers,
        params={"name": chal["name"]},
    ).json()["data"]

    if existing:
        chal_id = existing[0]["id"]
        
        # If the challenge already exists, update it instead of adding one
        r = requests.patch(
            f"{CTFD_URL}/api/v1/challenges/{chal_id}",
            headers=headers,
            json=payload,
        )
        print(f"Updated: {chal['name']} ({r.status_code})")
    else:
        # Otherwise just add it
        r = requests.post(
            f"{CTFD_URL}/api/v1/challenges",
            headers=headers,
            json=payload,
        )
        chal_id = r.json()["data"]["id"]
        print(f"Created: {chal['name']} ({r.status_code})")

    sync_flag(chal_id, chal["flag"])
    sync_hints(chal_id, chal.get("hints", []))

def sync_flag(chal_id, flag):
    existing = requests.get(
        f"{CTFD_URL}/api/v1/challenges/{chal_id}/flags",
        headers=headers,
    ).json()["data"]
    
    if not existing:
        requests.post(
            f"{CTFD_URL}/api/v1/flags",
            headers=headers,
            json={"challenge_id": chal_id, "content": flag, "type": "static"},
        )

def sync_hints(chal_id, hints):
    existing = requests.get(
        f"{CTFD_URL}/api/v1/challenges/{chal_id}/hints",
        headers=headers,
    ).json()["data"]
    if existing:
        return
    for hint in hints:
        requests.post(
            f"{CTFD_URL}/api/v1/hints",
            headers=headers,
            json={
                "challenge_id": chal_id,
                "content": hint["text"],
                "cost": hint.get("cost", 0),
            },
        )

if __name__ == "__main__":
    for path in load_challenges():
        sync_challenge(path)