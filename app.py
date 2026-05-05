import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정 및 세션 상태 초기화 (디자인 및 보안의 기초)
st.set_page_config(page_title="Sungsimdang Allergy Safe Guide", layout="wide")

if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

# 2. 핵심 링크 설정 (티스토리 이탈 방지 전략 적용)
BLOG_BASE_URL = "https://your-blog.tistory.com" # 사용자님의 실제 티스토리 주소
GITHUB_BASE_URL = "https://raw.githubusercontent.com/dongkeuncho-cmyk/sungsimdang-safe/main/"

# 3. 제조시설 공지 문구 (Source 2 완벽 반영) [cite: 2]
SHARED_FACILITY_NOTICE = "This product is manufactured in the same facility as products containing eggs (poultry), milk, buckwheat, peanuts, soybeans, wheat, mackerel, crab, shrimp, pork, peaches, tomatoes, sulfites, walnuts, chicken, beef, squid, shellfish (including oysters, abalone, and mussels), and pine nuts."

# ---------------------------------------------------------
# [GATE] Safety Gate (배경 티저 + 면책 조항 통합 차단막)
# ---------------------------------------------------------
if not st.session_state.disclaimer_accepted:
    # 튀김소보로 배경과 가독성 높은 면책 박스 디자인
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
                Please agree to our terms to access the <b>Comprehensive Allergy Guide</b> for 29 signature breads.
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
# [MAIN] Application (동의 후 진입 - 전체 로직 통합)
# ---------------------------------------------------------
else:
    # 3. 사이드바 필터 및 이용 안내
    st.sidebar.title("🚫 Your Allergies")
    st.sidebar.markdown("""
    **How to use:** Select the ingredients you are **allergic to**.  
    Breads containing those items will be automatically hidden.
    """)
    
    all_ingredients = sorted(["Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", "Shellfish (Oyster)", "Tomato"])
    avoid = st.sidebar.multiselect("I am allergic to:", all_ingredients)

    # 4. 전체 29종 상세 데이터 통합 (Source 4-157 완벽 반영) 
    bread_data = [
        {"id": 1, "name": "Malami Croquette", "ko": "마라미고로케", "price": "3,000", "origin": "Wheat (USA/AUS), Pork (Domestic), Mala Sauce (China)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"]},
        {"id": 2, "name": "Pain au Chocolat", "ko": "뺑오쇼콜라", "price": "3,000", "origin": "Butter sheet (Netherlands), Wheat (USA), Chocolate (France)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 3, "name": "Mochi-Mochi Milk Bread", "ko": "모찌모찌식빵", "price": "3,500", "origin": "Wheat (USA/CAN), Milk powder (Netherlands), Butter (NZ)", "allergens": ["Soybean", "Pork", "Wheat", "Milk"]},
        {"id": 4, "name": "Vegetable Croquette", "ko": "야채고로케", "price": "2,300", "origin": "Wheat (USA/AUS), Onion (Domestic), Sausage (Chicken/Pork)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]},
        {"id": 5, "name": "Little Echo", "ko": "작은메아리", "price": "3,000", "origin": "Butter sheet (Netherlands), Wheat (USA), Milk (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 6, "name": "Noix Raisin", "ko": "노아레즌", "price": "7,000", "origin": "Organic wheat flour (Türkiye), Walnut (USA)", "allergens": ["Wheat", "Sulfites", "Walnut"]},
        {"id": 7, "name": "October Fig", "ko": "시월의무화과", "price": "5,000", "origin": "Organic wheat (Türkiye), Fig (Türkiye)", "allergens": ["Wheat", "Sulfites", "Walnut"]},
        {"id": 8, "name": "Big Match", "ko": "빅매치", "price": "2,300", "origin": "Cream cheese (NZ), Wheat (USA/CAN), Butter (NZ)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 9, "name": "Under the Fig Tree", "ko": "무화과그늘아래", "price": "3,000", "origin": "Organic Wheat (Türkiye), Cream cheese (USA), Fig (Türkiye)", "allergens": ["Wheat", "Sulfites", "Milk", "Walnut"]},
        {"id": 10, "name": "Steak Bread", "ko": "스테이크빵", "price": "2,300", "origin": "Pork (Imported), Onion (China), Wheat (USA/CAN)", "allergens": ["Egg", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]},
        {"id": 11, "name": "Sunflower", "ko": "해바라기", "price": "2,000", "origin": "Onion (Domestic), Frankfurt sausage (Chicken/Pork), Wheat (USA/CAN)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]},
        {"id": 12, "name": "Soboro Bun", "ko": "소보로", "price": "1,300", "origin": "Wheat (USA/CAN), Cake flour (USA), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Peanut", "Wheat", "Milk"]},
        {"id": 13, "name": "Sweet Red Bean Bun", "ko": "단팥빵", "price": "1,700", "origin": "Red bean (China), Wheat (USA/CAN), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"]},
        {"id": 14, "name": "Cream Cheese White Bun", "ko": "크림치즈화이트번", "price": "3,300", "origin": "Wheat (USA/CAN), Cream cheese (NZ), Milk (Domestic)", "allergens": ["Wheat", "Sulfites", "Milk"]},
        {"id": 15, "name": "Bread Donut", "ko": "빵도넛", "price": "1,700", "origin": "Red bean (China), Wheat (USA/CAN), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 16, "name": "Long Twist", "ko": "키다리트위스트", "price": "3,000", "origin": "Wheat (USA/CAN), Butter (NZ/NLD/AUS), Vegetable oil (Malaysia)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 17, "name": "French Pie", "ko": "후렌치파이", "price": "2,000", "origin": "Wheat (USA/CAN), Raspberry jam (Denmark), Strawberry (Domestic)", "allergens": ["Egg", "Wheat", "Milk"]},
        {"id": 18, "name": "Almond Croissant", "ko": "아몬드크로와상", "price": "3,500", "origin": "Butter (France), Wheat (USA/CAN), Almond (USA)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 19, "name": "Stone-Ground Whole Wheat Bread", "ko": "맷돌로갈은통밀빵", "price": "4,500", "origin": "Organic wheat (Türkiye), Whole wheat (Domestic), Walnut (USA)", "allergens": ["Wheat", "Walnut"]},
        {"id": 20, "name": "Squid Ink Baton", "ko": "오징어먹물방망이", "price": "3,300", "origin": "Wheat (USA/CAN), Butter (NZ), Milk (Domestic), Squid ink (Spain)", "allergens": ["Egg", "Pork", "Wheat", "Squid", "Milk"]},
        {"id": 21, "name": "Red Wine Bread", "ko": "레드와인", "price": "4,500", "origin": "Organic wheat (Türkiye), Wine (Spain), Rye (Germany)", "allergens": ["Wheat", "Sulfites", "Walnut"]},
        {"id": 22, "name": "Walnut Bread", "ko": "월넛브레드", "price": "4,000", "origin": "Wheat (USA/CAN), Walnut (USA), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"]},
        {"id": 23, "name": "Toyo Bread", "ko": "토요빵", "price": "3,800", "origin": "Wheat (USA/CAN), Milk (Domestic), Cream cheese (NZ), Sweet potato (Domestic)", "allergens": ["Soybean", "Wheat", "Beef", "Milk"]},
        {"id": 24, "name": "Plain Croissant", "ko": "플레인크로와상", "price": "2,800", "origin": "Butter sheet (France), Wheat (USA/CAN), Milk (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 25, "name": "Bomunsan Echo", "ko": "보문산메아리", "price": "6,000", "origin": "Wheat (USA/CAN), Butter sheet (France), Milk (Domestic), Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 26, "name": "Pie Manju Set", "ko": "파이만주세트", "price": "9,600", "origin": "Red bean (China), Wheat (USA/CAN), Almond powder (USA)", "allergens": ["Egg", "Soybean", "Wheat", "Milk", "Walnut"]},
        {"id": 27, "name": "Pantaloon Chive Bread", "ko": "판타롱부추빵", "price": "2,000", "origin": "Chives (Domestic), Wheat (USA/CAN), Egg (Domestic)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)"]},
        {"id": 28, "name": "Twiso-guma", "ko": "튀소구마", "price": "1,700", "origin": "Sweet potato (Domestic), Wheat (USA/CAN), Milk powder (Imported)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"]},
        {"id": 29, "name": "Twigim Soboro", "ko": "튀김소보로", "price": "1,700", "origin": "Red bean paste (China), Wheat (USA/CAN), Milk powder (Imported)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"]}
    ]

    # 5. 메인 레이아웃 및 동적 알림 기능
    st.markdown("<h1 style='text-align: center; color: #78350f;'>🥖 Sungsimdang Safe Guide</h1>", unsafe_allow_html=True)
    st.warning(f"**🏭 Shared Facility Notice:** {SHARED_FACILITY_NOTICE}")

    filtered = [b for b in bread_data if not any(a in b["allergens"] for a in avoid)]
    
    # 실시간 필터 상태 메시지 (직관성 강화)
    if avoid:
        st.success(f"✅ **Safe Guide:** Showing **{len(filtered)}** items without: **{', '.join(avoid)}**")
    else:
        st.info(f"ℹ️ Showing all **{len(filtered)}** items. Use the sidebar to filter allergens.")

    # 6. 프리미엄 카드 그리드 (데이터 100% 반영 및 이미지 크롭)  [cite: 4-157, 164-320]
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
                            <img src="${{encodeURI(baseUrl + 'images/' + bread.id + '. ' + bread.name + '.png')}}" 
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
                            <div class="bg-gray-50 p-3 rounded-xl mb-6 text-left">
                                <p class="text-[8px] text-gray-400 font-bold uppercase mb-1">Detailed Origin Info:</p>
                                <p class="text-[10px] text-gray-600 leading-snug">${{bread.origin}}</p>
                            </div>
                            <button onclick="window.open('${{blogUrl}}', '_blank')" 
                               class="block w-full text-center bg-[#78350f] text-white py-3 rounded-2xl text-[9px] font-bold hover:bg-[#92400e] transition-colors shadow-md uppercase">
                               Sungsimdang Bread Allergy Comprehensive Guide ↗
                            </button>
                        </div>
                    </div>
                `);
            }});
        </script>
    </div>
    """
    st.components.v1.html(html_code, height=3000, scrolling=True)

    # 7. 하단 상세 데이터 시트 (체류 시간 극대화 장치) 
    st.markdown("---")
    st.markdown("### 📊 Comprehensive Bread Data Sheet (Full 29 Items)")
    st.caption("Detailed origin and allergen breakdown based on official English documentation.")
    st.table([{"ID": b["id"], "Name": f"{b['name']} ({b['ko']})", "Origin": b["origin"], "Allergens": ", ".join(b["allergens"])} for b in bread_data])
