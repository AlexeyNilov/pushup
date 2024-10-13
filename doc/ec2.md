# How to run the bot on AWS EC2 for free

* Why EC2?
* Why sqlite
* How to run your own bot (step-by-step)

## Compute configuration

The bot runs on t3.micro based on AL 2023 AMI

## Preparation

```
dnf install python3.11 git-core
python3.11 -m ensurepip --upgrade
```

## Install code

```
python3.11 -m venv .venv
source .venv/bin/activate
python -V
pip install -r requirements.txt
cp conf/settings.py.sample conf/settings.py
PYTHONPATH=${PYTHONPATH}:. python sample/simply.py
```

## Install services

```
cd /home/ec2-user/pushup/infra
cp *.timer *.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable github_syncer.timer
systemctl enable github_syncer.service
systemctl enable cody_bot.service
systemctl start cody_bot.service
```
