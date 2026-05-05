import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정 및 세션 상태 관리
st.set_page_config(page_title="Sungsimdang Allergy Safe Guide", layout="wide")

if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

# 2. 주요 설정
BLOG_BASE_URL = "https://your-blog.tistory.com" # 실제 티스토리 주소
GITHUB_BASE_URL = "https://raw.githubusercontent.com/dongkeuncho-cmyk/sungsimdang-safe/main/"

# 3. 제조시설 공지 문구 (Source 2)
SHARED_FACILITY_NOTICE = "This product is manufactured in the same facility as products containing eggs (poultry), milk, buckwheat, peanuts, soybeans, wheat, mackerel, crab, shrimp, pork, peaches, tomatoes, sulfites, walnuts, chicken, beef, squid, shellfish (including oysters, abalone, and mussels), and pine nuts."

# ---------------------------------------------------------
# [GATE] Safety Gate (면책 조항 차단막)
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
            max-width: 600px; margin: 60px auto 20px auto; text-align: center;
            box-shadow: 0 30px 60px rgba(0,0,0,0.6);
        }}
        .warning-box {{ 
            background-color: #fef2f2; border: 2px solid #fee2e2; 
            padding: 20px; border-radius: 20px; margin-bottom: 25px;
        }}
        .agreement-notice {{ 
            color: #000000 !important; font-weight: 900 !important; 
            font-size: 18px !important; display: block; margin-bottom: 25px;
        }}
        header, footer, #MainMenu {{visibility: hidden;}}
        </style>
        <div class="gate-card">
            <h2 style="color: #78350f; font-weight: 800; font-size: 32px;">🥖 Safety First</h2>
            <p style="color: #4b5563; font-size: 16px; margin-bottom: 20px;">
                Read our safety terms to access the <b>Comprehensive Allergy Guide</b> for 29 breads.
            </p>
            <div class="warning-box">
                <p style="color: #991b1b; font-weight: 800; font-size: 15px; line-height: 1.6; margin: 0;">
                    LEGAL DISCLAIMER:<br>
                    This guide is for reference ONLY. The user assumes all risks. 
                    Ingredients may change; always verify with staff on-site.
                </p>
            </div>
            <span class="agreement-notice">By clicking the button below, you agree to our terms.</span>
        </div>
    """, unsafe_allow_html=True)

    _, col_btn, _ = st.columns([1, 1.3, 1])
    with col_btn:
        if st.button("✅ I AGREE & VIEW 29 BREADS", use_container_width=True, type="primary"):
            st.session_state.disclaimer_accepted = True
            st.rerun()

# ---------------------------------------------------------
# [MAIN] Application (동의 후 진입)
# ---------------------------------------------------------
else:
    # 4. 사이드바 필터 및 안내
    st.sidebar.title("🚫 Your Allergies")
    st.sidebar.markdown("**How to use:** Select your allergies. Breads containing those items will be hidden.")
    
    all_ingredients = sorted(["Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", "Shellfish (Oyster)", "Tomato"])
    avoid = st.sidebar.multiselect("I am allergic to:", all_ingredients)

    # 5. 문서 데이터 통합 (Source 4-157)
    bread_data = [
        {"id": 1, "name": "Malami Croquette", "ko": "마라미고로케", "price": "3,000", "origin": "Wheat (USA/AUS), Pork (Domestic), Mala Sauce (China)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"]},
        {"id": 2, "name": "Pain au Chocolat", "ko": "뺑오쇼콜라", "price": "3,000", "origin": "Butter sheet (Netherlands), Wheat (USA), Chocolate (France)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 3, "name": "Mochi-Mochi Milk Bread", "ko": "모찌모찌식빵", "price": "3,500", "origin": "Wheat (USA/CAN), Whole milk powder (Netherlands), Butter (NZ)", "allergens": ["Soybean", "Pork", "Wheat", "Milk"]},
        {"id": 4, "name": "Vegetable Croquette", "ko": "야채고로케", "price": "2,300", "origin": "Wheat (USA/AUS), Onion (Domestic), Sausage (Domestic Chicken/Pork)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]},
        {"id": 5, "name": "Little Echo", "ko": "작은메아리", "price": "3,000", "origin": "Butter sheet (Netherlands), Wheat (USA), Milk (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 6, "name": "Noix Raisin", "ko": "노아레즌", "price": "7,000", "origin": "Organic strong wheat flour (Türkiye), Walnut (USA)", "allergens": ["Wheat", "Sulfites", "Walnut"]},
        {"id": 7, "name": "October Fig", "ko": "시월의무화과", "price": "5,000", "origin": "Organic wheat (Türkiye), Fig (Türkiye)", "allergens": ["Wheat", "Sulfites", "Walnut"]},
        {"id": 8, "name": "Big Match", "ko": "빅매치", "price": "2,300", "origin": "Cream cheese (NZ), Wheat (USA/CAN), Butter (NZ)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 9, "name": "Under the Fig Tree", "ko": "무화과그늘아래", "price": "3,000", "origin": "Organic Wheat (Türkiye), Cream cheese (USA), Fig (Türkiye)", "allergens": ["Wheat", "Sulfites", "Milk", "Walnut"]},
        {"id": 10, "name": "Steak Bread", "ko": "스테이크빵", "price": "2,300", "origin": "Neobiani Pork (Imported), Onion (Domestic), Wheat (USA/CAN)", "allergens": ["Egg", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]},
        {"id": 11, "name": "Sunflower", "ko": "해바라기", "price": "2,000", "origin": "Onion (Domestic), Frankfurt sausage (Domestic), Wheat (USA/CAN)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]},
        {"id": 12, "name": "Soboro Bun", "ko": "소보로", "price": "1,300", "origin": "Wheat (USA/CAN), Cake flour (USA), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Peanut", "Wheat", "Milk"]},
        {"id": 13, "name": "Sweet Red Bean Bun", "ko": "단팥빵", "price": "1,700", "origin": "Red bean (China), Wheat (USA/CAN), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"]},
        {"id": 14, "name": "Cream Cheese White Bun", "ko": "크림치즈화이트번", "price": "3,300", "origin": "Wheat (USA/CAN), Cream cheese (NZ), Milk (Domestic)", "allergens": ["Wheat", "Sulfites", "Milk"]},
        {"id": 15, "name": "Bread Donut", "ko": "빵도넛", "price": "1,700", "origin": "Red bean (China), Wheat (USA/CAN), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 16, "name": "Long Twist", "ko": "키다리트위스트", "price": "3,000", "origin": "Wheat (USA/CAN), Butter (NZ/NLD/AUS), Vegetable oil (Malaysia)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 17, "name": "French Pie", "ko": "후렌치파이", "price": "2,000", "origin": "Wheat (USA/CAN), Raspberry jam (Denmark), Strawberry (Domestic)", "allergens": ["Egg", "Wheat", "Milk"]},
        {"id": 18, "name": "Almond Croissant", "ko": "아몬드크로와상", "price": "3,50
