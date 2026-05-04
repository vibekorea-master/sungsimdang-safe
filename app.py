import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="성심당 알러지 세이프 가이드", layout="wide", initial_sidebar_state="expanded")

# 2. 데이터 정의 (알러지 정보 포함)
bread_data = [
    {"id": 1, "name": "마라미고로케", "allergens": ["밀", "대두", "돼지고기", "쇠고기"], "link": "https://travelbuddy-korea.tistory.com/2", "desc": "매콤한 마라향이 가득한 특별한 고로케", "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"},
    {"id": 2, "name": "뺑오쇼콜라", "allergens": ["밀", "우유", "계란", "대두"], "link": "https://travelbuddy-korea.tistory.com/3", "desc": "겹겹이 쌓인 페이스트리 속 달콤한 초콜릿", "img": "https://images.unsplash.com/photo-1530610476181-d83430b64dcd?w=400"},
    {"id": 3, "name": "모찌모찌식빵", "allergens": ["밀", "우유"], "link": "https://travelbuddy-korea.tistory.com/4", "desc": "쫄깃쫄깃한 식감이 일품인 식빵", "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"},
    {"id": 4, "name": "야채고로케", "allergens": ["밀", "계란", "돼지고기"], "link": "https://travelbuddy-korea.tistory.com/5", "desc": "아삭한 야채와 고소한 튀김의 환상 궁합", "img": "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=400"},
    {"id": 5, "name": "작은메아리", "allergens": ["밀", "우유"], "link": "https://travelbuddy-korea.tistory.com/6", "desc": "바삭하고 달콤한 퀸아망 스타일", "img": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400"},
    {"id": 6, "name": "노아레즌", "allergens": ["밀", "호두"], "link": "https://travelbuddy-korea.tistory.com/7", "desc": "건포도와 호두가 들어간 건강 호밀빵", "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"},
    {"id": 7, "name": "시월의무화과", "allergens": ["밀"], "link": "https://travelbuddy-korea.tistory.com/8", "desc": "톡톡 터지는 무화과의 풍미", "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"},
    {"id": 8, "name": "빅매치", "allergens": ["밀", "우유", "계란"], "link": "https://travelbuddy-korea.tistory.com/9", "desc": "크림치즈가 가득한 인기 메뉴", "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"},
    {"id": 9, "name": "무화과그늘아래", "allergens": ["밀", "호두"], "link": "https://travelbuddy-korea.tistory.com/10", "desc": "호두와 무화과의 조화로운 건강빵", "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"},
    {"id": 10, "name": "스테이크빵", "allergens": ["밀", "쇠고기", "대두"], "link": "https://travelbuddy-korea.tistory.com/11", "desc": "든든한 고기가 들어간 조리빵", "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"}
]

# 3. 사이드바 - 알러지 필터링 기능
st.sidebar.header("🚫 알러지 유발 성분 선택")
st.sidebar.write("못 드시는 성분을 선택하시면 해당 빵을 제외해 드립니다.")

all_allergens = ["밀", "우유", "계란", "대두", "돼지고기", "쇠고기", "호두"]
user_allergies = st.sidebar.multiselect("피해야 할 성분:", all_allergens)

# 4. 필터링 로직
filtered_breads = []
for bread in bread_data:
    # 사용자가 선택한 알러지 성분이 빵의 성분에 하나라도 포함되어 있는지 확인
    if not any(allergen in bread["allergens"] for allergen in user_allergies):
        filtered_breads.append(bread)

# 5. 메인 화면 구성
st.title("🥖 성심당 알러지 세이프 가이드")
st.markdown(f"현재 **{len(filtered_breads)}개**의 안전한 빵을 찾았습니다.")

if user_allergies:
    st.info(f"알러지 유발 성분 [{', '.join(user_allergies)}] 제외됨")

# 6. HTML 카드 생성 (필터링된 데이터만 자바스크립트로 전달)
import json
bread_json = json.dumps(filtered_breads)

html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .bread-card {{ transition: all 0.3s ease; }}
        .bread-card:hover {{ transform: translateY(-8px); }}
    </style>
</head>
<body class="bg-orange-50 p-4">
    <div id="bread-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    </div>

    <script>
        const breadData = {bread_json};
        const grid = document.getElementById('bread-grid');

        breadData.forEach(bread => {{
            const card = `
                <div class="bread-card bg-white rounded-xl shadow-md overflow-hidden border border-orange-100 flex flex-col h-full">
                    <img src="${{bread.img}}" class="w-full h-40 object-cover" alt="${{bread.name}}">
                    <div class="p-4 flex flex-col flex-grow">
                        <div class="flex justify-between items-start mb-2">
                            <h3 class="text-lg font-bold text-gray-800">${{bread.name}}</h3>
                            <span class="bg-green-100 text-green-700 text-[10px] px-2 py-1 rounded-full font-bold">안전</span>
                        </div>
                        <p class="text-xs text-gray-500 mb-2">성분: ${{bread.allergens.join(', ')}}</p>
                        <p class="text-sm text-gray-600 mb-4 flex-grow">${{bread.desc}}</p>
                        <a href="${{bread.link}}" target="_blank" 
                           class="block w-full text-center bg-orange-500 hover:bg-orange-600 text-white text-sm font-bold py-2 px-4 rounded-lg transition-colors">
                           리뷰 보기
                        </a>
                    </div>
                </div>
            `;
            grid.innerHTML += card;
        }});
    </script>
</body>
</html>
"""

components.html(html_template, height=1200, scrolling=True)
