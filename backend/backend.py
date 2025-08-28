"""Need to create a FastAPI with two different  methods. The first will be a /summarize whichi will utilize a  summarizer
to condense a news article. The second call will be to find similar news articles. I will calculate the cosine similarity
of the news articles with the given news article and return URL's for the top 5 matches.
 This will first work with text bodies but can be expanded to other URL"s as a future goal of the project"""
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from model import comparator, summarizer
from data import scraper
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
"""Testing new push"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
target_dir = ('../data/')
compare_agent = comparator.Article_Comparator()



class Compare_Request(BaseModel):
    text: str

class Compare_Result(BaseModel):
    title: str
    url: str
    text:str
    score: float

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.post("/compare", response_model = list[Compare_Result])
async def compare(request: Compare_Request):
    text = request.text
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    res = compare_agent.top_k(text)
    print(res)
    return res