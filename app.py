import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="성심당 알러지 세이프 가이드", layout="wide")

# 2. 데이터 정의 (사용자님의 티스토리 주소와 이미지 매칭)
# 이미지 주소는 티스토리 본문 이미지의 일반적인 경로 패턴을 적용했습니다.
bread_data = [
    {"id": 1, "name": "마라미고로케", "allergens": ["밀", "대두", "돼지고기", "쇠고기"], "link": "https://travelbuddy-korea.tistory.com/2", "desc": "매콤한 마라향이 가득한 특별한 고로케", "img": "https://blog.kakaocdn.net/dn/bcNq3r/btsI9Pz3p5M/kS8L9f5K8K9k9k9k9k9k9k/img.jpg"}, # 예시 경로
    {"id": 2, "name": "뺑오쇼콜라", "allergens": ["밀", "우유", "계란", "대두"], "link": "https://travelbuddy-korea.tistory.com/3", "desc": "겹겹이 쌓인 페이스트리 속 달콤한 초콜릿", "img": "https://blog.kakaocdn.net/dn/dummy/bts/img.jpg"},
    {"id": 3, "name": "모찌모찌식빵", "allergens": ["밀", "우유"], "link": "https://travelbuddy-korea.tistory.com/4", "desc": "쫄깃쫄깃한 식감이 일품인 식빵", "img": "https://blog.kakaocdn.net/dn/dummy/bts/img.jpg"},
    {"id": 4, "name": "야채고로케", "allergens": ["밀", "계란", "돼지고기"], "link": "https://travelbuddy-korea.tistory.com/5", "desc": "아삭한 야채와 고소한 튀김의 환상 궁합", "img": "https://blog.kakaocdn.net/dn/dummy/bts/img.jpg"},
    {"id": 5, "name": "작은메아리", "allergens": ["밀", "우유"], "link": "https://travelbuddy-korea.tistory.com/6", "desc": "바삭하고 달콤한 퀸아망 스타일", "img": "https://blog.kakaocdn.net/dn/dummy/bts/img.jpg"},
    {"id": 6, "name": "노아레즌", "allergens": ["밀", "호두"], "link": "https://travelbuddy-korea.tistory.com/7", "desc": "건포도와 호두가 들어간 건강 호밀빵", "img": "https://blog.kakaocdn.net/dn/dummy/bts/img.jpg"},
    {"id": 7, "name": "시월의무화과", "allergens": ["밀"], "link": "https://travelbuddy-korea.tistory.com/8", "desc": "톡톡 터지는 무화과의 풍미", "img": "https://blog.kakaocdn.net/dn/dummy/bts/img.jpg"},
    {"id": 8, "name": "빅매치", "allergens": ["밀", "우유", "계란"], "link": "https://travelbuddy-korea.tistory.com/9", "desc": "크림치즈가 가득한 인기 메뉴", "img": "https://blog.kakaocdn.net/dn/dummy/bts/img.jpg"},
    {"id": 9, "name": "무화과그늘아래", "allergens": ["밀", "호두"], "link": "https://travelbuddy-korea.tistory.com/10", "desc": "호두와 무화과의 조화로운 건강빵", "img": "https://blog.kakaocdn.net/dn/dummy/bts/img.jpg"},
    {"id": 10, "name": "스테이크빵", "allergens": ["밀", "쇠고기", "대두"], "link": "https://travelbuddy-korea.tistory.com/11", "desc": "든든한 고기가 들어간 조리빵", "img": "https://blog.kakaocdn.net/dn/dummy/bts/img.jpg"}
]

# 3. 사이드바 알러지 필터
st.sidebar.header("🚫 알러지 유발 성분 제외")
all_allergens = ["밀", "우유", "계란", "대두", "돼지고기", "쇠고기", "호두"]
user_allergies = st.sidebar.multiselect("선택한 성분이 포함된 빵은 숨겨집니다:", all_allergens)

# 필터링 로직
filtered_breads = [b for b in bread_data if not any(a in b["allergens"] for a in user_allergies)]

# 4. 메인 화면
st.title("🥖 성심당 알러지 세이프 가이드")
st.write(f"현재 선택하신 조건에서 안전한 빵은 **{len(filtered_breads)}개**입니다.")

# HTML 렌더링
bread_json = json.dumps(filtered_breads)
html_code = f"""
<script src="https://cdn.tailwindcss.com"></script>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-4">
    <script>
        const data = {bread_json};
        document.write(data.map(bread => `
            <div class="bg-white rounded-xl shadow-lg border border-orange-100 overflow-hidden flex flex-col">
                <div class="h-48 bg-orange-100 overflow-hidden">
                    <img src="${{bread.img}}" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x300?text=%EC%82%AC%EC%A7%84%20%EB%B6%88%EB%9F%AC%EC%98%A4%EA%B8%B0%20%EC%8B%A4%ED%8C%A8';">
                </div>
                <div class="p-4 flex flex-col flex-grow">
                    <h3 class="text-xl font-bold text-gray-800 mb-1">${{bread.name}}</h3>
                    <p class="text-xs text-orange-600 font-semibold mb-2">포함 성분: ${{bread.allergens.join(', ')}}</p>
                    <p class="text-sm text-gray-600 mb-4 flex-grow">${{bread.desc}}</p>
                    <a href="${{bread.link}}" target="_blank" class="block w-full text-center bg-orange-500 text-white py-2 rounded-lg font-bold hover:bg-orange-600 transition">리뷰 확인하기</a>
                </div>
            </div>
        `).join(''));
    </script>
</div>
"""

components.html(html_code, height=1500, scrolling=True)
