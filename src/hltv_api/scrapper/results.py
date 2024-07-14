"""
Scraps HLTV results page
- Get latest results from today
- Get latest 100 results (1st page)
- For each result, collect:
    - Winning team
    - Losing team
    - Final score
    - Event name
    - Series info (bo5, bo3, bo1, etc)
    - Match id
    - Link to match
- Implement pagination
"""

from bs4 import BeautifulSoup


def collect_results(html_content: str) -> list[dict]:
    soup = BeautifulSoup(html_content, "html.parser")
    results_div = soup.find("div", class_="results")
    results = []
    for match in results_div.find_all("a", class_="a-reset"):
        match_url = match["href"]

        winner_team_name = match.find("div", class_="team team-won").text.strip()
        scores = match.find("td", class_="result-score")
        score_won = scores.find("span", class_="score-won").text.strip()
        score_lost = scores.find("span", class_="score-lost").text.strip()

        teams = match.find_all("div", class_="team")
        if teams[0].text.strip() == winner_team_name:
            winner_team = {"name": teams[0].text.strip(), "score": score_won}
            loser_team = {"name": teams[1].text.strip(), "score": score_lost}
        else:
            winner_team = {"name": teams[1].text.strip(), "score": score_won}
            loser_team = {"name": teams[0].text.strip(), "score": score_lost}

        event_name = (
            match.find("td", class_="event")
            .find("span", class_="event-name")
            .text.strip()
        )
        map_info = (
            match.find("td", class_="star-cell")
            .find("div", class_="map-text")
            .text.strip()
        )

        result = {
            "url": match_url,
            "teams": [winner_team, loser_team],
            "event_name": event_name,
            "map_info": map_info,
        }

        results.append(result)
    return results
