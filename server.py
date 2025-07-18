from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from main import grade_essay

app = FastAPI()

class EssayRequest(BaseModel):
    topic: Optional[str]
    essay: str

class EssayResponse(BaseModel):
    topic: str
    essay: str
    relevance_score: Optional[float]
    grammar_score: Optional[float]
    structure_score: Optional[float]
    depth_score: Optional[float]
    final_score: Optional[float]
    
@app.post("/grade_essay", response_model=EssayResponse)
async def grade_essay_endpoint(essay_request: EssayRequest):
    try:
        result = grade_essay(essay_request.topic, essay_request.essay)
        return EssayResponse(
            topic=essay_request.topic,
            essay=essay_request.essay,
            relevance_score=result["relevance_score"],
            grammar_score=result["grammar_score"],
            structure_score=result["structure_score"],
            depth_score=result["depth_score"],
            final_score=result["final_score"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))