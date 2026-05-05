import streamlit as st
import streamlit.components.v1 as components
import json

# 1. Page Configuration
st.set_page_config(page_title="Sungsimdang Allergy Safe Guide", layout="wide")

# 2. GitHub Raw Base URL
GITHUB_BASE_URL = "https://raw.githubusercontent.com/dongkeuncho-cmyk/sungsimdang-safe/main/"

# 3. Shared Facility Notice Text 
SHARED_FACILITY_TEXT = """
**⚠️ Shared Facility Notice:** This product is manufactured in the same facility as products containing:  
*Eggs (poultry), Milk, Buckwheat, Peanuts, Soybeans, Wheat, Mackerel, Crab, Shrimp, Pork, Peaches, Tomatoes, Sulfites, Walnuts, Chicken, Beef, Squid, Shellfish (including Oysters, Abalone, and Mussels), and Pine nuts.*
"""

# 4. Sidebar: Filter ONLY (직관적인 구성을 위해 안내문 제거)
st.sidebar.title("🚫 Filter Ingredients")
st.sidebar.write("Select ingredients to hide:")

all_ingredients = sorted([
    "Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", 
    "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", 
    "Shellfish (Oyster)", "Tomato"
])
avoid = st.sidebar.multiselect("Avoid these:", all_ingredients)

# 5. Bread Data (29 items fully verified [cite: 4-157])
bread_data = [
    {"id": 1, "name": "Malami Croquette", "price": "3,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"], "img": "images/1. Malami Croquette.png", "desc": "Spicy Mala Xiangguo sauce with minced pork."},
    {"id": 2, "name": "Pain au Chocolat", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/2. Pain au Chocolat.png", "desc": "Crispy pastry with French chocolate sticks."},
    {"id": 3, "name": "Mochi-Mochi Milk Bread", "price": "3,500", "allergens": ["Soybean", "Pork", "Wheat", "Milk"], "img": "images/3. Mochi-Mochi Milk Bread.png", "desc": "Chewy texture made with whole milk powder."},
    {"id": 4, "name": "Vegetable Croquette", "price": "2,300", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/4. Vegetable Croquette.png", "desc": "Fresh onions and sausages with domestic pork."},
    {"id": 5, "name": "Little Echo", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/5. Little Echo.png", "desc": "Mini version of Bomunsan Echo."},
    {"id": 6, "name": "Noix Raisin", "price": "7,000", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/6. Noix Raisin.png", "desc": "Organic flour with walnuts and raisins."},
    {"id": 7, "name": "October Fig", "price": "5,000", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/7. October Fig.png", "desc": "Seasonal fig bread made with organic flour."},
    {"id": 8, "name": "Big Match", "price": "2,300", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/8. Big Match.png", "desc": "Cream cheese with a sweet biscuit top."},
    {"id": 9, "name": "Under the Fig Tree", "price": "3,000", "allergens": ["Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/9. Under the Fig Tree.png", "desc": "Wholesome bread with figs and cream cheese."},
    {"id": 10, "name": "Steak Bread", "price": "2,300", "allergens": ["Egg", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/10. Steak Bread.png", "desc": "Korean-style sliced grilled pork with onions."},
    {"id": 11, "name": "Sunflower", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/11. Sunflower.png", "desc": "Frankfurt sausage and domestic onions."},
    {"id": 12, "name": "Soboro Bun", "price": "1,300", "allergens": ["Egg", "Soybean", "Peanut", "Wheat", "Milk"], "img": "images/12. Soboro Bun.png", "desc": "Classic Korean Streusel Bun."},
    {"id": 13, "name": "Sweet Red Bean Bun", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/13. Sweet Red Bean Bun.png", "desc": "Traditional red bean paste with walnuts."},
    {"id": 14, "name": "Cream Cheese White Bun", "price": "3,300", "allergens": ["Wheat", "Sulfites", "Milk"], "img": "images/14. Cream Cheese White Bun.png", "desc": "Soft bun with New Zealand cream cheese."},
    {"id": 15, "name": "Bread Donut", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/15. Bread Donut.png", "desc": "Fried donut filled with red bean paste."},
    {"id": 16, "name": "Long Twist", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/16. Long Twist.png", "desc": "Buttery twisted bread with vegetable oil."},
    {"id": 17, "name": "French Pie", "price": "2,000", "allergens": ["Egg", "Wheat", "Milk"], "img": "images/17. French Pie.png", "desc": "Raspberry and domestic strawberry jam."},
    {"id": 18, "name": "Almond Croissant", "price": "3,500", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/18. Almond Croissant.png", "desc": "Buttery croissant with USA almonds."},
    {"id": 19, "name": "Stone-Ground Whole Wheat Bread", "price": "4,500", "allergens": ["Wheat", "Walnut"], "img": "images/19. Stone-Ground Whole Wheat Bread.png", "desc": "Organic whole wheat flour and walnuts."},
    {"id": 20, "name": "Squid Ink Baton", "price": "3,300", "allergens": ["Egg", "Pork", "Wheat", "Squid", "Milk"], "img": "images/20. Squid Ink Baton.png", "desc": "Spanish squid ink with condensed milk."},
    {"id": 21, "name": "Red Wine Bread", "price": "4,500", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/21. Red Wine Bread.png", "desc": "Made with Spanish wine and German rye."},
    {"id": 22, "name": "Walnut Bread", "price": "4,000", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/22. Walnut Bread.png", "desc": "Hearty bread packed with USA walnuts."},
    {"id": 23, "name": "Toyo Bread", "price": "3,800", "allergens": ["Soybean", "Wheat", "Beef", "Milk"], "img": "images/23. Toyo Bread.png", "desc": "Sweet potato and cream cheese filling."},
    {"id": 24, "name": "Plain Croissant", "price": "2,800", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/24. Plain Croissant.png", "desc": "Classic croissant with French butter."},
    {"id": 25, "name": "Bomunsan Echo", "price": "6,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/25. Bomunsan Echo.png", "desc": "Signature pastry with layered butter."},
    {"id": 26, "name": "Pie Manju Set", "price": "9,600", "allergens": ["Egg", "Soybean", "Wheat", "Milk", "Walnut"], "img": "images/26. Pie Manju Set.png", "desc": "Red bean manju with almond powder."},
    {"id": 27, "name": "Pantaloon Chive Bread", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)"], "img": "images/27. Pantaloon Chive Bread.png", "desc": "Famous bread with domestic chives and eggs."},
    {"id": 28, "name": "Twiso-guma", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/28. Twiso-guma.png", "desc": "Fried sweet potato soboro bun."},
    {"id": 29, "name": "Twigim Soboro", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/29. Twigim Soboro.png", "desc": "Legendary fried red bean soboro bun."}
]

# 6. Main UI Rendering
st.title("🥖 Sungsimdang Safe Guide")

# 메인 상단에 제조시설 안내 배치 (강렬하게 경고) 
st.error(SHARED_FACILITY_TEXT)

filtered = [b for b in bread_data if not any(a in b["allergens"] for a in avoid)]
st.markdown(f"**{len(filtered)}** safe items found for your selection.")

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
                    <div class="h-52 overflow-hidden bg-gray-200 relative">
                        <img src="${{encodeURI(baseUrl + bread.img)}}" 
                             style="width: 115%; height: 115%; object-fit: cover; object-position: left top; max-width: none;"
                             onerror="this.src='https://via.placeholder.com/400x300?text=Wait+for+Sync';">
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
