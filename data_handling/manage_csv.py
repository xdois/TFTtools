import json
import pprint

def make_empty_augment_csv():
    # 순방률, 우승률도 추가했으면 좋았을텐데?

    augment_csv = open('./data/augment_statistics.csv', 'w')
    augment_csv.write('augment name,play count,rank sum,win count,top4 count\n')
    augments_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-augments.json'
    hero_augments_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-hero-augments.json'

    with open(augments_json_path, 'r', encoding='utf-8') as file:
        data_augments = json.load(file)['data']
    with open(hero_augments_json_path, 'r', encoding='utf-8') as file:
        data_hero_augments = json.load(file)['data']
    
    for augment in data_augments:
        print(data_augments[augment]['name'])
        augment_csv.write(data_augments[augment]['name'] + ',0,0,0,0\n')
    
    for augment in data_hero_augments:
        augment_csv.write(data_hero_augments[augment]['name'] + ',0,0,0,0\n')

    augment_csv.close()

def make_empty_champion_csv():
    champion_csv = open('./data/champion_statistics.csv', 'w')
    champion_csv.write('champion_name,play_count,rank_sum,win_count,top4_count,star1_count,star2_count,star3_count\n')
    champion_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-champion.json'

    with open(champion_json_path, 'r', encoding='utf-8') as file:
        data_champion = json.load(file)['data']

    for champion in data_champion:
        champion_csv.write(data_champion[champion]['name'] + ',0,0,0,0,0,0,0\n')

    champion_csv.close()

def make_empty_champion_item_csv():
    champion_item_csv = open('./data/champion_item_statistics.csv', 'w')
    string_champion_name = 'item_name'
    item_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-item.json'
    champion_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-champion.json'

    with open(item_json_path, 'r', encoding='utf-8') as file:
        data_item = json.load(file)['data']
        # 찬란한 아이템같은건 극 소수 케이스니까 따로 안모은다?
        # 아이템+챔피언 평균성적을 구하는건? -> 3차원 데이터를 만든다?
        # 데이터가 커지긴 하겠지만 어떻게든 되겠지 -> 이건 일단 나중에 안정화를 시켜놓고 하자
    
    with open(champion_json_path, 'r', encoding='utf-8') as file:
        data_champion = json.load(file)['data']

    # nan값은 나중에(match_analyze에서) 0으로 채워주자

    for champion in data_champion:
        string_champion_name += ',' + data_champion[champion]['name']
    string_champion_name += '\n'
    champion_item_csv.write(string_champion_name)

    for item in data_item:
        print(data_item[item]['name'])
        champion_item_csv.write(data_item[item]['name'] + '\n')    
    
    champion_item_csv.close()


def make_empty_trait_csv():
    trait_csv = open('./data/trait_statisctics.csv', 'w')
    trait_csv.write('trait_name,tier_current_count_1,tier_current_count_2,tier_current_count_3,tier_current_count_4,play_count,rank_sum,win_count,top4_count\n')
    trait_json_path = './dragontail-13.1.1/13.1.1/data/ko_KR/tft-trait.json'

    with open(trait_json_path, 'r', encoding='utf-8') as file:
        data_trait = json.load(file)['data']

    for trait in data_trait:
        trait_csv.write(data_trait[trait]['name'] + ',0,0,0,0,0,0,0,0\n')

    trait_csv.close()
    


if __name__ == '__main__':
    #make_empty_augment_csv()
    make_empty_champion_csv()
    #make_empty_trait_csv()
    make_empty_champion_item_csv()