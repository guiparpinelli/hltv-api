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
    client = HLTVClient()

    teams_links = Team.get_all_teams(client)
    print(teams_links)

    i = 0
    for team_link in teams_links:
        if i != 10:
            results_html = client.fetch_page(team_link)
            soup = BeautifulSoup(results_html, "html.parser")
            result = Team.from_html(soup)
            print(result)
            i += 1
        else:
            break
