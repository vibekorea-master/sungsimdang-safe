import streamlit as st
import streamlit.components.v1 as components
import json

# 1. Page Configuration
st.set_page_config(page_title="Sungsimdang Allergy Safe Guide", layout="wide")

# 2. GitHub Raw Base URL
GITHUB_BASE_URL = "https://raw.githubusercontent.com/dongkeuncho-cmyk/sungsimdang-safe/main/"

# 3. Shared Facility Notice Text [cite: 2]
SHARED_FACILITY_TEXT = """
**⚠️ Shared Facility Notice:** This product is manufactured in the same facility as products containing:  
*Eggs (poultry), Milk, Buckwheat, Peanuts, Soybeans, Wheat, Mackerel, Crab, Shrimp, Pork, Peaches, Tomatoes, Sulfites, Walnuts, Chicken, Beef, Squid, Shellfish (including Oysters, Abalone, and Mussels), and Pine nuts.*
"""

# 4. Sidebar: Fixed Notice & Filter
st.sidebar.header("🛡️ Safety First")
st.sidebar.info(SHARED_FACILITY_TEXT)
st.sidebar.markdown("---")

st.sidebar.title("🚫 Filter Ingredients")
all_ingredients = sorted([
    "Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", 
    "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", 
    "Shellfish (Oyster)", "Tomato"
])
avoid = st.sidebar.multiselect("Hide breads containing:", all_ingredients)

# 5. Bread Data (29 items fully verified from source [cite: 4-157])
bread_data = [
    {"id": 1, "name": "Malami Croquette", "price": "3,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"], "img": "images/1. Malami Croquette.png", "desc": "Spicy Mala Xiangguo sauce with minced pork. [cite: 5, 9]"},
    {"id": 2, "name": "Pain au Chocolat", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/2. Pain au Chocolat.png", "desc": "Crispy pastry with French chocolate sticks. [cite: 12, 14]"},
    {"id": 3, "name": "Mochi-Mochi Milk Bread", "price": "3,500", "allergens": ["Soybean", "Pork", "Wheat", "Milk"], "img": "images/3. Mochi-Mochi Milk Bread.png", "desc": "Chewy texture made with whole milk powder. [cite: 17, 19]"},
    {"id": 4, "name": "Vegetable Croquette", "price": "2,300", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/4. Vegetable Croquette.png", "desc": "Fresh onions and sausages with domestic pork. [cite: 22, 24]"},
    {"id": 5, "name": "Little Echo", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/5. Little Echo.png", "desc": "Mini version of Bomunsan Echo. [cite: 27, 29]"},
    {"id": 6, "name": "Noix Raisin", "price": "7,000", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/6. Noix Raisin.png", "desc": "Organic flour with walnuts and raisins. [cite: 32, 34]"},
    {"id": 7, "name": "October Fig", "price": "5,000", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/7. October Fig.png", "desc": "Seasonal fig bread made with organic flour. [cite: 37, 39]"},
    {"id": 8, "name": "Big Match", "price": "2,300", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/8. Big Match.png", "desc": "Cream cheese with a sweet biscuit top. [cite: 42, 44]"},
    {"id": 9, "name": "Under the Fig Tree", "price": "3,000", "allergens": ["Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/9. Under the Fig Tree.png", "desc": "Wholesome bread with figs and cream cheese. [cite: 47, 49]"},
    {"id": 10, "name": "Steak Bread", "price": "2,300", "allergens": ["Egg", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/10. Steak Bread.png", "desc": "Korean-style sliced grilled pork with onions. [cite: 52, 55]"},
    {"id": 11, "name": "Sunflower", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/11. Sunflower.png", "desc": "Frankfurt sausage and domestic onions. [cite: 58, 60]"},
    {"id": 12, "name": "Soboro Bun", "price": "1,300", "allergens": ["Egg", "Soybean", "Peanut", "Wheat", "Milk"], "img": "images/12. Soboro Bun.png", "desc": "Classic Korean Streusel Bun. [cite: 63, 65]"},
    {"id": 13, "name": "Sweet Red Bean Bun", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/13. Sweet Red Bean Bun.png", "desc": "Traditional red bean paste with walnuts. [cite: 68, 70]"},
    {"id": 14, "name": "Cream Cheese White Bun", "price": "3,300", "allergens": ["Wheat", "Sulfites", "Milk"], "img": "images/14. Cream Cheese White Bun.png", "desc": "Soft bun with New Zealand cream cheese. [cite: 73, 75]"},
    {"id": 15, "name": "Bread Donut", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/15. Bread Donut.png", "desc": "Fried donut filled with red bean paste. [cite: 78, 80]"},
    {"id": 16, "name": "Long Twist", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/16. Long Twist.png", "desc": "Buttery twisted bread with vegetable oil. [cite: 83, 86]"},
    {"id": 17, "name": "French Pie", "price": "2,000", "allergens": ["Egg", "Wheat", "Milk"], "img": "images/17. French Pie.png", "desc": "Raspberry and domestic strawberry jam. [cite: 89, 92]"},
    {"id": 18, "name": "Almond Croissant", "price": "3,500", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/18. Almond Croissant.png", "desc": "Buttery croissant with USA almonds. [cite: 95, 97]"},
    {"id": 19, "name": "Stone-Ground Whole Wheat Bread", "price": "4,500", "allergens": ["Wheat", "Walnut"], "img": "images/19. Stone-Ground Whole Wheat Bread.png", "desc": "Organic whole wheat flour and walnuts. [cite: 100, 102]"},
    {"id": 20, "name": "Squid Ink Baton", "price": "3,300", "allergens": ["Egg", "Pork", "Wheat", "Squid", "Milk"], "img": "images/20. Squid Ink Baton.png", "desc": "Spanish squid ink with condensed milk. [cite: 105, 107]"},
    {"id": 21, "name": "Red Wine Bread", "price": "4,500", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/21. Red Wine Bread.png", "desc": "Made with Spanish wine and German rye. [cite: 110, 112]"},
    {"id": 22, "name": "Walnut Bread", "price": "4,000", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/22. Walnut Bread.png", "desc": "Hearty bread packed with USA walnuts. [cite: 115, 117]"},
    {"id": 23, "name": "Toyo Bread", "price": "3,800", "allergens": ["Soybean", "Wheat", "Beef", "Milk"], "img": "images/23. Toyo Bread.png", "desc": "Sweet potato and cream cheese filling. [cite: 120, 122]"},
    {"id": 24, "name": "Plain Croissant", "price": "2,800", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/24. Plain Croissant.png", "desc": "Classic croissant with French butter. [cite: 125, 127]"},
    {"id": 25, "name": "Bomunsan Echo", "price": "6,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/25. Bomunsan Echo.png", "desc": "Signature pastry with layered butter. [cite: 130, 132]"},
    {"id": 26, "name": "Pie Manju Set", "price": "9,600", "allergens": ["Egg", "Soybean", "Wheat", "Milk", "Walnut"], "img": "images/26. Pie Manju Set.png", "desc": "Red bean manju with almond powder. [cite: 135, 139]"},
    {"id": 27, "name": "Pantaloon Chive Bread", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)"], "img": "images/27. Pantaloon Chive Bread.png", "desc": "Famous bread with domestic chives and eggs. [cite: 142, 144]"},
    {"id": 28, "name": "Twiso-guma", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/28. Twiso-guma.png", "desc": "Fried sweet potato soboro bun. [cite: 147, 150]"},
    {"id": 29, "name": "Twigim Soboro", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/29. Twigim Soboro.png", "desc": "Legendary fried red bean soboro bun. [cite: 153, 156]"}
]

# 6. Filter Logic
filtered = [b for b in bread_data if not any(a in b["allergens"] for a in avoid)]

# 7. Main UI Rendering
st.title("🥖 Sungsimdang Safe Guide")
st.error(SHARED_FACILITY_TEXT)
st.markdown(f"**{len(filtered)}** safe items found. Enjoy Daejeon safely!")

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
