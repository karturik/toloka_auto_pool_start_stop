import toloka.client as toloka
from datetime import datetime

# YANDEX TOLOKA TOKEN
OAUTH_TOKEN = ''
HEADERS = {"Authorization": "OAuth %s" % OAUTH_TOKEN, "Content-Type": "application/JSON"}
toloka_client = toloka.TolokaClient(OAUTH_TOKEN, 'PRODUCTION')

project_id = ''
pool_id = ''

# CREATE EVERY DAY POOL
print(toloka_client.get_requester())
pools = toloka_client.find_pools(project_id=project_id,limit = 300)
pools_open = list(map(lambda x: x.id, filter(lambda x: x.status.value == 'OPEN', pools.items)))
for i in pools_open:
    r = toloka_client.close_pool(i)
new_pool = toloka_client.clone_pool(pool_id)
print(new_pool.id)
new_pool.private_name = str(datetime.now())[:19]
r = toloka_client.update_pool(pool_id = new_pool.id, pool = new_pool)

tasks = [toloka.task.Task(input_values={'id': str(i)}, pool_id=new_pool.id) for i in range(10)]
created_result = toloka_client.create_tasks(tasks, allow_defaults=True)
print(len(created_result.items))
toloka_client.open_pool(pool_id = new_pool.id)
t = toloka_client.open_pool(pool_id = new_pool.id)
print(str(datetime.now()))