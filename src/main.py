import asyncio

from prometheus_client import start_http_server

from exporters.osrs.account import OldSchoolRuneScapeAccountExporter
from exporters.trackmania2020.player import TrackmaniaPlayerExporter


async def main():
    start_http_server(5005)
    exporters = [
        # TODO config
        TrackmaniaPlayerExporter(['a3dff1a1-8c43-4867-b982-58fde4cc6cc3']),
        OldSchoolRuneScapeAccountExporter([{
            'rsn': 'DJetelina',
            'mode': 'normal'
        }])
    ]
    tasks = []
    for exporter in exporters:
        tasks.append(asyncio.create_task(exporter.run()))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
