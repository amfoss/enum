import json
from pydantic import BaseModel
from typing import List, Dict


class Member(BaseModel):
    id: str
    name: str
    club: str


class Club(BaseModel):
    name: str
    members: List[str]


with open("data.json", "r") as f:
    data = json.load(f)

clubs: Dict[str, Club] = {}
members: Dict[str, Member] = {}

for club_key, club_data in data["clubs"].items():
    member_ids = [m["id"] for m in club_data["members"]]

    clubs[club_key] = Club(
        name=club_data["name"],
        members=member_ids
    )

    for m in club_data["members"]:
        members[m["id"]] = Member(
            id=m["id"],
            name=m["name"],
            club=club_data["name"]
        )
