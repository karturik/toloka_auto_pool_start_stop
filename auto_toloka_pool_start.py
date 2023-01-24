import toloka.client as toloka
from datetime import datetime
import requests
import json

# YANDEX TOLOKA TOKEN
OAUTH_TOKEN = ''
HEADERS = {"Authorization": "OAuth %s" % OAUTH_TOKEN, "Content-Type": "application/JSON"}
toloka_client = toloka.TolokaClient(OAUTH_TOKEN, 'PRODUCTION')

today = str(datetime.now()).split(' ')[0]

pool_id = ''
project_id = ''

# CHECK IF THERE IS TODAY POOL AND TASK COUNT, AUTO POOL START/STOP
balance = requests.get('https://toloka.dev/api/v1/requester', headers=HEADERS).json()
if balance['balance'] > 20.00:
    pools = toloka_client.find_pools(project_id=project_id,limit = 300)
    for pool in pools.items:
        if today in pool.private_name:
            pool_id = pool.id
            break
    if pool_id:
        df_toloka = toloka_client.get_assignments_df(pool_id, status=['ACTIVE'])
        print(len(df_toloka))
        if len(df_toloka) >= 100:
            r = toloka_client.close_pool(pool_id=pool_id)
            print(r)
        elif len(df_toloka) < 80:
            r = toloka_client.open_pool(pool_id=pool_id)
            print(r)
    else:
        print("There is no today's pool")