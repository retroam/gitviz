import requests
import pandas as pd


def get_data(repo: str, auth: tuple, state="all") -> pd.DataFrame:
    """
    Function for downloading issues data from GitHub
    """
    requests.adapters.DEFAULT_RETRIES = 5

    url = "https://api.github.com/repos/{}/issues?state={}".format(repo, state)
    results = []
    r = requests.get(url, auth=auth)
    results.extend(r.json())
    if "link" in r.headers:
        pages = {
            rel[6:-1]: url[url.index("<") + 1 : -1]
            for url, rel in (link.split(";") for link in r.headers["link"].split(","))
        }

        while "last" in pages and "next" in pages:
            pages = {
                rel[6:-1]: url[url.index("<") + 1 : -1]
                for url, rel in (
                    link.split(";") for link in r.headers["link"].split(",")
                )
            }
            r = requests.get(pages["next"], auth=auth)
            results.extend(r.json())
            if pages["next"] == pages["last"]:
                break
    output = pd.DataFrame(results)
    output = output.merge(
        pd.json_normalize(output.user)[["login", "type"]],
        left_index=True,
        right_index=True,
    )
    return output


def get_group(data: pd.DataFrame, field: str, limit=None, sort=False) -> tuple:
    data["month"] = pd.to_datetime(data.created_at).dt.strftime("%Y-%m")
    grp = data.groupby(field).id.count()
    if sort:
        grp = grp.sort_values(ascending=False)
    if limit:
        grp = grp.head(limit)

    return list(grp.values), list(grp.index)


def get_dashboard_stats(df: pd.DataFrame) -> tuple:
    count_stats = df.state.value_counts().to_dict()
    count_stats_norm = round(100 * df.state.value_counts(normalize=True)).to_dict()

    return (
        count_stats["open"],
        count_stats["closed"],
        int(count_stats_norm["closed"]),
        df.login.nunique(),
    )
