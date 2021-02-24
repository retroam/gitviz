from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/{repo}", response_class=HTMLResponse)
async def get_repo(request: Request, repo: str):
    return templates.TemplateResponse("gitviz.html", {"request": request, "repo":repo})
