import logging
import logging.handlers
import os

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise

def telebot(botmsg):
    tok =os.environ["TOK"]
    chatId=os.environ["CHAT"]
    sendtxt='https://api.telegram.org/bot'+tok+'/sendMessage?chat_id='+chatId +'&parse_mode=MarkdownV2&text=' + botmsg
    res=requests.get(sendtxt)
    return res.json()
    
if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")
    date=os.environ["DATE"]
    movie_name=os.environ["MOV"]
    cinemas=[os.environ["CINE_1"],os.environ["CINE_2"],os.environ["CINE_3"],os.environ["CINE_4"]]
    for cini in cinemas:
        url= os.environ["URL"]+cini+'?fromdate='+date
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find_all('div', class_='MovieSessionsListing_movieDetailsDivHeading__5ARu1')
        for i in s:
            if i.text==movie_name:
                logger.info(f"movie: {i.text}")
                telebot(movie_name+" --> "+cini)
                break
