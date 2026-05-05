import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="Sungsimdang Image Test", layout="wide")

# 2. 1번 마라미고로케 데이터 (영문 문서 기준 )
bread_data = [
    {
        "id": 1, 
        "name": "Malami Croquette", 
        "price": "3,000", 
        "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"], 
        "img": "images/1. Malami Croquette.png", 
        "desc": "Spicy Mala Xiangguo sauce with minced pork."
    }
]

# 3. 메인 타이틀
st.title("🥖 Sungsimdang Image Test (Item No. 1)")
st.write("Checking if 'images/1. Malami Croquette.png' displays correctly.")

# 4. 카드 렌더링 (HTML/Tailwind CSS)
bread_json = json.dumps(bread_data)
html_code = f"""
<script src="https://cdn.tailwindcss.com"></script>
<div class="flex justify-center p-10 bg-orange-50">
    <script>
        const data = {bread_json};
        data.forEach(bread => {{
            document.write(`
                <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-orange-200 w-80">
                    <div class="h-64 overflow-hidden bg-gray-200">
                        <img src="${{encodeURI(bread.img)}}" class="w-full h-full object-cover transform scale-110" 
                             onerror="this.src='https://via.placeholder.com/400x300?text=Check+Filename+In+Images+Folder';">
                    </div>
                    <div class="p-6">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-xl font-bold text-gray-800">${{bread.name}}</h3>
                            <span class="text-orange-600 font-extrabold">${{bread.price}} W</span>
                        </div>
                        <p class="text-xs text-gray-400 mb-2 font-bold uppercase tracking-tighter">Allergens: ${{bread.allergens.join(', ')}}</p>
                        <p class="text-sm text-gray-600 italic">"${{bread.desc}}"</p>
                    </div>
                </div>
            `);
        }});
    </script>
</div>
"""
components.html(html_code, height=600)
