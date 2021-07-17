from typing import List

import aiohttp
from prometheus_client import Gauge

from ..base import Exporter

skill_rank = Gauge('osrs_account_skill_rank', 'Rank of a skill', labelnames=['name', 'mode', 'skill'])
level = Gauge('osrs_account_skill_level', 'Level of a skill', labelnames=['name', 'mode', 'skill'])
xp = Gauge('osrs_account_skill_xp', 'Xp in a skill', labelnames=['name', 'mode', 'skill'])
activity_rank = Gauge('osrs_account_activity_rank', 'Rank of an activity', labelnames=['name', 'mode', 'activity'])
score = Gauge('osrs_account_activity_score', 'Score in an activity', labelnames=['name', 'mode', 'activity'])

mode_translator = {
    'normal': 'hiscore_oldschool',
    'im': 'hiscore_oldschool_ironman',
    'uim': 'hiscore_oldschool_ultimate',
    'hcim': 'hiscore_oldschool_hardcore_ironman',
    'dmm': 'hiscore_oldschool_hardcore_deadman',
    'leagues': 'hiscore_oldschool_seasonal',
    'tournament': 'hiscore_oldschool_tournament'
}


class OldSchoolRuneScapeAccountExporter(Exporter):
    def __init__(self, accounts: List[dict]):
        self.interval = 15
        self.accounts = accounts

    async def update(self):
        for player in self.accounts:
            data = await self.get_stats(player['rsn'])
            next = 'skill'
            for name, value in data.items():
                if next == 'skill':
                    skill_rank.labels(name=player['rsn'], mode=player['mode'], skill=name).set(value[0])
                    level.labels(name=player['rsn'], mode=player['mode'], skill=name).set(value[1])
                    xp.labels(name=player['rsn'], mode=player['mode'], skill=name).set(value[2])
                    if name == 'construction':
                        next = 'activity'
                else:
                    activity_rank.labels(name=player['rsn'], mode=player['mode'], activity=name).set(value[0])
                    score.labels(name=player['rsn'], mode=player['mode'], activity=name).set(value[1])

    async def get_stats(self, player, mode='hiscore_oldschool'):
        async with aiohttp.ClientSession() as s:
            async with s.get(f'https://secure.runescape.com/m={mode_translator[mode]}/index_lite.ws?player={player}') as r:
                data = await r.text()
        stats = data.split(' ')
        return dict(
            overall=stats[0].split(','),
            attack=stats[1].split(','),
            defence=stats[2].split(','),
            strength=stats[3].split(','),
            hitpoints=stats[4].split(','),
            ranged=stats[5].split(','),
            prayer=stats[6].split(','),
            magic=stats[7].split(','),
            cooking=stats[8].split(','),
            woodcutting=stats[9].split(','),
            fletching=stats[10].split(','),
            fishing=stats[11].split(','),
            firemaking=stats[12].split(','),
            crafting=stats[13].split(','),
            smithing=stats[14].split(','),
            mining=stats[15].split(','),
            herblore=stats[16].split(','),
            agility=stats[17].split(','),
            thieving=stats[18].split(','),
            slayer=stats[19].split(','),
            farming=stats[20].split(','),
            runecraft=stats[21].split(','),
            hunter=stats[22].split(','),
            construction=stats[23].split(','),
            league_points=stats[24].split(','),
            bh_hunter=stats[25].split(','),
            bh_rogue=stats[26].split(','),
            clues_all=stats[27].split(','),
            clues_beginner=stats[28].split(','),
            clues_easy=stats[29].split(','),
            clues_medium=stats[30].split(','),
            clues_hard=stats[31].split(','),
            clues_elite=stats[32].split(','),
            clues_master=stats[33].split(','),
            lms=stats[34].split(','),
            soul_wars=stats[35].split(','),
            abyssal_sire=stats[36].split(','),
            alchemical_hydra=stats[37].split(','),
            barrows=stats[38].split(','),
            bryophyta=stats[39].split(','),
            callisto=stats[40].split(','),
            cerberus=stats[41].split(','),
            raids=stats[42].split(','),
            raids_challenge=stats[43].split(','),
            chaos_elemental=stats[44].split(','),
            chaos_fanatic=stats[45].split(','),
            zilyana=stats[46].split(','),
            corp=stats[47].split(','),
            crazy_archeologist=stats[48].split(','),
            dag_prime=stats[49].split(','),
            dag_rex=stats[50].split(','),
            dag_supreme=stats[51].split(','),
            deranged_archeoloogist=stats[52].split(','),
            graardor=stats[53].split(','),
            mole=stats[54].split(','),
            grotesque_guardians=stats[55].split(','),
            hespori=stats[56].split(','),
            kalphite_queen=stats[57].split(','),
            kbd=stats[58].split(','),
            kraken=stats[59].split(','),
            kree=stats[60].split(','),
            kril=stats[61].split(','),
            mimic=stats[62].split(','),
            nightmare=stats[63].split(','),
            phosani_nightmare=stats[64].split(','),
            obor=stats[65].split(','),
            sarachnis=stats[66].split(','),
            scorpia=stats[67].split(','),
            skotizo=stats[68].split(','),
            tempoross=stats[69].split(','),
            gauntlet=stats[70].split(','),
            corrupted_gauntlet=stats[71].split(','),
            tob=stats[72].split(','),
            tob_hard=stats[73].split(','),
            themonuclear_smoke_devil=stats[74].split(','),
            zuk=stats[75].split(','),
            jad=stats[76].split(','),
            venenatis=stats[77].split(','),
            vetion=stats[78].split(','),
            vorkath=stats[79].split(','),
            wintertodot=stats[80].split(','),
            zalcano=stats[81].split(','),
            zulrah=stats[82].split(',')
        )
