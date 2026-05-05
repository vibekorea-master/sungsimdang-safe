import streamlit as st
import streamlit.components.v1 as components
import json

# 1. Page Config & Custom CSS (Premium Typography)
st.set_page_config(page_title="Sungsimdang Safe Guide", layout="wide")

# 2. Settings (Change your Tistory URL here)
BLOG_BASE_URL = "https://your-blog.tistory.com"  # 사용자님의 티스토리 주소로 변경하세요.
GITHUB_BASE_URL = "https://raw.githubusercontent.com/dongkeuncho-cmyk/sungsimdang-safe/main/"

# 3. Legal Disclaimer & Facility Notice Text 
DISCLAIMER_HTML = """
<div style="background-color: #fef2f2; border-left: 5px solid #dc2626; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
    <h4 style="color: #991b1b; margin: 0; font-size: 14px;">⚠️ LEGAL DISCLAIMER (면책 조항)</h4>
    <p style="color: #b91c1c; font-size: 12px; margin: 5px 0 0 0;">
        This app is for <b>reference only</b> and is not an official Sungsimdang service. Ingredients may change without notice. 
        Final responsibility for safety lies with the user. Always verify with staff on-site before consumption.
    </p>
</div>
<div style="background-color: #fffbeb; border-left: 5px solid #f59e0b; padding: 15px; border-radius: 8px; margin-bottom: 25px;">
    <h4 style="color: #92400e; margin: 0; font-size: 14px;">🏭 Shared Facility Notice (제조시설 공유 고지)</h4>
    <p style="color: #b45309; font-size: 12px; margin: 5px 0 0 0;">
        All products are manufactured in a facility processing: <b>Eggs, Milk, Buckwheat, Peanuts, Soybeans, Wheat, Mackerel, Crab, Shrimp, Pork, Peaches, Tomatoes, Sulfites, Walnuts, Chicken, Beef, Squid, Shellfish, and Pine nuts.</b>
    </p>
</div>
"""

# 4. Sidebar: Premium Filter
st.sidebar.image("https://via.placeholder.com/150x50?text=SUNGSIMDANG", use_container_width=True)
st.sidebar.title("🚫 Filter Allergens")
st.sidebar.markdown("---")

all_ingredients = sorted([
    "Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", 
    "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", 
    "Shellfish (Oyster)", "Tomato"
])
avoid = st.sidebar.multiselect("I am allergic to:", all_ingredients, help="Selected ingredients will be hidden.")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Click the button on each card to read a detailed review on our blog.")

# 5. Bread Data (29 Items with Korean Names) 
bread_data = [
    {"id": 1, "name": "Malami Croquette", "ko": "마라미고로케", "price": "3,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"], "img": "images/1. Malami Croquette.png", "desc": "Spicy Mala Xiangguo sauce with minced pork."},
    {"id": 2, "name": "Pain au Chocolat", "ko": "뺑오쇼콜라", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/2. Pain au Chocolat.png", "desc": "Crispy pastry with French chocolate sticks."},
    {"id": 3, "name": "Mochi-Mochi Milk Bread", "ko": "모찌모찌식빵", "price": "3,500", "allergens": ["Soybean", "Pork", "Wheat", "Milk"], "img": "images/3. Mochi-Mochi Milk Bread.png", "desc": "Chewy texture made with whole milk powder."},
    {"id": 4, "name": "Vegetable Croquette", "ko": "야채고로케", "price": "2,300", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/4. Vegetable Croquette.png", "desc": "Fresh onions and sausages with domestic pork."},
    {"id": 5, "name": "Little Echo", "ko": "작은메아리", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/5. Little Echo.png", "desc": "Mini version of Bomunsan Echo."},
    {"id": 6, "name": "Noix Raisin", "ko": "노아레즌", "price": "7,000", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/6. Noix Raisin.png", "desc": "Organic flour with walnuts and raisins."},
    {"id": 7, "name": "October Fig", "ko": "시월의무화과", "price": "5,000", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/7. October Fig.png", "desc": "Seasonal fig bread made with organic flour."},
    {"id": 8, "name": "Big Match", "ko": "빅매치", "price": "2,300", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/8. Big Match.png", "desc": "Cream cheese with a sweet biscuit top."},
    {"id": 9, "name": "Under the Fig Tree", "ko": "무화과그늘아래", "price": "3,000", "allergens": ["Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/9. Under the Fig Tree.png", "desc": "Wholesome bread with figs and cream cheese."},
    {"id": 10, "name": "Steak Bread", "ko": "스테이크빵", "price": "2,300", "allergens": ["Egg", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/10. Steak Bread.png", "desc": "Korean-style sliced grilled pork with onions."},
    {"id": 11, "name": "Sunflower", "ko": "해바라기", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/11. Sunflower.png", "desc": "Frankfurt sausage and domestic onions."},
    {"id": 12, "name": "Soboro Bun", "ko": "소보로", "price": "1,300", "allergens": ["Egg", "Soybean", "Peanut", "Wheat", "Milk"], "img": "images/12. Soboro Bun.png", "desc": "Classic Korean Streusel Bun."},
    {"id": 13, "name": "Sweet Red Bean Bun", "ko": "단팥빵", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/13. Sweet Red Bean Bun.png", "desc": "Traditional red bean paste with walnuts."},
    {"id": 14, "name": "Cream Cheese White Bun", "ko": "크림치즈화이트번", "price": "3,300", "allergens": ["Wheat", "Sulfites", "Milk"], "img": "images/14. Cream Cheese White Bun.png", "desc": "Soft bun with New Zealand cream cheese."},
    {"id": 15, "name": "Bread Donut", "ko": "빵도넛", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/15. Bread Donut.png", "desc": "Fried donut filled with red bean paste."},
    {"id": 16, "name": "Long Twist", "ko": "키다리트위스트", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/16. Long Twist.png", "desc": "Buttery twisted bread with vegetable oil."},
    {"id": 17, "name": "French Pie", "ko": "후렌치파이", "price": "2,000", "allergens": ["Egg", "Wheat", "Milk"], "img": "images/17. French Pie.png", "desc": "Raspberry and domestic strawberry jam."},
    {"id": 18, "name": "Almond Croissant", "ko": "아몬드크로와상", "price": "3,500", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/18. Almond Croissant.png", "desc": "Buttery croissant with USA almonds."},
    {"id": 19, "name": "Stone-Ground Whole Wheat Bread", "ko": "맷돌로갈은통밀빵", "price": "4,500", "allergens": ["Wheat", "Walnut"], "img": "images/19. Stone-Ground Whole Wheat Bread.png", "desc": "Organic whole wheat flour and walnuts."},
    {"id": 20, "name": "Squid Ink Baton", "ko": "오징어먹물방망이", "price": "3,300", "allergens": ["Egg", "Pork", "Wheat", "Squid", "Milk"], "img": "images/20. Squid Ink Baton.png", "desc": "Spanish squid ink with condensed milk."},
    {"id": 21, "name": "Red Wine Bread", "ko": "레드와인", "price": "4,500", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/21. Red Wine Bread.png", "desc": "Made with Spanish wine and German rye."},
    {"id": 22, "name": "Walnut Bread", "ko": "월넛브레드", "price": "4,000", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/22. Walnut Bread.png", "desc": "Hearty bread packed with USA walnuts."},
    {"id": 23, "name": "Toyo Bread", "ko": "토요빵", "price": "3,800", "allergens": ["Soybean", "Wheat", "Beef", "Milk"], "img": "images/23. Toyo Bread.png", "desc": "Sweet potato and cream cheese filling."},
    {"id": 24, "name": "Plain Croissant", "ko": "플레인크로와상", "price": "2,800", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/24. Plain Croissant.png", "desc": "Classic croissant with French butter."},
    {"id": 25, "name": "Bomunsan Echo", "ko": "보문산메아리", "price": "6,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/25. Bomunsan Echo.png", "desc": "Signature pastry with layered butter."},
    {"id": 26, "name": "Pie Manju Set", "ko": "파이만주세트", "price": "9,600", "allergens": ["Egg", "Soybean", "Wheat", "Milk", "Walnut"], "img": "images/26. Pie Manju Set.png", "desc": "Red bean manju with almond powder."},
    {"id": 27, "name": "Pantaloon Chive Bread", "ko": "판타롱부추빵", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)"], "img": "images/27. Pantaloon Chive Bread.png", "desc": "Famous bread with domestic chives and eggs."},
    {"id": 28, "name": "Twiso-guma", "ko": "튀소구마", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/28. Twiso-guma.png", "desc": "Fried sweet potato soboro bun."},
    {"id": 29, "name": "Twigim Soboro", "ko": "튀김소보로", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/29. Twigim Soboro.png", "desc": "Legendary fried red bean soboro bun."}
]

# 6. Filtering Logic
filtered = [b for b in bread_data if not any(a in b["allergens"] for a in avoid)]

# 7. Main Rendering
st.markdown("<h1 style='text-align: center; color: #78350f;'>🥖 Sungsimdang Safe Guide</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #92400e; margin-bottom: 30px;'>Accurate Ingredient Guide for International Tourists</p>", unsafe_allow_html=True)

# Fixed Top Disclaimers
components.html(DISCLAIMER_HTML, height=220)

st.markdown(f"**{len(filtered)}** items found. We prioritize your safety.")

# Bread Grid (Premium HTML/JS)
bread_json = json.dumps(filtered)
html_code = f"""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<style>
    body {{ font-family: 'Poppins', sans-serif; }}
    .bread-card {{ transition: all 0.3s cubic-bezier(.25,.8,.25,1); }}
    .bread-card:hover {{ transform: translateY(-10px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04); }}
</style>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 p-4 bg-orange-50">
    <script>
        const data = {bread_json};
        const baseUrl = "{GITHUB_BASE_URL}";
        const blogUrl = "{BLOG_BASE_URL}";
        
        data.forEach(bread => {{
            document.write(`
                <div class="bread-card bg-white rounded-[2rem] overflow-hidden border border-orange-100 flex flex-col h-full shadow-md">
                    <div class="h-60 overflow-hidden bg-gray-100 relative">
                        <img src="${{encodeURI(baseUrl + bread.img)}}" 
                             style="width: 115%; height: 115%; object-fit: cover; object-position: left top; max-width: none;"
                             class="transition-transform duration-700 hover:scale-105" 
                             onerror="this.src='https://via.placeholder.com/400x300?text=Image+Syncing...';">
                    </div>
                    <div class="p-6 flex flex-col flex-grow">
                        <div class="flex justify-between items-start mb-3">
                            <div>
                                <h3 class="text-lg font-bold text-gray-800 leading-tight">${{bread.name}}</h3>
                                <p class="text-xs text-orange-800 font-semibold opacity-70">${{bread.ko}}</p>
                            </div>
                            <span class="text-orange-600 font-bold text-md ml-2">${{bread.price}}W</span>
                        </div>
                        <div class="flex flex-wrap gap-1 mb-4">
                            ${{bread.allergens.map(a => `<span class="px-2 py-0.5 bg-orange-100 text-orange-700 text-[9px] rounded-full font-bold uppercase">${{a}}</span>`).join('')}}
                        </div>
                        <p class="text-xs text-gray-500 mb-6 flex-grow italic">"${{bread.desc}}"</p>
                        <a href="${{blogUrl}}" target="_blank" 
                           class="block w-full text-center bg-[#78350f] hover:bg-[#92400e] text-white py-3 rounded-2xl text-[11px] font-bold transition-colors shadow-lg">
                           View Details & Blog Review ↗
                        </a>
                    </div>
                </div>
            `);
        }});
    </script>
</div>
"""
components.html(html_code, height=3000, scrolling=True)
