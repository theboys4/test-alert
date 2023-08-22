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




def telebot(botmsg):
    logger.info(f"movie: {botmsg}")
    tok =os.environ["TOK"]
    chatId=os.environ["CHAT"]
    sendtxt='https://api.telegram.org/bot'+tok+'/sendMessage?chat_id='+chatId +'&parse_mode=MarkdownV2&text=' + botmsg
    res=requests.get(sendtxt)
    logger.info(f"Token value: {res.status_code}")
    return res.json()
    
if __name__ == "__main__":
    
    date=os.environ["DATE"]
    movie_name=os.environ["MOV"]
    cinemas=[os.environ["CINE_1"],os.environ["CINE_2"],os.environ["CINE_3"],os.environ["CINE_4"]]
    theatre=["AERO","varadaraja","venkateswara","vettri"]
    for c in range(len(cinemas)):
        url= os.environ["URL"]+cinemas[c]+'?fromdate='+date
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find_all('div', class_='MovieSessionsListing_movieDetailsDivHeading__5ARu1')
        for i in s:
            if i.text==movie_name:
                logger.info(f"movie: {i.text}")
                if theatre[c]!="AERO":
                    telebot(movie_name+" "+theatre[c])
                    break
