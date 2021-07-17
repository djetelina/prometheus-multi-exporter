import aiohttp
from prometheus_client import Gauge

from ..base import Exporter

PLAYER_POINTS = Gauge('trackmania_player_points', 'Number of trophy points', labelnames=['display_name'])
PLAYER_POSITION = Gauge('trackmania_player_position', 'World Ranking', labelnames=['display_name', 'zone'])


class TrackmaniaPlayerExporter(Exporter):
    def __init__(self, player_ids: list):
        self.interval = 15 * 60
        self.player_ids = player_ids

    async def update(self):
        for player in self.player_ids:
            data = await self.get_player_data(player)
            PLAYER_POINTS.labels(display_name=data['displayname']).set(data['trophies']['points'])
            PLAYER_POSITION.labels(
                display_name=data['displayname'],
                zone=data['trophies']['zone']['name']
            ).set(data['trophies']['zonepositions'][0])
            PLAYER_POSITION.labels(
                display_name=data['displayname'],
                zone=data['trophies']['zone']['parent']['name']
            ).set(data['trophies']['zonepositions'][1])
            PLAYER_POSITION.labels(
                display_name=data['displayname'],
                zone=data['trophies']['zone']['parent']['parent']['name']
            ).set(data['trophies']['zonepositions'][2])
            PLAYER_POSITION.labels(
                display_name=data['displayname'],
                zone=data['trophies']['zone']['parent']['parent']['parent']['name']
            ).set(data['trophies']['zonepositions'][3])

    async def get_player_data(self, player_id):
        async with aiohttp.ClientSession() as s:
            async with s.get(f'https://trackmania.io/api/player/{player_id}') as r:
                return await r.json()
