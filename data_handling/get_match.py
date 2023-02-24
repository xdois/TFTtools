import pprint
import httplib2
import json
import apikey
import pandas as pd
import numpy as np
import time
from datetime import datetime
import os
import shutil

API_KEY = apikey.API_KEY

MAIN_URL_KR = 'https://kr.api.riotgames.com/tft/league/v1'
h = httplib2.Http()

# 챌린저 명단을 가져와서 필요한 정보(소환사 이름, 소환사id)만 csv 파일에 저장
def get_challenger():
    URL_CHALLENGER = MAIN_URL_KR + '/challenger?api_key=' + apikey.API_KEY
    
    response_challenger, content_challenger = h.request(URL_CHALLENGER, 'GET')
    result_challenger = json.loads(content_challenger.decode('utf-8'))['entries']
    result_challenger = sorted(result_challenger, key=lambda x: x['leaguePoints'], reverse=True)

    challenger_csv = open('./data/challenger.csv', 'w')
    challenger_csv.write('summonerName,summonerId\n')
    for challenger in result_challenger:
        summonerName = challenger['summonerName']
        summonerId = challenger['summonerId']
        challenger_csv.write(summonerName + ',' + summonerId + '\n')
    
    challenger_csv.close()
    return

def get_time_string():
    now = datetime.now()
    return now.strftime('%Y_%m_%d_%H_%M_%S')



def get_ranker(tier='challenger'):
    URL = ''
    if tier == 'challenger':
        URL = MAIN_URL_KR + '/challenger?api_key=' + apikey.API_KEY
    elif tier == 'grandmaster':
        URL = MAIN_URL_KR + '/grandmaster?api_key=' + apikey.API_KEY
    elif tier == 'master':
        URL = MAIN_URL_KR + '/master?api_key=' + apikey.API_KEY
    
    response, content = h.request(URL, 'GET')
    result = json.loads(content.decode('utf-8'))['entries']

    
    file_path = './data/ranker/' + tier + '_' + get_time_string() + '.csv'
    ranker_csv = open(file_path, 'w')
    ranker_csv.write('summonerName,summonerId\n')

    for r in result:
        summonerName = r['summonerName']
        summonerId = r['summonerId']
        ranker_csv.write(summonerName + ',' + summonerId + '\n')
        print(summonerName + ',' + summonerId + '\n')
    ranker_csv.close()
    return



# csv 파일을 읽어와서 이를 통해 puuid를 추가로 가져옴
def get_puuid(csv_file):
    df = pd.read_csv(csv_file, encoding='CP949')
    #print(type(df))
    df['puuid'] = ''
    for idx, row in df.iterrows():
        
        summonerId= row['summonerId']
        #print(row['summonerId'])
        print(idx)
        # api 리밋이 걸릴때 2분간 휴식하는 코드를 추가
        # -> api 리밋이 걸리고 휴식하면 휴식했을때 idx에 해당하는게 스킵된다?
        # 1.3초마다 request를 보낸다
        # 새 파일을 쓰고 거기에 puuid를 저장할 것인가? - 약간 비효율적인듯
        # 기존 dataframe에 puuid 열을 추가하고 거기다가 puuid를 작성
        
        
        URL_SUMMONER = 'https://kr.api.riotgames.com/tft/summoner/v1/summoners/' + summonerId +'?api_key=' + apikey.API_KEY
        
        response, content = h.request(URL_SUMMONER, 'GET')
        result = json.loads(content.decode('utf-8'))
        puuid = result['puuid']
        print(puuid)
        row['puuid'] = puuid
        time.sleep(1.3)

    print(df)
    df.to_csv(csv_file, encoding='utf-8-sig')
    return

# 매치id를 가져오는 함수, 중복처리 필수
# 매치 json 폴더를 만들어놓고, 매치 json 파일을 저장해놓는다
# "game_version": "Version 13.3.491.6222 (Feb 09 2023/14:51:50) [PUBLIC] ",

def get_match(csv_file):
    df = pd.read_csv(csv_file)

    for idx,row in df.iterrows():
        print('index:',idx)
        puuid = row['puuid']
        
        URL_MATCH_LIST = 'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid +'/ids?start=0&count=20&api_key=' + apikey.API_KEY
        response, content = h.request(URL_MATCH_LIST, 'GET')
        result = json.loads(content.decode('utf-8'))
        
        for match in result:
            file_path = './data/match/13.3/' + match + '.json'
            file_path_13_1 = './data/match/13.1/' + match + '.json'
            if os.path.isfile(file_path) == False and os.path.isfile(file_path_13_1) == False:
                URL_MATCH = 'https://asia.api.riotgames.com/tft/match/v1/matches/' + match + '?api_key=' + apikey.API_KEY
                response, content = h.request(URL_MATCH, 'GET')
                result_match = json.loads(content.decode('utf-8'))
                #game_version = result_match['info']['game_version']
                time.sleep(1.3)
                print(match)
                with open(file_path, 'w') as outfile:
                    json.dump(result_match, outfile)
            # 중복 판정을 먼저하고 api를 불러오자
            # 버전 체크를 하지말고 일단 다운부터 다 받고 버전체크는 나중에 하자(버전체크 자체가 어처피 1api호출임)
            
            else:
                print('중복!', match)
            
        time.sleep(1.3)

def check_version():
    folder_path = './data/match/13.3/'
    file_list = os.listdir(folder_path)

    for j in file_list:
        with open(folder_path + j, 'r') as file:
            version = json.load(file)['info']['game_version']

        if '13.1' in version:
            print(j)
            os.remove(folder_path + j)


        

if __name__ == '__main__':

    #get_ranker('challenger')
    #get_ranker('grandmaster')


    get_puuid('./data/ranker/challenger_2023_02_20_13_56_05.csv')
    get_puuid('./data/ranker/grandmaster_2023_02_20_13_56_05.csv')
    get_match('./data/ranker/challenger_2023_02_20_13_56_05.csv')
    get_match('./data/ranker/grandmaster_2023_02_20_13_56_05.csv')
    check_version()
