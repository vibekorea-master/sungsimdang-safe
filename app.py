import streamlit as st
import streamlit.components.v1 as components
import json

# 1. Page Config & Session State
st.set_page_config(page_title="Sungsimdang Allergy Safe Guide", layout="wide")

if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

# 2. Key Settings
BLOG_BASE_URL = "https://your-blog.tistory.com" # 실제 티스토리 주소
GITHUB_BASE_URL = "https://raw.githubusercontent.com/dongkeuncho-cmyk/sungsimdang-safe/main/"

# ---------------------------------------------------------
# CASE A: Safety Gate (면책 조항 동의 창)
# ---------------------------------------------------------
if not st.session_state.disclaimer_accepted:
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url('{GITHUB_BASE_URL}images/29. Twigim Soboro.png');
            background-size: cover; background-position: center; background-attachment: fixed;
        }}
        .gate-wrapper {{ display: flex; justify-content: center; align-items: center; padding-top: 50px; }}
        .gate-card {{
            background-color: white; padding: 40px; border-radius: 40px;
            max-width: 600px; width: 90%; text-align: center;
            box-shadow: 0 30px 60px rgba(0,0,0,0.5);
        }}
        .gate-title {{ color: #78350f; font-size: 32px; font-weight: 800; margin-bottom: 15px; }}
        .warning-box {{ 
            background-color: #fef2f2; border: 2px solid #fee2e2; 
            padding: 20px; border-radius: 20px; margin-bottom: 20px;
        }}
        .agreement-text {{ 
            color: #000000 !important; font-weight: 900 !important; 
            font-size: 16px !important; display: block; margin-bottom: 20px;
        }}
        </style>
        <div class="gate-wrapper">
            <div class="gate-card">
                <div class="gate-title">🥖 Safety First</div>
                <p style="color: #4b5563; margin-bottom: 20px;">Welcome to the most accurate guide for Sungsimdang Breads.</p>
                <div class="warning-box">
                    <p style="color: #991b1b; font-weight: 800; margin: 0; font-size: 15px; line-height: 1.6;">
                        LEGAL DISCLAIMER:<br>
                        This guide is for reference ONLY. The user assumes all risks. 
                        Always verify ingredients with staff on-site.
                    </p>
                </div>
                <span class="agreement-text">By clicking the button below, you agree to our terms.</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    _, col_btn, _ = st.columns([1, 1.2, 1])
    with col_btn:
        if st.button("✅ I AGREE & VIEW 29 BREADS", use_container_width=True, type="primary"):
            st.session_state.disclaimer_accepted = True
            st.rerun()

# ---------------------------------------------------------
# CASE B: Main Application (동의 후 진입)
# ---------------------------------------------------------
else:
    # 3. Sidebar: 직관적인 설명 추가
    st.sidebar.title("🚫 Your Allergies")
    st.sidebar.markdown("""
    **How to use:** Select the ingredients you are **allergic to**.  
    Breads containing those items will be **automatically hidden** from the list.
    """)

    all_ingredients = sorted(["Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", "Shellfish (Oyster)", "Tomato"])
    avoid = st.sidebar.multiselect("I am allergic to:", all_ingredients)

    # 4. Full Bread Data (29 Items [cite: 4-157])
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

    # 5. 메인 레이아웃 및 필터 메시지
    st.markdown("<h1 style='text-align: center; color: #78350f;'>🥖 Sungsimdang Safe Guide</h1>", unsafe_allow_html=True)
    st.warning("**🏭 Shared Facility Notice:** All products are manufactured in a facility processing Eggs, Milk, Buckwheat, Peanuts, Soybeans, Wheat, Mackerel, Crab, Shrimp, Pork, Peaches, Tomatoes, Sulfites, Walnuts, Chicken, Beef, Squid, Shellfish, and Pine nuts.")

    filtered = [b for b in bread_data if not any(a in b["allergens"] for a in avoid)]
    
    # 동적 결과 안내 (가독성 보완 핵심 패치)
    if avoid:
        st.success(f"✅ **Safe Results:** Showing **{len(filtered)}** breads WITHOUT: **{', '.join(avoid)}**")
    else:
        st.info(f"ℹ️ Showing all **{len(filtered)}** signature breads. Select allergens in the sidebar to filter.")

    # 6. Bread Grid (Premium HTML/Tailwind)
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
                    <div class="bg-white rounded-[2rem] overflow-hidden border border-orange-100 flex flex-col h-full shadow-lg transform transition hover:-translate-y-2">
                        <div class="h-60 overflow-hidden bg-gray-100 relative">
                            <img src="${{encodeURI(baseUrl + bread.img)}}" 
                                 style="width: 115%; height: 115%; object-fit: cover; object-position: left top; max-width: none;"
                                 onerror="this.src='https://via.placeholder.com/400x300?text=Syncing...';">
                        </div>
                        <div class="p-6 flex flex-col flex-grow text-center">
                            <h3 class="text-md font-bold text-gray-800 leading-tight">${{bread.name}}</h3>
                            <p class="text-[10px] text-orange-700 font-bold mb-2">${{bread.ko}}</p>
                            <span class="text-orange-600 font-bold text-sm mb-3 block">${{bread.price}}W</span>
                            <div class="flex flex-wrap justify-center gap-1 mb-4">
                                ${{bread.allergens.map(a => `<span class="px-2 py-0.5 bg-orange-50 text-orange-600 text-[8px] rounded-full border border-orange-200 font-bold">${{a}}</span>`).join('')}}
                            </div>
                            <p class="text-xs text-gray-500 mb-6 flex-grow italic">"${{bread.desc}}"</p>
                            <a href="${{blogUrl}}" target="_blank" class="block w-full text-center bg-[#78350f] text-white py-3 rounded-2xl text-[10px] font-bold hover:bg-[#92400e] transition-colors shadow-md">Read Review on Blog ↗</a>
                        </div>
                    </div>
                `);
            }});
        </script>
    </div>
    """
    components.html(html_code, height=3000, scrolling=True)
