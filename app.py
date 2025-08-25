import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from tavily import TavilyClient  # Import the Tavily client

# Retrieve secret key from environment variable
TAVILY_API_SECRET_KEY = os.environ.get("TAVILY_API_SECRET_KEY", "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")
app = FastAPI(title="Tavily API Search Service")

class SearchRequest(BaseModel):
    company: str
    partners: Optional[List[str]] = None

@app.post("/search")
def search_company(data: SearchRequest):
    """
    Searches Tavily API with the provided company and company partners using the Tavily client.
    The TavilyClient.search method requires a 'query' argument.
    """
    client = TavilyClient(api_key=TAVILY_API_SECRET_KEY)
    try:
        # Pass 'query' argument with the company name; include partners as optional argument.
        result = client.search(query=data.company, partners=data.partners or [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tavily API call failed: {str(e)}")
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)