import requests
import math
import time

DEFENSE_LIMIT = 652
MR_MAX = 41
START_PAGE = 1
PAGES = 20

MY_TEAM = {"BP": 663, "MP": 243}


def get_mr_pct(defense_team, attack_team):
    mp_modifier = 1.25 * (defense_team["MP"] / 3 - 56)
    bp_closeness = 20 / math.sqrt(attack_team["BP"] - defense_team["BP"])
    return 7 + mp_modifier + bp_closeness


count = 0
for page in range(START_PAGE, START_PAGE + PAGES):
    response = requests.get(f'http://idle-game-api.crabada.com/public/idle/mines?page={page}&status=open&limit=100')
    loots_json = response.json()
    games = loots_json['result']['data']
    good_loots = []
    for game in games:
        if len(game['process']) > 1:
            continue
        count += 1
        defense_points = game['defense_point']
        if game['faction'] in ['ORE', 'FAERIE']:
            defense_points *= 0.93
        elif game['faction'] == 'NO_FACTION':
            defense_points *= 0.97
        elif game['faction'] in ['TRENCH', 'MACHINE']:
            defense_points /= 0.93
        if defense_points < DEFENSE_LIMIT:
            revenge_pct = get_mr_pct({"BP": defense_points, "MP": game['defense_mine_point']}, MY_TEAM)
            if revenge_pct < MR_MAX:
                page = math.ceil(count / 8)
                good_loots.append([game['game_id'], page, round(revenge_pct, 1), game['faction'], game['defense_point']])

    best = sorted(good_loots, key=lambda g: g[0], reverse=True)
    for game in best:
        print(game)

    if page >= loots_json['result']['totalPages']:
        break

print('END\n\n')
