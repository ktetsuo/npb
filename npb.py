import sys
import urllib.request
import datetime
from bs4 import BeautifulSoup

class TeamInfo:
    def __init(self):
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
for result in results:
    print(result.teams[0].name + ' ' + result.teams[0].score
          + ' - ' + result.teams[1].score + ' ' + result.teams[1].name)
