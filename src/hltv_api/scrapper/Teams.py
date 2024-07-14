from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl


class Team(BaseModel):
    team_id: int
    name: str
    players: list
    position: int

    @property
    def name(self) -> str:
        return self.name

    @property
    def players(self) -> list:
        return self.players

    @property
    def hltv_position(self) -> int:
        return self.position

