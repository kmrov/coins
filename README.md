coins
=====
A script that scrapes coin classifieds on some secret Russian website and tries to guess their years of issue.

Setup
-----
Requires Python 3.5 or later. Install dependencies from `requirements.txt` file. For example, with virtualenv, virtualenvwrapper and pip:

```
mkvirtualenv -p `which python3` coins
pip install -r requirements.txt
```

Then copy `config.py-EXAMPLE` to `config.py` and fill out the missing parameters:
* `CATEGORY_URL`: full path to category on desktop version of website.
* `API_URL`, `SECRET`, `KEY`: path to the API and credentials for it.

Usage
-----
To run, just execute
```
python coins.py
```
The script saves all lots to the SQLite3 database defined by `DB` parameter in the config file. By default, it fetches a list of lots, then processes them, getting the description and trying to guess the year of issue. 

With optional `--continue` parameter, it assumes that lots are already fetched, just processing them where needed. 

Finally, it outputs the full number of lots and percentages of lots with nonempty year and lots issued in 2000 or later.
