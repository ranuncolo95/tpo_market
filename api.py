from fastapi import FastAPI, Request, Form, HTTPException, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from defs import fetch_stock_data
from typing import Optional

app = FastAPI()

# Add CORS middleware to handle requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/data")
async def get_stock_data(
    ticker: str = Body(...),
    start_date: date = Body(...),
    end_date: date = Body(...)
):
    try:
        df = fetch_stock_data(ticker, start_date, end_date)
        
        return JSONResponse({
            "labels": df['date'].dt.strftime('%Y-%m-%d').tolist(),
            "datasets": [{
                "label": ticker,
                "data": df['close'].tolist(),
                "borderColor": "#4CAF50",
                "backgroundColor": "rgba(0,0,0,0)",
                "tension": 0.1
            }]
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))