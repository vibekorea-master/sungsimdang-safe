import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정
st.set_page_config(page_title="Sungsimdang Safe Guide", layout="wide")

# 2. GitHub Raw Base URL (사용자님 정보 반영)
GITHUB_BASE_URL = "https://raw.githubusercontent.com/dongkeuncho-cmyk/sungsimdang-safe/main/"

# 3. 29종 빵 전체 데이터 (DOCX 영문본 기준) [cite: 4-157]
bread_data = [
    {"id": 1, "name": "Malami Croquette", "price": "3,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"], "img": "images/1. Malami Croquette.png", "desc": "Spicy Mala Xiangguo sauce with minced pork."},
    {"id": 2, "name": "Pain au Chocolat", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/2. Pain au Chocolat.png", "desc": "Crispy pastry with French chocolate sticks."},
    {"id": 3, "name": "Mochi-Mochi Milk Bread", "price": "3,500", "allergens": ["Soybean", "Pork", "Wheat", "Milk"], "img": "images/3. Mochi-Mochi Milk Bread.png", "desc": "Chewy texture made with whole milk powder."},
    {"id": 4, "name": "Vegetable Croquette", "price": "2,300", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/4. Vegetable Croquette.png", "desc": "Fresh onions and sausages with domestic pork."},
    {"id": 5, "name": "Little Echo", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/5. Little Echo.png", "desc": "Mini version of Bomunsan Echo with butter sheet."},
    {"id": 6, "name": "Noix Raisin", "price": "7,000", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/6. Noix Raisin.png", "desc": "Organic strong wheat flour with walnuts and raisins."},
    {"id": 7, "name": "October Fig", "price": "5,000", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/7. October Fig.png", "desc": "Seasonal fig bread made with organic flour."},
    {"id": 8, "name": "Big Match", "price": "2,300", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/8. Big Match.png", "desc": "New Zealand cream cheese with a sweet biscuit top."},
    {"id": 9, "name": "Under the Fig Tree", "price": "3,000", "allergens": ["Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/9. Under the Fig Tree.png", "desc": "Wholesome bread with figs and cream cheese."},
    {"id": 10, "name": "Steak Bread", "price": "2,300", "allergens": ["Egg", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/10. Steak Bread.png", "desc": "Korean-style sliced grilled pork with onions."},
    {"id": 11, "name": "Sunflower", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/11. Sunflower.png", "desc": "Frankfurt sausage and domestic onions."},
    {"id": 12, "name": "Soboro Bun", "price": "1,300", "allergens": ["Egg", "Soybean", "Peanut", "Wheat", "Milk"], "img": "images/12. Soboro Bun.png", "desc": "Classic Korean Streusel Bun with domestic eggs."},
    {"id": 13, "name": "Sweet Red Bean Bun", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/13. Sweet Red Bean Bun.png", "desc": "Traditional whole red bean paste with walnuts."},
    {"id": 14, "name": "Cream Cheese White Bun", "price": "3,300", "allergens": ["Wheat", "Sulfites", "Milk"], "img": "images/14. Cream Cheese White Bun.png", "desc": "Soft bun with New Zealand cream cheese."},
    {"id": 15, "name": "Bread Donut", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/15. Bread Donut.png", "desc": "Fried donut filled with sweet red bean paste."},
    {"id": 16, "name": "Long Twist", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/16. Long Twist.png", "desc": "Buttery twisted bread with vegetable oil."},
    {"id": 17, "name": "French Pie", "price": "2,000", "allergens": ["Egg", "Wheat", "Milk"], "img": "images/17. French Pie.png", "desc": "Raspberry and domestic strawberry jam."},
    {"id": 18, "name": "Almond Croissant", "price": "3,500", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/18. Almond Croissant.png", "desc": "Buttery French croissant with USA almonds."},
    {"id": 19, "name": "Stone-Ground Whole Wheat Bread", "price": "4,500", "allergens": ["Wheat", "Walnut"], "img": "images/19. Stone-Ground Whole Wheat Bread.png", "desc": "Organic whole wheat flour and walnuts."},
    {"id": 20, "name": "Squid Ink Baton", "price": "3,300", "allergens": ["Egg", "Pork", "Wheat", "Squid", "Milk"], "img": "images/20. Squid Ink Baton.png", "desc": "Spanish squid ink with domestic condensed milk."},
    {"id": 21, "name": "Red Wine Bread", "price": "4,500", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/21. Red Wine Bread.png", "desc": "Bread made with Spanish wine and German rye."},
    {"id": 22, "name": "Walnut Bread", "price": "4,000", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/22. Walnut Bread.png", "desc": "Hearty bread packed with USA walnuts."},
    {"id": 23, "name": "Toyo Bread", "price": "3,800", "allergens": ["Soybean", "Wheat", "Beef", "Milk"], "img": "images/23. Toyo Bread.png", "desc": "Saturday bread with sweet potato and cream cheese."},
    {"id": 24, "name": "Plain Croissant", "price": "2,800", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/24. Plain Croissant.png", "desc": "Classic croissant with French butter sheet."},
    {"id": 25, "name": "Bomunsan Echo", "price": "6,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/25. Bomunsan Echo.png", "desc": "Signature pastry with layered butter sheet."},
    {"id": 26, "name": "Pie Manju Set", "price": "9,600", "allergens": ["Egg", "Soybean", "Wheat", "Milk", "Walnut"], "img": "images/26. Pie Manju Set.png", "desc": "8 pcs of red bean manju with almond powder."},
    {"id": 27, "name": "Pantaloon Chive Bread", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)"], "img": "images/27. Pantaloon Chive Bread.png", "desc": "Famous bread with domestic chives and eggs."},
    {"id": 28, "name": "Twiso-guma", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/28. Twiso-guma.png", "desc": "Fried sweet potato soboro with domestic sweet potato."},
    {"id": 29, "name": "Twigim Soboro", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/29. Twigim Soboro.png", "desc": "Legendary fried red bean soboro bun."}
]

# 4. 사이드바 필터
st.sidebar.title("🚫 Allergy Filter")
all_ingredients = sorted(["Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", "Shellfish (Oyster)", "Tomato"])
avoid = st.sidebar.multiselect("Avoid ingredients:", all_ingredients)

filtered = [b for b in bread_data if not any(a in b["allergens"] for a in avoid)]

# 5. UI 렌더링 (HTML)
st.title("🥖 Sungsimdang Safe Guide (Full 29 Items)")
st.markdown(f"Found **{len(filtered)}** items safe for you. Enjoy Daejeon's best bread!")

bread_json = json.dumps(filtered)
html_code = f"""
<script src="https://cdn.tailwindcss.com"></script>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 p-4 bg-orange-50">
    <script>
        const data = {bread_json};
        const baseUrl = "{GITHUB_BASE_URL}";
        data.forEach(bread => {{
            document.write(`
                <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-orange-100 flex flex-col h-full">
                    <div class="h-52 overflow-hidden bg-gray-200">
                        <img src="${{encodeURI(baseUrl + bread.img)}}" class="w-full h-full object-cover transition-transform duration-500 hover:scale-110" 
                             onerror="this.src='https://via.placeholder.com/400x300?text=Wait+for+GitHub+Sync';">
                    </div>
                    <div class="p-5 flex flex-col flex-grow">
                        <div class="flex justify-between items-start mb-2">
                            <h3 class="text-sm font-bold text-gray-800 leading-tight">${{bread.name}}</h3>
                            <span class="text-orange-600 font-bold text-xs ml-2">${{bread.price}}W</span>
                        </div>
                        <p class="text-[8px] text-gray-400 mb-2 font-bold uppercase tracking-tighter">Allergens: ${{bread.allergens.join(', ')}}</p>
                        <p class="text-[11px] text-gray-600 mb-4 flex-grow italic leading-snug">"${{bread.desc}}"</p>
                        <div class="text-center bg-green-600 text-white py-2 rounded-lg text-[10px] font-bold shadow-sm">SAFE ✅</div>
                    </div>
                </div>
            `);
        }});
    </script>
</div>
"""
components.html(html_code, height=2500, scrolling=True)
