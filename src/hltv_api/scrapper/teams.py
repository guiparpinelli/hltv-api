from typing import List, Any, Optional
from bs4 import BeautifulSoup
from pydantic import BaseModel
from main import HLTVClient


class Team(BaseModel):
    name: str
    players: List[str]
    coach: str
    position: str

    @classmethod
    def get_all_teams(cls, client: HLTVClient) -> List[str]:
        results_html = client.fetch_page("stats/teams?minMapCount=0")
        if not results_html:
            return []
        soup = BeautifulSoup(results_html, "html.parser")
        td_elements = soup.find_all('td', class_='teamCol-teams-overview')

        teams = []
        for td in td_elements:
            link = td.find('a', href=True)
            team_url = link['href'].replace("/stats/teams", "team")
            teams.append(team_url)

        return teams

    @classmethod
    def get_teams_by_region(cls, url_suffix: str, limit: Optional[int] = None) -> List[Any]:
        client = HLTVClient()
        recent_url = client.validate_hltv_url(f"ranking/teams{url_suffix}")
        results_html = client.fetch_page(recent_url)
        if not results_html:
            return []
        soup = BeautifulSoup(results_html, "html.parser")
        teams = soup.select('.ranked-team.standard-box')
        if limit:
            teams = teams[:limit]

        result = []
        for team in teams:
            team_name = team.select_one('.teamLine .name').get_text(strip=True)
            team_points = team.select_one('.teamLine .points').get_text(strip=True)
            player_names = [player.get_text(strip=True) for player in team.select('.rankingNicknames span')]
            result.append([team_name, team_points, player_names])

        return result

    @classmethod
    def get_top_5_teams(cls) -> List[Any]:
        return cls.get_teams_by_region("", limit=5)

    @classmethod
    def get_top_30_teams(cls) -> List[Any]:
        return cls.get_teams_by_region("")

    @classmethod
    def get_top_teams_south_america(cls) -> List[Any]:
        return cls.get_teams_by_region("country/South%20America")

    @classmethod
    def get_top_teams_north_america(cls) -> List[Any]:
        return cls.get_teams_by_region("country/North%20America")

    @classmethod
    def get_top_teams_europe(cls) -> List[Any]:
        return cls.get_teams_by_region("country/europe")

    @classmethod
    def get_top_teams_asia(cls) -> List[Any]:
        return cls.get_teams_by_region("country/asia")

    @classmethod
    def get_top_teams_oceania(cls) -> List[Any]:
        return cls.get_teams_by_region("country/oceania")

    @classmethod
    def from_html(cls, soup: BeautifulSoup) -> "Team":
        name = soup.find('h1', class_='profile-team-name text-ellipsis').text.strip()
        players = [span.text for span in soup.find_all('span', class_='text-ellipsis bold')]
        position = None
        coach = None

        for div in soup.find_all('div', class_='profile-team-stat'):
            if div.find('b') and 'World ranking' in div.find('b').text:
                try:
                    position = div.find('a').text
                    if position.startswith('#'):
                        position = position[1:]
                except:
                    position = "-"
            if div.find('b') and 'Coach' in div.find('b').text:
                coach = div.find('a').text
            else:
                coach = "-"

        return Team(name=name, coach=coach, players=players, position=position)
