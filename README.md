# Pysqldump

Parallel mysqldump in Python

## Getting started

Can phai co mysqldump tren may
Viet file `.env` theo mau~
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
