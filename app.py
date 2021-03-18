from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from utils import get_data, get_dashboard_stats, get_group
import configparser


app = FastAPI()

templates = Jinja2Templates(directory="templates")

config = configparser.ConfigParser()
config.read(".config")
access_token = config.get("GITHUB", "token")
username = config.get("GITHUB", "username")
auth = (username, access_token)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.get("/analysis/", response_class=HTMLResponse)
async def get_repo(request: Request, repo: str):
    data = get_data(repo, auth)
    (
        dsh_open_issues,
        dsh_closed_issues,
        dsh_closed_rate,
        dsh_contrib,
    ) = get_dashboard_stats(data)
    contrib_data, contrib_labels = get_group(data,'login', limit=3, sort=True)
    issues_data, issues_labels = get_group(data,'month')
    outcome = {
            "request": request,
            "repo": repo,
            "dsh_closed_issues": dsh_closed_issues,
            "dsh_open_issues": dsh_open_issues,
            "dsh_closed_rate": dsh_closed_rate,
            "dsh_contrib": dsh_contrib,
            "contrib_data":contrib_data,
            "contrib_labels": contrib_labels,
            "issues_data": issues_data,
            "issues_labels": issues_labels
        }
    return templates.TemplateResponse(
        "gitviz.html",
        outcome,
    )
