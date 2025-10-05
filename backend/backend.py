"""Need to create a FastAPI with two different  methods. The first will be a /summarize whichi will utilize a  summarizer
to condense a news article. The second call will be to find similar news articles. I will calculate the cosine similarity
of the news articles with the given news article and return URL's for the top 5 matches.
 This will first work with text bodies but can be expanded to other URL"s as a future goal of the project"""
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from model import comparator, summarizer
from fastapi.middleware.cors import CORSMiddleware
import os


print("Starting FastAPI")
app = FastAPI()

print("App has been set..")
"""Testing new push"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Creating target dir")
target_dir = ('../data/')
print("Target dir created, creating compare_agent..")

compare_agent = comparator.Article_Comparator()
print("Backend startup complete!!")

print("Current working directory is: " + os.getcwd())

"""temp"""

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