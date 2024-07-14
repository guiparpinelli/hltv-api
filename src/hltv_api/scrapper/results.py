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
from pydantic import BaseModel, HttpUrl


class Team(BaseModel):
    name: str
    score: int


class Result(BaseModel):
    match_id: int
    match_url: HttpUrl
    teams: list[Team]
    event_name: str
    series_info: str

    @property
    def winner(self) -> Team:
        return max(self.teams, key=lambda team: team.score)

    @property
    def loser(self) -> Team:
        return min(self.teams, key=lambda team: team.score)

    @property
    def final_score(self) -> str:
        return f"{self.winner.name} {self.winner.score}-{self.loser.score} {self.loser.name}"

    def display(self) -> str:
        return f"{self.final_score} / {self.event_name} / {self.series_info}"


with open("results.html", "r") as page:
    soup = BeautifulSoup(page, "html.parser")

results = []

if results_div := soup.find("div", class_="results"):
    for match in results_div.find_all("a", class_="a-reset"):
        match_url = match["href"]
        match_id = int(match_url.split("/")[-2])

        winner_team_name = match.find("div", class_="team team-won").text.strip()
        scores = match.find("td", class_="result-score")
        score_won = int(scores.find("span", class_="score-won").text.strip())
        score_lost = int(scores.find("span", class_="score-lost").text.strip())

        teams = match.find_all("div", class_="team")
        if teams[0].text.strip() == winner_team_name:
            winner_team = Team(name=teams[0].text.strip(), score=score_won)
            loser_team = Team(name=teams[1].text.strip(), score=score_lost)
        else:
            winner_team = Team(name=teams[1].text.strip(), score=score_won)
            loser_team = Team(name=teams[0].text.strip(), score=score_lost)

        event_name = (
            match.find("td", class_="event")
            .find("span", class_="event-name")
            .text.strip()
        )
        series_info = (
            match.find("td", class_="star-cell")
            .find("div", class_="map-text")
            .text.strip()
        )

        result = Result(
            match_id=match_id,
            match_url=match_url,
            teams=[winner_team, loser_team],
            event_name=event_name,
            series_info=series_info,
        )

        results.append(result)

for r in results:
    print(r.display())
