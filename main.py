from fastapi import FastAPI, HTTPException
from typing import List
from models import clubs, members, Club, Member

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ACTIVE"}


# CLUB

@app.get("/clubs", response_model=List[str])
def get_clubs():
    return list(clubs.keys())


@app.get("/clubs/{club_name}", response_model=Club)
def get_club(club_name: str):
    if club_name not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")
    return clubs[club_name]


# MEMBER

@app.get("/members/{member_id}", response_model=Member)
def get_member(member_id: str):
    if member_id not in members:
        raise HTTPException(status_code=404, detail="Member not found")
    return members[member_id]
