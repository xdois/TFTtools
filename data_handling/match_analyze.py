import json
import pprint
import pandas as pd

json_path = './example.json'

def open_json():
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def is_ranked(json):
    if json['info']['queue_id'] == 1100:
        return True
    else:
        return False

def json_info(json):
    return json['info']

def json_participants(json):
    return json['info']['participants']

def winners_data(json):
    participants = json_participants(json)
    # 플레이어 순회
    winner = ''
    for participant in participants:
        # 1등 리턴
        if participant['placement'] == 1:
            #pprint.pprint(participant)
            winner = participant
    return winner

def top4_data(json):
    participants = json_participants(json)
    top4 = []

    for participant in participants:
        if participant['placement'] <= 4:
            top4.append(participant)
    return top4

def all_participants_data(json):
    participants = json_participants(json)

    top8 = []
    for participant in participants:
        top8.append(participant)
    return top8

# winner, top4, top8 데이터 추출 함수 하나로 통일하기

def get_augments(participant):
    # 증강체 반환(한글 이름으로)
    # 등수도 같이 기록해야한다?
    augments_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-augments.json'
    hero_augments_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-hero-augments.json'
    augments = participant['augments']
    augments_kr = []
    with open(augments_json_path, 'r', encoding='utf-8') as file:
        data_augments = json.load(file)['data']
    with open(hero_augments_json_path, 'r', encoding='utf-8') as file:
        data_hero_augments = json.load(file)['data']

    for augment in augments:
        if data_augments.get(augment):
            #print(data_augments[augment]['name'])
            augments_kr.append(data_augments[augment]['name'])
        else:
            #print(data_hero_augments[augment]['name'])
            augments_kr.append(data_hero_augments[augment]['name'])
        # 영증일 경우와 일반 증강체일 경우 구분해야함
        # data_augments에 있을경우와 없을경우 구분 -> if get 활용
    return augments_kr, participant['placement']

def get_champion(participant):
    champion_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-champion.json'
    champions = participant['units']
    item_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-item.json'
    
    # [(챔피언, [아이템1, 아이템2, 아이템3]),...] 이런식으로 한다?

    with open(champion_json_path, 'r', encoding='utf-8') as file:
        data_champion = json.load(file)['data']

    with open(item_json_path, 'r', encoding='utf-8') as file:
        data_item = json.load(file)['data']
    champ_list = []
    for champion in champions:
        champ_id = champion['character_id']
        champion_name = data_champion[champ_id]['name']
        item_id_list = champion['itemNames']
        item_list = []

            # Set5_RadiantItems/ 찬란한 아이템
            # TFT7_ShimmerscaleItems/ 빛비늘 아이템
            # TFT8_EmblemItems/ 시즌8 
            # TFT8_GenAEItems/ 기계유망주 아이템
            #----- 여기부터는 의미 없을듯
            # TFT8_ArsenalItems/ 아펠 무기
            # DoubleUp_AssistItems
            # TFT8_TheUndergroundItems
            # TFT8_Admin
        
        for item_id in item_id_list:
            if data_item.get(item_id):
                item_list.append(data_item[item_id]['name'])
            elif data_item.get('TFT8_EmblemItems/' + item_id):
                item_list.append(data_item['TFT8_EmblemItems/' + item_id]['name'])
            elif data_item.get('TFT8_GenAEItems/' + item_id):
                item_list.append(data_item['TFT8_GenAEItems/' + item_id]['name'])
            elif data_item.get('Set5_RadiantItems/' + item_id):
                item_list.append(data_item['Set5_RadiantItems/' + item_id]['name'])
            else:
                print('------------------살려주세요---------------------')

        champ_list.append((champion_name, item_list))
        
    return champ_list, participant['placement']


def get_trait(participant):
    trait_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-trait.json'
    traits = participant['traits']
    traits_list = []

    with open(trait_json_path, 'r', encoding='utf-8') as file:
        data_traits = json.load(file)['data']

    for trait in traits:
        if trait['tier_current'] > 0:
            #print(data_traits[trait['name']]['name'])
            #print(trait['num_units'])
            traits_list.append((data_traits[trait['name']]['name'], trait['num_units'], trait['tier_current']))

    # num_units말고 tier_current를 저장할까?
    # 아니면 맘 편하게 둘다?
    return traits_list, participant['placement']


def make_empty_augment_csv():
    # 순방률, 우승률도 추가했으면 좋았을텐데?
    # -- manage_csv.py에 넣엇음

    augment_csv = open('./data/augment_statistics.csv', 'w')
    augment_csv.write('augment name,play count,average rank\n')
    augments_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-augments.json'
    hero_augments_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-hero-augments.json'

    with open(augments_json_path, 'r', encoding='utf-8') as file:
        data_augments = json.load(file)['data']
    with open(hero_augments_json_path, 'r', encoding='utf-8') as file:
        data_hero_augments = json.load(file)['data']
    
    for augment in data_augments:
        print(data_augments[augment]['name'])
        augment_csv.write(data_augments[augment]['name'] + ',0,0\n')
    
    for augment in data_hero_augments:
        augment_csv.write(data_hero_augments[augment]['name'] + ',0,0\n')

    augment_csv.close()

def add_data_augment(augment_return, dataframe):
    # augment : tuple([증강체 3개 리스트], 등수)
    augments = augment_return[0]
    placement = augment_return[1]

    # dataframe 구조 augment name,play count,rank sum(avg*play count),win count, top4 count
    # 증강체 이름에대해 play count + 1, rank sum + placement
    # if placement == 1: win count + 1, if placement <= 4: top4 count + 1
    
    #print(dataframe)
    for augment in augments:
        dataframe.loc[augment, 'play count'] += 1
        dataframe.loc[augment, 'rank sum'] += placement
        if placement == 1:
            dataframe.loc[augment, 'win count'] += 1
        if placement <= 4:
            dataframe.loc[augment, 'top4 count'] += 1
        print(dataframe.loc[augment])
    print(placement)
    return dataframe

def add_data_trait(trait_return, dataframe):
    # trait_detail에 대해
    # 데이터 갱신하면서 해야될거같음
    # -> csv 파일에 x축에 tier_total or num_units 관련 값을 추가
    # tier_total 값을 넣는게 데이터 공간에 효율적인듯
    # 위협의 경우만 num_units을 기록한다 -> 애매한데?
    # [(시너지명, num_units, tier_current), placement]
    # tier_current_(현재tier_current값) + 1
    # play_count + 1
    # rank_sum + placement
    # if placement == 1: win count + 1, if placement <= 4: top4 count + 1
    trait_list = trait_return[0]
    placement = trait_return[1]
    for trait in trait_list:
        #print(trait)
        trait_name = trait[0]
        tier_current = trait[2]
        dataframe.loc[trait_name, 'play_count'] += 1
        dataframe.loc[trait_name, 'tier_current_count_' + str(tier_current)] += 1
        dataframe.loc[trait_name, 'rank_sum'] += placement
        if placement == 1:
            dataframe.loc[trait_name, 'win_count'] += 1
        if placement <= 4:
            dataframe.loc[trait_name, 'top4_count'] += 1
        print(dataframe.loc[trait_name])
    
    return dataframe

def add_data_champion(champion_return, dataframe):
    # 챔피언 3성작 비율 등을 알아보기위해 csv파일에 몇성인지를 저장하자
    # 챔피언이 착용한 아이템에 대한 통계도 필요하다 -> 이건 csv 파일을 분리하자

    # 
    pass

    

def analyze_participants(participant):
    # participant 객체를 받아서 분석
    # 이후 csv 파일에 데이터에 현재 데이터를 추가해준다
    # 파일 경로들이 필요하고
    # 매 json마다 csv를 로드하고 -> 데이터프레임으로 바꾸고 -> 결과를 반영하고 -> 데이터 프레임을 다시 csv로 변환하는것은 너무 비효율적
    # 매치 분석을 요청하는 파일에서 이미 데이터프레임 상태로 갖고있게 하고 그걸 이용하면 될듯
    # 데이터 프레임을 파라미터로 받는다? -> 복잡해지니까 함수를 나누자
    pass

# 아이템 시너지 챔피언 증강체 등을 클래스를 만들어서 관리?
# 이를 통합한 participant 클래스를 만듦
# 클래스에는 각 요소의 이름, json에서의 코드명, 이미지 경로 등을 속성으로 갖고있음
# 클래스 혹은 json 파일을 만들어도 괜찮을듯
# -> 이미 json파일이 있다
# dragontail-13.1.1/13.1.1/data/ko_KR
# json 파일 경로들 다 따놓고
# 

# 1,2,3,4등 시너지, 챔피언(아이템), 증강체 정보를 가져온다
# dragontail-13.1.1/13.1.1/img -> tft 이미지 경로
# 1. 일단 해당하는 것을 json 그대로 출력하기
# 정리해서 알아보기 쉽게 문자로 or 이미지로? 띄우기
# -> 키워드를 추출할수 있는 기능?
# 데이터 통계를 csv파일로 저장
# 필요한 데이터 통계
# 1. 1등할때 많이 사용한 챔피언/시너지(통으로 묶어서 / 2,4,6.. 등등 따로)/ 증강체
# 2. 순방할때 많이 사용한 ~~~~
# 3. 챔피언별 많이 사용한 아이템
# 4. 챔피언별 아이템이 들어갔을 때 평균성적, 챔피언별 아이템이 들어간 빈도?
# 5. 증강체별 성적
# 6. 1,2를 기반으로 한 덱 아키타입? 추정 (캐리챔피언, 주요 챔피언, 밸류업용 챔피언 등 구분)
# 7. 덱 별 증강체 추천
# 8. 3성작 비율

# 뭔가를 반환할때 등수를 같이 반환해야함 -> 자료형은 어떻게?
# tuple로 반환하는게 가장 무난할거같다 -> (augment 배열, 등수) 이런식으로

if __name__ == '__main__':
    j = open_json()
    winner = all_participants_data(j)
    augment_csv = './data/augment_statistics.csv'
    trait_csv = './data/trait_statisctics.csv'
    dataframe_augment = pd.read_csv(augment_csv, encoding='CP949')
    trait_dataframe = pd.read_csv(trait_csv, encoding='CP949')
    dataframe_augment.set_index('augment name', inplace = True)
    trait_dataframe.set_index('trait_name', inplace=True)
    #print(trait_dataframe)
    for p in winner:
        #print(get_augments(p))
        #add_data_augment(get_augments(p), dataframe_augment)
        print(get_champion(p))
        #print(get_trait(p))
        #add_data_trait(get_trait(p), trait_dataframe)

    
    #print(dataframe_augment.loc['신병'])
    

    