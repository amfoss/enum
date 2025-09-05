import re
import time
from typing import List
from fastapi import FastAPI, HTTPException, UploadFile, File
from langchain_community.document_loaders.parsers import RapidOCRBlobParser
from langchain_community.document_loaders.blob_loaders import Blob
from fastapi.middleware.cors import CORSMiddleware
from models import clubs, members, Club, Member


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to frontend url like: ["http://localhost:3000", "https://your-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def get_member(member_id: str):
    if member_id not in members:
        raise HTTPException(status_code=404, detail="Member not found")
    return members[member_id]


# OCR
@app.post("/scan", response_model=Member)
async def parse_image(file: UploadFile = File(...)):
    try:
        start_time = time.perf_counter()

        image_bytes = await file.read()
        blob = Blob(data=image_bytes)
        parser = RapidOCRBlobParser()

        documents = list(parser.lazy_parse(blob))
        parsed_texts = [doc.page_content for doc in documents]

        # Looks for AM.EN.U4AIE220XX style strings
        pattern = re.compile(r"[A-Z]{2}\.[A-Z]{2}\.[A-Z0-9]{10}")
        extracted = None
        if parsed_texts:
            for text in parsed_texts:
                match = pattern.search(text)
                if match:
                    extracted = match.group(0)
                    break

            elapsed_ms = (time.perf_counter() - start_time) * 1000
            print(f"OCR executed in {elapsed_ms:.2f} ms | extracted={extracted}")

            try:
                member = get_member(extracted)
                return member
            except HTTPException:
                raise HTTPException(status_code=404, detail="Member not found")
        print("couldn't extract text")

        raise HTTPException(status_code=404, detail="ID not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
