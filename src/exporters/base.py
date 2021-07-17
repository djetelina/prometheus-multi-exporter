import asyncio
from abc import abstractmethod


class Exporter:
    def __init__(self, interval):
        self.interval = interval

    async def run(self):
        while True:
            await self.update()
            await asyncio.sleep(self.interval)

    @abstractmethod
    async def update(self):
        pass
