import asyncio
import datetime
import time
import curses
import requests
import json
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout

from server import ServerComm
from Graphic import Graphic

graphic=Graphic()
servercomm=ServerComm()

posts=[""]
graphic.stdscr.keypad(True)

for i in range(100):
    posts.insert(0,"")

def post_mode(count):
    data={
        'WindSpeed':count,
        'Time':datetime.datetime.now(),
        'LHWD':True,
        'LD':True,
        'AID':1
    }
    posts.insert(0,servercomm.post_data(body=data)+" RECEVE AT:"+datetime.datetime.now().strftime("%H:%M:%S")) 

    height,width = graphic.stdscr.getmaxyx()
    for i in range(height-7):
        graphic.stdscr.addstr(i,0,posts[height-7-i][:30])

def get_mode(count):
    graphic.stdscr.addstr(1,40,"GET DATA")
    getdata=json.loads(servercomm.get_data(query_set='?LD=True'))[0]
    graphic.stdscr.addstr(3,40,str(getdata.get('WindSpeed',0.0))+"m/s",curses.color_pair(1))

def get_status():
    graphic.stdscr.addstr(6,40,'ANEMOMETER STATUS')
    graphic.stdscr.addstr(8,40,'ID:1  WORKING',curses.color_pair(2))

async def task(count):
    await asyncio.gather(
    post_mode(count),
    get_mode(count),
    get_status(),
    )

def main():
    count=int(0)
    try:
        while True:
            graphic.stdscr.clear()
            #asyncio.run(task(count=count))
            post_mode(count)
            get_mode(count)
            get_status()
            graphic.refresh()
            time.sleep(1)
            count+=1
    
    except KeyboardInterrupt:
        curses.endwin()

if __name__ == "__main__":
    main()

"""
表示する項目
瞬間風速
瞬間風向
更新時刻

3分間平均風速推移
3分間平均風向推移

過去

オプション　p pg g


"""