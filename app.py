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

# 4. Sidebar: Fixed Notice & Filter
st.sidebar.header("🛡️ Safety First")
st.sidebar.info(SHARED_FACILITY_TEXT) # 사이드바 상단 고정 안내
st.sidebar.markdown("---")

st.sidebar.title("🚫 Filter Ingredients")
all_ingredients = sorted([
    "Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", 
    "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", 
    "Shellfish (Oyster)", "Tomato"
])
avoid = st.sidebar.multiselect("Hide breads containing:", all_ingredients)

# 5. Bread Data (Full 29 items)
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
    {"id": 11, "name": "Sunflower", "price": "2,000", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk",
