# KI-Song-Contest am Stand der Piratenpartei an der BEA 2025

**Wichtig**: Wurde nur auf Linux getestet.

## Installation

- Install Python 3.13
- Run `python3.13 -m venv env`
- Run `./env/bin/activate`
- Run `pip install -r requirements.txt`
- Delete line 910 of "./env/lib/python3.13/site-packages/owncloud/owncloud.py" (`'name': data_el.find('name').text`)

To start, run `python main.py`.
