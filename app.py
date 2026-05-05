import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="Sungsimdang Image Test", layout="wide")

# 2. GitHub 저장소 직통 주소 설정 (사용자님 정보 반영 )
# 이 주소는 GitHub의 실제 이미지 파일에 직접 연결됩니다.
GITHUB_BASE_URL = "https://raw.githubusercontent.com/dongkeuncho-cmyk/sungsimdang-safe/main/"

bread_data = [
    {
        "id": 1, 
        "name": "Malami Croquette", 
        "price": "3,000", 
        "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"], 
        "img": "images/1. Malami Croquette.png", # 파일명 정확히 일치 
        "desc": "Spicy Mala Xiangguo sauce with minced pork."
    }
]

# 3. 메인 타이틀
st.title("🥖 Sungsimdang Image Test (Raw URL Mode)")

# 4. 카드 렌더링
bread_json = json.dumps(bread_data)
html_code = f"""
<script src="https://cdn.tailwindcss.com"></script>
<div class="flex justify-center p-10 bg-orange-50">
    <script>
        const data = {bread_json};
        const baseUrl = "{GITHUB_BASE_URL}";
        
        data.forEach(bread => {{
            // 전체 주소 생성: baseUrl + images/파일명 
            const fullImgUrl = baseUrl + bread.img;
            
            document.write(`
                <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-orange-200 w-80">
                    <div class="h-64 overflow-hidden bg-gray-200">
                        <img src="${{encodeURI(fullImgUrl)}}" class="w-full h-full object-cover transform scale-110" 
                             onerror="this.src='https://via.placeholder.com/400x300?text=Image+Not+Found';">
                    </div>
                    <div class="p-6">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-xl font-bold text-gray-800">${{bread.name}}</h3>
                            <span class="text-orange-600 font-extrabold text-lg">${{bread.price}} W</span>
                        </div>
                        <p class="text-xs text-gray-400 mb-2 font-bold uppercase">Allergens: ${{bread.allergens.join(', ')}}</p>
                        <p class="text-sm text-gray-600 italic">"${{bread.desc}}"</p>
                    </div>
                </div>
            `);
        }});
    </script>
</div>
"""
components.html(html_code, height=600)
