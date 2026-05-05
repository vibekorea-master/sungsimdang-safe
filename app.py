import streamlit as st
import streamlit.components.v1 as components
import json

# 1. Page Configuration
st.set_page_config(page_title="Sungsimdang Allergy Safe Guide", layout="wide")

# 2. Complete Bread Database (Data from PDF )
# Filenames follow the pattern: "Number. English Name.png"
bread_data = [
    {"id": 1, "name": "Marami Croquette", "price": "3,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"], "img": "images/1. Marami Croquette.png", "desc": "Spicy Marasanguo sauce with minced pork."},
    {"id": 2, "name": "Pain au Chocolat", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/2. Pain au Chocolat.png", "desc": "Crispy pastry with French chocolate sticks."},
    {"id": 3, "name": "Mochi Mochi Bread", "price": "3,500", "allergens": ["Soybean", "Pork", "Wheat", "Milk"], "img": "images/3. Mochi Mochi Bread.png", "desc": "Chewy texture made with whole milk powder."},
    {"id": 4, "name": "Vegetable Croquette", "price": "2,300", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish", "Tomato"], "img": "images/4. Vegetable Croquette.png", "desc": "Fresh onions and sausages in a crunchy shell."},
    {"id": 5, "name": "Little Echo", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/5. Little Echo.png", "desc": "Mini version of the famous Bomunsan Echo."},
    {"id": 6, "name": "Noix Raisin", "price": "7,000", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/6. Noix Raisin.png", "desc": "Healthy rye bread with walnuts and raisins."},
    {"id": 7, "name": "October Fig", "price": "5,000", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/7. October Fig.png", "desc": "Seasonal fig bread with organic flour."},
    {"id": 8, "name": "Big Match", "price": "2,300", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/8. Big Match.png", "desc": "Sweet biscuit bread filled with cream cheese."},
    {"id": 9, "name": "Under the Fig Shade", "price": "3,000", "allergens": ["Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/9. Under the Fig Shade.png", "desc": "Wholesome bread with figs and cream cheese."},
    {"id": 10, "name": "Steak Bread", "price": "2,300", "allergens": ["Egg", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish", "Tomato"], "img": "images/10. Steak Bread.png", "desc": "Savory bread filled with Neobiwani steak."},
    {"id": 11, "name": "Sunflower", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish", "Tomato"], "img": "images/11. Sunflower.png", "desc": "Unique shape with frank sausage and onions."},
    {"id": 12, "name": "Soboro (Streusel Bread)", "price": "1,300", "allergens": ["Egg", "Soybean", "Peanut", "Wheat", "Milk"], "img": "images/12. Soboro (Streusel Bread).png", "desc": "Classic crunchy peanut butter streusel."},
    {"id": 13, "name": "Sweet Red Bean Bread", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/13. Sweet Red Bean Bread.png", "desc": "Traditional bread with sweet red bean paste."},
    {"id": 14, "name": "Cream Cheese White Bun", "price": "3,300", "allergens": ["Wheat", "Sulfites", "Milk"], "img": "images/14. Cream Cheese White Bun.png", "desc": "Soft white bun filled with rich cream cheese."},
    {"id": 15, "name": "Bread Donut", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/15. Bread Donut.png", "desc": "Deliciously fried donut with red bean filling."},
    {"id": 16, "name": "Long Twist", "price": "3,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/16. Long Twist.png", "desc": "Large twisted bread with a buttery aroma."},
    {"id": 17, "name": "French Pie", "price": "2,000", "allergens": ["Egg", "Wheat", "Milk"], "img": "images/17. French Pie.png", "desc": "Flaky pie with strawberry and raspberry jam."},
    {"id": 18, "name": "Almond Croissant", "price": "3,500", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/18. Almond Croissant.png", "desc": "Buttery croissant topped with sliced almonds."},
    {"id": 19, "name": "Stone-ground Whole Wheat", "price": "4,500", "allergens": ["Wheat", "Walnut"], "img": "images/19. Stone-ground Whole Wheat Bread.png", "desc": "Nutritious stone-ground whole wheat and walnuts."},
    {"id": 20, "name": "Squid Ink Bat", "price": "3,300", "allergens": ["Egg", "Pork", "Wheat", "Squid", "Milk"], "img": "images/20. Squid Ink Bat.png", "desc": "Squid ink bread with condensed milk cream."},
    {"id": 21, "name": "Red Wine", "price": "4,500", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/21. Red Wine.png", "desc": "Aromatic bread made with red wine and rye."},
    {"id": 22, "name": "Walnut Bread", "price": "4,000", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/22. Walnut Bread.png", "desc": "Hearty bread packed with walnuts."},
    {"id": 23, "name": "Toyo-ppang (Saturday Bread)", "price": "3,800", "allergens": ["Soybean", "Wheat", "Beef", "Milk"], "img": "images/23. Toyo-ppang (Saturday Bread).png", "desc": "Sweet potato and cream cheese filling."},
    {"id": 24, "name": "Plain Croissant", "price": "2,800", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/24. Plain Croissant.png", "desc": "Classic French-style buttery croissant."},
    {"id": 25, "name": "Bomunsan Echo", "price": "6,000", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/25. Bomunsan Echo.png", "desc": "Sungsimdang's signature layered pastry."},
    {"id": 26, "name": "Pie Manju Set", "price": "9,600", "allergens": ["Egg", "Soybean", "Wheat", "Milk", "Walnut"], "img": "images/26. Pie Manju Set (8ea).png", "desc": "Gift set of sweet red bean pie manjus."},
    {"id": 27, "name": "Pantaloon Chive Bread", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish"], "img": "images/27. Pantaloon Chive Bread.png", "desc": "Unique bread filled with fresh chives and eggs."},
    {"id": 28, "name": "Twisoguma", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/28. Twisoguma.png", "desc": "Fried streusel bread with sweet potato filling."},
    {"id": 29, "name": "Twigim Soboro", "price": "1,700", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/29. Twigim Soboro.png", "desc": "The legendary fried red bean streusel bread."}
]

# 3. Sidebar - Allergy Filter
st.sidebar.title("🚫 Allergy Guide")
all_allergens = sorted(["Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", "Shellfish", "Tomato"])
selected_allergies = st.sidebar.multiselect("Select ingredients to AVOID:", all_allergens)

# Filtering Logic
filtered_data = [b for b in bread_data if not any(a in b["allergens"] for a in selected_allergies)]

# 4. Main UI
st.title("🥖 Sungsimdang Safe Hall of Fame")
st.markdown(f"Found **{len(filtered_data)}** safe items for you.")

# 5. HTML/CSS Component with "Auto-Crop" logic
# Using 'object-cover' and 'scale-110' for zooming in on the center
bread_json = json.dumps(filtered_data)
html_code = f"""
<script src="https://cdn.tailwindcss.com"></script>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 p-4 bg-orange-50">
    <script>
        const data = {bread_json};
        data.forEach(bread => {{
            document.write(`
                <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-orange-100 flex flex-col h-full transform transition hover:scale-105">
                    <div class="h-52 overflow-hidden bg-gray-200">
                        <img src="${{bread.img}}" class="w-full h-full object-cover transform scale-110" 
                             onerror="this.src='https://via.placeholder.com/400x300?text=Check+Filename';">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <div class="flex justify-between items-start mb-2">
                            <h3 class="text-lg font-bold text-gray-800">${{bread.name}}</h3>
                            <span class="text-orange-600 font-bold text-sm">${{bread.price}} W</span>
                        </div>
                        <p class="text-[10px] text-gray-400 mb-2 leading-tight">Allergens: ${{bread.allergens.join(', ')}}</p>
                        <p class="text-xs text-gray-600 mb-4 flex-grow">${{bread.desc}}</p>
                        <div class="text-center bg-orange-500 text-white py-2 rounded-lg text-xs font-bold">
                            Allergy Safe ✅
                        </div>
                    </div>
                </div>
            `);
        }});
    </script>
</div>
"""


components.html(html_code, height=2500, scrolling=True)
