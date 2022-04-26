#!/usr/bin/env python3

import MySQLdb
import os
import asyncio

# Database credentials
host = os.getenv('db_host')
user = os.getenv('db_user')
password = os.getenv('db_password')
dbname = os.getenv('db_name')

# Parameters
is_gzip = os.getenv('gzip', default=True)
max_worker = os.getenv('max_worker', default=8)
table_dump_query_params = "--single-transaction --quick --max_allowed_packet=512M"
table_dump_query = f"mysqldump {table_dump_query_params} -p{password} -u{user} -h{host} {dbname} {{table}}"
output_dir = os.getenv('output_dir', default=f'output/{dbname}')

if is_gzip:
    table_dump_query += f" | gzip -9 > {output_dir}/{{table}}.sql.gz"
else:
    table_dump_query += f" > {output_dir}/{{table}}.sql"

os.makedirs(f'{output_dir}', exist_ok=True)


def get_tables(db_host: str, db_user: str, passwd: str, db_name: str):
    connection: MySQLdb.connections.Connection = MySQLdb.connect(host=db_host, user=db_user,
                                                                 passwd=passwd)  # create the connection

    cursor: MySQLdb.cursors.Cursor = connection.cursor()  # get the cursor

    cursor.execute(f"USE {db_name}")  # select the database
    cursor.execute("SHOW TABLES")  # execute 'SHOW TABLES' (but data is not returned)

    tables_tuples = cursor.fetchall()  # return data from last query

    cursor.close()

    table: str
    table_list = list()

    for (table,) in tables_tuples:
        table_list.append(table)

    return table_list


async def worker(name: str, queue: asyncio.Queue):
    while True:
        # Get a "work item" out of the queue.
        t = await queue.get()
        cmd_str = table_dump_query.format(table=t)
        # Sleep for the "sleep_for" seconds.
        proc = await asyncio.create_subprocess_shell(cmd_str, stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE)
        await proc.communicate()

        # Notify the queue that the "work item" has been processed.
        queue.task_done()
        print(f'{name} finished table {t}.')


async def run(tables: list, max_worker: int):
    queue = asyncio.Queue()
    for table in tables:
        queue.put_nowait(table)

    tasks = []
    for i in range(max_worker):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    await queue.join()

    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


tables = get_tables(host, user, password, dbname)
asyncio.run(run(tables, int(max_worker)))
