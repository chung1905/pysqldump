# Pysqldump

Parallel mysqldump in Python

## Getting started

This script requires mysqldump.

Copy this `.env` file and change its variables.

```shell
db_host=xxx
db_user=xxx
db_password=xxx
db_name=xxx
max_worker=8
```

```shell
# Install venv (optional)
python -m venv venv
source ./venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Run
export $(cat .env)
python3 pysqldump.py
```
