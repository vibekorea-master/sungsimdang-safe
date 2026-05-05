import streamlit as st
import streamlit.components.v1 as components
import json

# 1. Page Config & Session State
st.set_page_config(page_title="Sungsimdang Allergy Safe Guide", layout="wide")

if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

# 2. Key Settings
BLOG_BASE_URL = "https://your-blog.tistory.com" 
GITHUB_BASE_URL = "https://raw.githubusercontent.com/dongkeuncho-cmyk/sungsimdang-safe/main/"

# 3. Shared Facility Notice (Source: 2) 
FACILITY_NOTICE = "This product is manufactured in the same facility as products containing eggs (poultry), milk, buckwheat, peanuts, soybeans, wheat, mackerel, crab, shrimp, pork, peaches, tomatoes, sulfites, walnuts, chicken, beef, squid, shellfish (including oysters, abalone, and mussels), and pine nuts."

# ---------------------------------------------------------
# [GATE] Safety Disclaimer (면책 조항 차단막)
# ---------------------------------------------------------
if not st.session_state.disclaimer_accepted:
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url('{GITHUB_BASE_URL}images/29. Twigim Soboro.png');
            background-size: cover; background-position: center; background-attachment: fixed;
        }}
        .gate-card {{
            background-color: white; padding: 40px; border-radius: 40px;
            max-width: 600px; margin: 80px auto 20px auto; text-align: center;
            box-shadow: 0 30px 60px rgba(0,0,0,0.6);
        }}
        .warning-box {{ 
            background-color: #fef2f2; border: 2px solid #fee2e2; 
            padding: 20px; border-radius: 20px; margin-bottom: 25px;
        }}
        .agreement-notice {{ 
            color: #000000 !important; font-weight: 900 !important; 
            font-size: 16px !important; display: block; margin-bottom: 20px;
        }}
        </style>
        <div class="gate-card">
            <h2 style="color: #78350f; font-weight: 800;">🥖 Safety First</h2>
            <p style="color: #4b5563; font-size: 15px; margin-bottom: 20px;">
                Please read our safety terms to access the full guide of 29 breads.
            </p>
            <div class="warning-box">
                <p style="color: #991b1b; font-weight: 800; font-size: 14px; line-height: 1.6; margin: 0;">
                    LEGAL DISCLAIMER:<br>
                    This guide is for reference ONLY. The user assumes all risks. 
                    Ingredients may change; always verify with staff on-site.
                </p>
            </div>
            <span class="agreement-notice">By clicking the button below, you agree to our terms.</span>
        </div>
    """, unsafe_allow_html=True)

    _, col_btn, _ = st.columns([1, 1.2, 1])
    with col_btn:
        if st.button("✅ I AGREE & ENTER GUIDE", use_container_width=True, type="primary"):
            st.session_state.disclaimer_accepted = True
            st.rerun()

# ---------------------------------------------------------
# [MAIN] Application (동의 후 진입)
# ---------------------------------------------------------
else:
    # 4. Sidebar: Filter & Tutorial
    st.sidebar.title("🚫 Your Allergies")
    st.sidebar.markdown("""
    **How to use:** Select the ingredients you are **allergic to**.  
    Breads containing those items will be hidden. [cite: 4-157]
    """)
    
    # List based on Source 2 
    all_ingredients = sorted(["Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", "Shellfish (Oyster)", "Tomato"])
    avoid = st.sidebar.multiselect("I am allergic to:", all_ingredients)

    # 5. Full Data (Source: 4-157) [cite: 4-157]
    bread_data = [
        {"id": 1, "name": "Malami Croquette", "ko": "마라미고로케", "price": "3,000", "origin": "Wheat (USA/AUS), Pork (Domestic), Mala Sauce (China)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"], "img": "images/1. Malami Croquette.png"},
        {"id": 2, "name": "Pain au Chocolat", "ko": "뺑오쇼콜라", "price": "3,000", "origin": "Butter (Netherlands), Wheat (USA), Chocolate (France)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/2. Pain au Chocolat.png"},
        {"id": 3, "name": "Mochi-Mochi Milk Bread", "ko": "모찌모찌식빵", "price": "3,500", "origin": "Wheat (USA/CAN), Milk Powder (Netherlands), Butter (NZ)", "allergens": ["Soybean", "Pork", "Wheat", "Milk"], "img": "images/3. Mochi-Mochi Milk Bread.png"},
        {"id": 4, "name": "Vegetable Croquette", "ko": "야채고로케", "price": "2,300", "origin": "Wheat (USA/AUS), Onion (Domestic), Sausage (Domestic)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/4. Vegetable Croquette.png"},
        {"id": 5, "name": "Little Echo", "ko": "작은메아리", "price": "3,000", "origin": "Butter (Netherlands), Wheat (USA), Milk (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/5. Little Echo.png"},
        {"id": 6, "name": "Noix Raisin", "ko": "노아레즌", "price": "7,000", "origin": "Organic Wheat (Türkiye), Walnut (USA)", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/6. Noix Raisin.png"},
        {"id": 7, "name": "October Fig", "ko": "시월의무화과", "price": "5,000", "origin": "Organic Wheat (Türkiye), Fig (Türkiye)", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/7. October Fig.png"},
        {"id": 8, "name": "Big Match", "ko": "빅매치", "price": "2,300", "origin": "Cream Cheese (NZ), Wheat (USA/CAN), Butter (NZ)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/8. Big Match.png"},
        {"id": 9, "name": "Under the Fig Tree", "ko": "무화과그늘아래", "price": "3,000", "origin": "Organic Wheat (Türkiye), Cream Cheese (USA), Fig (Türkiye)", "allergens": ["Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/9. Under the Fig Tree.png"},
        {"id": 10, "name": "Steak Bread", "ko": "스테이크빵", "price": "2,300", "origin": "Pork (USA/ESP/CAN), Onion (Domestic), Wheat (USA/CAN)", "allergens": ["Egg", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/10. Steak Bread.png"},
        {"id": 11, "name": "Sunflower", "ko": "해바라기", "price": "2,000", "origin": "Onion (Domestic), Sausage (Domestic), Wheat (USA/CAN)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"], "img": "images/11. Sunflower.png"},
        {"id": 12, "name": "Soboro Bun", "ko": "소보로", "price": "1,300", "origin": "Wheat (USA/CAN), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Peanut", "Wheat", "Milk"], "img": "images/12. Soboro Bun.png"},
        {"id": 13, "name": "Sweet Red Bean Bun", "ko": "단팥빵", "price": "1,700", "origin": "Red Bean (China), Wheat (USA/CAN), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/13. Sweet Red Bean Bun.png"},
        {"id": 14, "name": "Cream Cheese White Bun", "ko": "크림치즈화이트번", "price": "3,300", "origin": "Wheat (USA/CAN), Cream Cheese (NZ), Milk (Domestic)", "allergens": ["Wheat", "Sulfites", "Milk"], "img": "images/14. Cream Cheese White Bun.png"},
        {"id": 15, "name": "Bread Donut", "ko": "빵도넛", "price": "1,700", "origin": "Red Bean (China), Wheat (USA/CAN), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/15. Bread Donut.png"},
        {"id": 16, "name": "Long Twist", "ko": "키다리트위스트", "price": "3,000", "origin": "Wheat (USA/CAN), Butter (NZ/NLD/AUS)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/16. Long Twist.png"},
        {"id": 17, "name": "French Pie", "ko": "후렌치파이", "price": "2,000", "origin": "Wheat (USA/CAN), Raspberry Jam (Denmark), Strawberry (Domestic)", "allergens": ["Egg", "Wheat", "Milk"], "img": "images/17. French Pie.png"},
        {"id": 18, "name": "Almond Croissant", "ko": "아몬드크로와상", "price": "3,500", "origin": "Butter (France), Wheat (USA/CAN), Almond (USA)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/18. Almond Croissant.png"},
        {"id": 19, "name": "Stone-Ground Whole Wheat Bread", "ko": "맷돌로갈은통밀빵", "price": "4,500", "origin": "Organic Wheat (Türkiye), Whole Wheat (Domestic), Walnut (USA)", "allergens": ["Wheat", "Walnut"], "img": "images/19. Stone-Ground Whole Wheat Bread.png"},
        {"id": 20, "name": "Squid Ink Baton", "ko": "오징어먹물방망이", "price": "3,300", "origin": "Wheat (USA/CAN), Butter (NZ), Milk (Domestic), Squid Ink (Spain)", "allergens": ["Egg", "Pork", "Wheat", "Squid", "Milk"], "img": "images/20. Squid Ink Baton.png"},
        {"id": 21, "name": "Red Wine Bread", "ko": "레드와인", "price": "4,500", "origin": "Organic Wheat (Türkiye), Wine (Spain), Rye (Germany)", "allergens": ["Wheat", "Sulfites", "Walnut"], "img": "images/21. Red Wine Bread.png"},
        {"id": 22, "name": "Walnut Bread", "ko": "월넛브레드", "price": "4,000", "origin": "Wheat (USA/CAN), Walnut (USA), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"], "img": "images/22. Walnut Bread.png"},
        {"id": 23, "name": "Toyo Bread", "ko": "토요빵", "price": "3,800", "origin": "Wheat (USA/CAN), Milk (Domestic), Cream Cheese (NZ), Sweet Potato (Domestic)", "allergens": ["Soybean", "Wheat", "Beef", "Milk"], "img": "images/23. Toyo Bread.png"},
        {"id": 24, "name": "Plain Croissant", "ko": "플레인크로와상", "price": "2,800", "origin": "Butter (France), Wheat (USA/CAN), Milk (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/24. Plain Croissant.png"},
        {"id": 25, "name": "Bomunsan Echo", "ko": "보문산메아리", "price": "6,000", "origin": "Wheat (USA/CAN), Butter (France), Milk (Domestic), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"], "img": "images/25. Bomunsan Echo.png"},
        {"id": 26, "name": "Pie Manju Set", "ko": "파이만주세트", "price": "9,600", "origin": "Red Bean (China), Wheat (USA/CAN), Almond (USA)", "allergens": ["Egg", "Soybean", "Wheat", "Milk", "Walnut"], "img": "images/26. Pie Manju Set.png"},
        {"id": 27, "name": "Pantaloon Chive Bread", "ko": "판타롱부추빵", "price": "2,000", "origin": "Chives (Domestic), Wheat (USA/CAN), Egg (Domestic)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)"], "img": "images/27. Pantaloon Chive Bread.png"},
        {"id": 28, "name": "Twiso-guma", "ko": "튀소구마", "price": "1,700", "origin": "Sweet Potato (Domestic), Wheat (USA/CAN), Milk Powder (Imported)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/28. Twiso-guma.png"},
        {"id": 29, "name": "Twigim Soboro", "ko": "튀김소보로", "price": "1,700", "origin": "Red Bean (China), Wheat (USA/CAN), Milk Powder (Imported)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"], "img": "images/29. Twigim Soboro.png"}
    ]

    st.markdown("<h1 style='text-align: center; color: #78350f;'>🥖 Sungsimdang Safe Guide</h1>", unsafe_allow_html=True)
    st.warning(f"**🏭 Shared Facility Notice:** {FACILITY_NOTICE}") # [cite: 2, 3]

    filtered = [b for b in bread_data if not any(a in b["allergens"] for a in avoid)]
    
    # 실시간 결과 안내
    if avoid:
        st.success(f"✅ **Safe Guide:** Showing **{len(filtered)}** items without: **{', '.join(avoid)}**")
    else:
        st.info(f"ℹ️ Showing all **{len(filtered)}** items. Please use the sidebar to filter allergens.")

    # 6. Bread Grid Rendering (Data from Source 1-157) 
    bread_json = json.dumps(filtered)
    html_code = f"""
    <script src="https://cdn.tailwindcss.com"></script>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 p-4 bg-orange-50">
        <script>
            const data = {bread_json};
            const baseUrl = "{GITHUB_BASE_URL}";
            const blogUrl = "{BLOG_BASE_URL}";
            data.forEach(bread => {{
                document.write(`
                    <div class="bg-white rounded-[2rem] overflow-hidden border border-orange-100 flex flex-col h-full shadow-lg">
                        <div class="h-60 overflow-hidden bg-gray-100 relative">
                            <img src="${{encodeURI(baseUrl + bread.img)}}" 
                                 style="width: 115%; height: 115%; object-fit: cover; object-position: left top; max-width: none;">
                        </div>
                        <div class="p-6 flex flex-col flex-grow text-center">
                            <h3 class="text-md font-bold text-gray-800 leading-tight">${{bread.name}}</h3>
                            <p class="text-[10px] text-orange-700 font-bold mb-2">${{bread.ko}}</p>
                            <span class="text-orange-600 font-bold text-sm mb-3 block">${{bread.price}}W</span>
                            <div class="flex flex-wrap justify-center gap-1 mb-4">
                                ${{bread.allergens.map(a => `<span class="px-2 py-0.5 bg-orange-50 text-orange-600 text-[8px] rounded-full border border-orange-200 font-bold">${{a}}</span>`).join('')}}
                            </div>
                            <div class="bg-gray-50 p-3 rounded-xl mb-6 text-left">
                                <p class="text-[9px] text-gray-400 font-bold uppercase mb-1">Origin:</p>
                                <p class="text-[10px] text-gray-600 leading-snug">${{bread.origin}}</p>
                            </div>
                            <a href="${{blogUrl}}" target="_blank" 
                               class="block w-full text-center bg-[#9ca3af] text-white py-3 rounded-2xl text-[10px] font-bold hover:bg-gray-500 transition-colors shadow-md">
                               Review Coming Soon... ↗
                            </a>
                        </div>
                    </div>
                `);
            }});
        </script>
    </div>
    """
    components.html(html_code, height=3000, scrolling=True)
