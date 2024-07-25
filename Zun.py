
from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
import json
import os

app = Flask(__name__)

DATA_FILE = 'categories.txt'

# 데이터 파일이 존재하면 읽어오고, 존재하지 않으면 초기 데이터를 사용
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        categories = json.load(f) #제이슨파일(f)을 읽어올때
else:
    categories = {'운동': [], '학습': [], '취미': [], '데이트': [], '여행': [], '기타': []}

def save_categories():
#카테고리에 사용자가 입력한 데이터 저장
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=4)

def get_weather(location):
    query = f"{location} 날씨"
    html = requests.get(f"https://search.naver.com/search.naver?query={query}")
    soup = BeautifulSoup(html.text, "html.parser")

    # 위치
    address = soup.find("div", {"class": "title_area _area_panel"}).find("h2", {"class": 'blind'}).text

    # 날씨정보
    weather_data = soup.find("div", {"class": "weather_info"})

    # 현재온도
    temperature = weather_data.find("div", {"class": "temperature_text"}).text.strip()[5:]

    # 날씨상태
    weather_status = weather_data.find("span", {"class": "weather before_slash"}).text

    # 미세먼지와 자외선 상태
    air = soup.find('ul', {'class': 'today_chart_list'})
    air_info = [info.text.strip() for info in air.find_all('li', {'class': 'item_today'})]

    return address, temperature, weather_status, air_info

@app.route('/')
def index():
    location = request.args.get('location', '동작구')
    address, temperature, weather_status, air_info = get_weather(location)
    return render_template('index.html', address=address, temperature=temperature, weather_status=weather_status,
                           air_info=air_info, categories=categories)

@app.route('/add', methods=['POST'])
def add():
    category = request.form['category']
    items = request.form['item'].split(',')  # 쉼표(,)를 기준으로 준비물을 분리
    for item in items:
        item = item.strip()  # 공백 제거
        if item:
            categories[category].append(item)  # 각 준비물을 해당 카테고리에 추가
    save_categories()  # 데이터 저장
    return redirect(url_for('index'))

@app.route('/categories')   #categories.html로 넘어가기
def show_categories():
    return render_template('categories.html', categories=categories)

@app.route('/reset', methods=['POST'])  #초기화 버튼 눌렀을 때, 실행
def reset():
    global categories
    categories = {'운동': [], '학습': [], '취미': [], '데이트': [], '여행': [], '기타': []}  # 초기 데이터로 재설정
    save_categories()  # 초기화된 데이터를 파일에 저장
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)