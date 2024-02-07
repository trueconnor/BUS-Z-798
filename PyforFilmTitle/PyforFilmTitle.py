import pandas as pd
from pandas import DataFrame
import requests
import time
import Levenshtein

api_key = ""  # 替换为您的 API 密钥


def import_data():
    data = pd.read_csv('tmdb_5000_movies.csv')
    # select data with original_language = 'en'
    data_en = data[data['original_language'] == 'en'].sort_values('vote_count', ascending=False)
    data_en = data_en[['id', 'original_title']]
    data_en = data_en.reset_index(drop=True).iloc[:1000]
    return data_en


def get_gpt_response(text, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {api_key}"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text}],
        "temperature": 0.1
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        show_message("OpenAI Access Failed! Please check your Internet or API")
        return "Error: " + response.text


def getFilmChineseTitle(original_title):
    response = get_gpt_response("Return the officially translated Chinese name of this English film: '"+original_title+
                                "'.\n If such name exists, just return this Chinese name ALONE and DON'T say ANY OTHER word!"+
                                "\n If you're not sure or the film doesn't have an official Chinese name, return 'NotSure' ALONE.",
                                api_key)
    return response.strip()


def getBackTranslationTitle(chinese_title):
    response = get_gpt_response("I am currently working on a Back Translation task involving the Chinese title of an English movie."+
                                "My goal is to translate the Chinese title back into English using a direct or literal translation approach."+
                                "You should translate the Chinese title of an English movie into English using a literal translation method."+
                                "Just return your translation result and don't say anything else."+
                                "\n This is the Chinese title: '"+
                                chinese_title+"'.",
                                api_key)
    return response.strip()

def getFilmChineseOverview(original_title):
    return data[data['id'] == film_id]['overview'].values[0]


def getChineseTitleFor1000Films(part=0):
    data = import_data()
    # 将data分成10份，每份100部电影
    list_data = [data.iloc[i*100:(i+1)*100] for i in range(10)]
    data = list_data[part].reset_index(drop=True)
    for j in range(100):
        film_id = data.iloc[j]['id']
        original_title = data.iloc[j]['original_title']
        chinese_title = getFilmChineseTitle(original_title)
        data.at[j, 'chinese_title'] = chinese_title
        time.sleep(3)
        print( part*100+j + 1, ' films have been processed.')
    data.to_csv('tmdb_1000_movies_ChineseTitle' + '_' + str(part) + '.csv', index=False)

# 将0-9个文件合并成一个文件
# data = DataFrame()
# for i in range(0, 10):
#     # getChineseTitleFor1000Films(i)
#     data = pd.concat([data, pd.read_csv('tmdb_1000_movies_ChineseTitle' + '_' + str(i) + '.csv')], ignore_index=True)
# data = data.sort_values('chinese_title', ascending=True)
# data.to_excel('tmdb_1000_movies_ChineseTitle.xlsx', index=False)

def getBackTranslationForFilms():
    data = pd.read_excel('01_tmdb_1000_movies_ChineseTitle_QingSelected.xlsx')
    # 针对每一部电影，获取其中文标题的直译
    try:
        for i in range(len(data)):
            chinese_title = data.iloc[i]['chinese_title']
            back_translation = getBackTranslationTitle(chinese_title)
            data.at[i, 'back_translation'] = back_translation
            time.sleep(3)
            print(i + 1, ' films have been processed.')
    except:
        print('Error occurs when processing film ', i)
    data.to_excel('02_tmdb_1000_movies_BackTranslation.xlsx', index=False)


def final_sample():
    data = pd.read_excel('02_tmdb_1000_movies_BackTranslation_QingCleaned.xlsx')
    data_vote = pd.read_csv('tmdb_5000_movies.csv').loc[:, ['id', 'vote_count']]
    # for each film in data, calculate the similarity between the original title and the back translation title
    data['similarity'] = 0
    for i in range(len(data)):
        original_title = data.iloc[i]['original_title']
        back_translation = data.iloc[i]['back_translation']
        similarity = Levenshtein.ratio(original_title, back_translation)
        data.at[i, 'similarity'] = similarity
    data = data.sort_values('similarity', ascending=True).reset_index(drop=True)
    # select similar < 0.5
    data = data[data['similarity'] < 0.5]
    # merge the vote_count into the data
    data = pd.merge(data, data_vote, on='id', how='left').sort_values('vote_count', ascending=False).reset_index(drop=True)
    # select the top 50
    data = data.iloc[:50]
    #data = data.iloc[51:100]
    #data.to_excel('04_PracticeSample.xlsx', index=False)
