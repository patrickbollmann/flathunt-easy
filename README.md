## Insall:
- run: ``` pip install -r requirements.txt ``` to install required packages
- install google chrome
- download chromedriver for your chrome version from: https://chromedriver.chromium.org and copy chromedriver to this directory

## usage
 - setup telegram-send with your bot (instructions: https://pypi.org/project/telegram-send/)
 - fill the urls in the script with your search urls
 - run: ``` python flathunt.py ```

The script checks every 10 mins for new flats and sends telegram msg if new flats are found
