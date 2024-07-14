from bs4 import BeautifulSoup
from pydantic import BaseModel
from main import HLTVClient


class Team(BaseModel):
    name: str
    players: list[str]
    coach: str
    position: str

    @classmethod
    def get_all_teams(cls, client: HLTVClient) -> list[str]:
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
    def get_top_5_teams(cls) -> list[str]:
        client = HLTVClient
        recent_url = client.validate_hltv_url("ranking/teams")
        results_html = client.fetch_page(recent_url)
        if not results_html:
            return []
        soup = BeautifulSoup(results_html, "html.parser")
        teams = soup.select('.ranked-team.standard-box')[:5]

        result = []
        for team in teams:
            team_name = team.select_one('.teamLine .name').get_text(strip=True)
            team_points = team.select_one('.teamLine .points').get_text(strip=True)
            player_names = [player.get_text(strip=True) for player in team.select('.rankingNicknames span')]
            result.append([team_name, team_points, player_names])

        return result

    @classmethod
    def get_top_30_teams(cls) -> list[str]:
        client = HLTVClient
        recent_url = client.validate_hltv_url("ranking/teams")
        results_html = client.fetch_page(recent_url)
        if not results_html:
            return []
        soup = BeautifulSoup(results_html, "html.parser")
        teams = soup.select('.ranked-team.standard-box')

        result = []
        for team in teams:
            team_name = team.select_one('.teamLine .name').get_text(strip=True)
            team_points = team.select_one('.teamLine .points').get_text(strip=True)
            player_names = [player.get_text(strip=True) for player in team.select('.rankingNicknames span')]
            result.append([team_name, team_points, player_names])

        return result

    @classmethod
    def from_html(cls, soup: BeautifulSoup) -> "Team":
        """
        Parses a BeautifulSoup object to extract team information.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the team's HTML.

        Returns:
            Team: A Team object with the extracted information.
        """
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


if __name__ == "__main__":
    print(Team.get_top_30_teams())
