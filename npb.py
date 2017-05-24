import os
import sys
import urllib.request
import datetime
from bs4 import BeautifulSoup
from vfd import VFD
from vfdimg import vfdimg
import time

class TeamInfo:
    def __init__(self):
        self.team = ''
        self.score = ''
        self.name = ''

class VsResult:
    def __init__(self):
        self.teams = []
        self.teams.append(TeamInfo())
        self.teams.append(TeamInfo())

args = sys.argv
if len(args) == 2:
    str_day = args[1]
else:
    today = datetime.date.today()
    str_day = "{0:%Y%m%d}".format(today)
print(str_day)

url = 'https://baseball.yahoo.co.jp/npb/schedule/?date=' + str_day
response = urllib.request.urlopen(url)
data = response.read()
decoded_data = data.decode('utf_8')
#decoded_data = open('test.html').read() # for test

soup = BeautifulSoup(decoded_data, 'html.parser')
tables = soup.findAll('table', class_ = 'teams')
results = []
for table in tables:
    result = VsResult()
    scores = table.findAll('td', class_ = 'score_r')
    teams = table.findAll('th', class_ = 'bt bb bl')
    for i in [0 ,1]:
        result.teams[i].score = scores[i].text
        result.teams[i].team = teams[i].find('a')['data-ylk'][9:12]  # slk:icon_XXX;pos:0
        result.teams[i].name = teams[i].find('a')['title']
    results.append(result)
vfd = VFD(17, 27)
vfd.open('/dev/ttyAMA0')
vfd.fontxy(2, 2)

for result in results:
    t1 = result.teams[0]
    t2 = result.teams[1]
    print(t1.name + ' ' + t1.team + ' ' + t1.score
          + ' - ' + t2.score + ' ' + t2.team + ' ' + t2.name)
    dir = os.path.dirname(__file__)
    if dir != '':
        dir = dir + '/'
    dir = dir + 'icon/'
    icon1 = vfdimg(dir + t1.team + '.bmp')
    icon2 = vfdimg(dir + t2.team + '.bmp')
    x = 280
    vfd.cursor(x, 0)
    vfd.drawimg(icon1)
    x += 16 + 4
    vfd.cursor(x, 0)
    s = t1.score + ' - ' + t2.score
    vfd.puts(s)
    x += len(s) * 7 * 2 + 4
    vfd.cursor(x, 0)
    vfd.drawimg(icon2)
    x += 16 + 20
    vfd.cursor(x, 0)
    vfd.scroll(2, 512, 1)
    vfd.clr()
time.sleep(5)
vfd.fontxy(1, 1)
pos = [(0,0), (95,0), (190,0), (0,1), (95, 1), (190,1)]
i = 0
for result in results:
    vfd.cursor(pos[i][0], pos[i][1])
    t1 = result.teams[0]
    t2 = result.teams[1]
    s = t1.team + ' ' + t1.score + '-' + t2.score + ' ' + t2.team
    vfd.puts(s)
    i += 1
vfd.close()
