import streamlit as st
import streamlit.components.v1 as components
import json

# 1. 페이지 설정 및 세션 상태 관리
st.set_page_config(page_title="Sungsimdang Allergy Safe Guide", layout="wide")

if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

# 2. 핵심 설정 (데이터 보존)
GITHUB_BASE_URL = "https://raw.githubusercontent.com/dongkeuncho-cmyk/sungsimdang-safe/main/"
FACILITY_NOTICE = "This product is manufactured in the same facility as products containing eggs (poultry), milk, buckwheat, peanuts, soybeans, wheat, mackerel, crab, shrimp, pork, peaches, tomatoes, sulfites, walnuts, chicken, beef, squid, shellfish (including oysters, abalone, and mussels), and pine nuts." # [cite: 2]

# ---------------------------------------------------------
# [GATE] Safety Gate (면책 조항 차단막 - 티저 배경 유지)
# ---------------------------------------------------------
if not st.session_state.disclaimer_accepted:
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
                        url('{GITHUB_BASE_URL}images/29. Twigim Soboro.png');
            background-size: cover; background-position: center; background-attachment: fixed;
        }}
        .gate-card {{
            background-color: white; padding: 40px; border-radius: 40px;
            max-width: 600px; margin: 80px auto 20px auto; text-align: center;
            box-shadow: 0 30px 60px rgba(0,0,0,0.6);
        }}
        .warning-box {{ background-color: #fef2f2; border: 2px solid #fee2e2; padding: 20px; border-radius: 20px; margin-bottom: 25px; }}
        .agreement-notice {{ color: #000000 !important; font-weight: 900 !important; font-size: 18px !important; display: block; margin-bottom: 25px; }}
        header, footer, #MainMenu {{visibility: hidden;}}
        </style>
        <div class="gate-card">
            <h2 style="color: #78350f; font-weight: 800; font-size: 32px;">🥖 Safety First</h2>
            <p style="color: #4b5563; font-size: 16px; margin-bottom: 20px;">Please agree to our terms to access the <b>Comprehensive Allergy Guide</b>.</p>
            <div class="warning-box">
                <p style="color: #991b1b; font-weight: 800; font-size: 15px; line-height: 1.6; margin: 0;">
                    LEGAL DISCLAIMER: This guide is for reference ONLY. The user assumes all risks. 
                    Always verify with staff on-site.
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
# [MAIN] Application (동의 후 진입 - 모든 정보 복구)
# ---------------------------------------------------------
else:
    # 배경 초기화 (새커먼 화면 방지)
    st.markdown("""<style>.stApp { background-color: #fffaf5 !important; background-image: none !important; } header, footer, #MainMenu {visibility: hidden;}</style>""", unsafe_allow_html=True)

    st.sidebar.title("🚫 Your Allergies")
    all_ingredients = sorted(["Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken", "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites", "Shellfish (Oyster)", "Tomato"])
    avoid = st.sidebar.multiselect("I am allergic to:", all_ingredients)

    # 4. 전체 29종 상세 데이터 무결성 보존 
    bread_data = [
        {"id": 1, "name": "Malami Croquette", "ko": "마라미고로케", "price": "3,000", "origin": "Medium-strength wheat flour (USA / Australia); Minced pork (Pork: Domestic); Mala Xiangguo sauce [Mala Xiangguo sauce base (China; doubanjiang, soybean oil, dried chili, brewed soy sauce, green Sichuan pepper); Pork bone extract (Pork bone: Domestic)]; Classic Malatang sauce (China)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"]},
        {"id": 2, "name": "Pain au Chocolat", "ko": "뺑오쇼콜라", "price": "3,000", "origin": "Butter sheet (Netherlands); Wheat flour (Wheat: USA); Strong wheat flour (USA / Canada); Chocolate stick (France)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 3, "name": "Mochi-Mochi Milk Bread", "ko": "모찌모찌식빵", "price": "3,500", "origin": "Strong wheat flour (USA / Canada); Whole milk powder (Netherlands); Butter (New Zealand)", "allergens": ["Soybean", "Pork", "Wheat", "Milk"]},
        {"id": 4, "name": "Vegetable Croquette", "ko": "야채고로케", "price": "2,300", "origin": "Medium-strength wheat flour (USA / Australia); Onion (Domestic); Sausage [Chicken (Domestic), Pork (Domestic), Pork fat (Domestic)]", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]},
        {"id": 5, "name": "Little Echo", "ko": "작은메아리", "price": "3,000", "origin": "Butter sheet (Netherlands); Wheat flour (Wheat: USA); Strong wheat flour (USA / Canada); Milk (Raw milk: Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 6, "name": "Noix Raisin", "ko": "노아레즌", "price": "7,000", "origin": "Organic strong wheat flour (Türkiye); Walnut (USA); Organic cake flour (Türkiye)", "allergens": ["Wheat", "Sulfites", "Walnut"]},
        {"id": 7, "name": "October Fig", "ko": "시월의무화과", "price": "5,000", "origin": "Organic strong wheat flour (Türkiye); Fig (Türkiye); Strong wheat flour (USA / Canada)", "allergens": ["Wheat", "Sulfites", "Walnut"]},
        {"id": 8, "name": "Big Match", "ko": "빅매치", "price": "2,300", "origin": "Cream cheese (New Zealand); Strong wheat flour (USA / Canada); Butter (New Zealand)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 9, "name": "Under the Fig Tree", "ko": "무화과그늘아래", "price": "3,000", "origin": "Organic strong wheat flour (Türkiye); Cream cheese (USA); Wheat flour (Wheat: Domestic); Fig (Türkiye)", "allergens": ["Wheat", "Sulfites", "Milk", "Walnut"]},
        {"id": 10, "name": "Steak Bread", "ko": "스테이크빵", "price": "2,300", "origin": "Neobiani (Korean-style sliced grilled pork) [Pork: Imported (USA, Spain, Canada, etc.); Green onion (China)]; Onion (Domestic); Strong wheat flour (USA / Canada)", "allergens": ["Egg", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]},
        {"id": 11, "name": "Sunflower", "ko": "해바라기", "price": "2,000", "origin": "Onion (Domestic); Frankfurt sausage [Chicken (Domestic), Pork (Domestic)]; Strong wheat flour (USA / Canada)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]},
        {"id": 12, "name": "Soboro Bun", "ko": "소보로", "price": "1,300", "origin": "Strong wheat flour (USA / Canada); Cake flour (USA); Egg (Domestic)", "allergens": ["Egg", "Soybean", "Peanut", "Wheat", "Milk"]},
        {"id": 13, "name": "Sweet Red Bean Bun", "ko": "단팥빵", "price": "1,700", "origin": "Whole red bean paste [Red bean (China), Refined salt (Domestic)]; Strong wheat flour (USA / Canada); Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"]},
        {"id": 14, "name": "Cream Cheese White Bun", "ko": "크림치즈화이트번", "price": "3,300", "origin": "Strong wheat flour (USA / Canada); Cream cheese (New Zealand); Milk (Raw milk: Domestic)", "allergens": ["Wheat", "Sulfites", "Milk"]},
        {"id": 15, "name": "Bread Donut", "ko": "빵도넛", "price": "1,700", "origin": "Whole red bean paste [Red bean (China), Refined salt (Domestic)]; Strong wheat flour (USA / Canada); Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 16, "name": "Long Twist", "ko": "키다리트위스트", "price": "3,000", "origin": "Strong wheat flour (USA / Canada); Cake flour (USA); Butter [Processed butter (Imported: New Zealand, Netherlands, Australia); Vegetable oil (Malaysia)]", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 17, "name": "French Pie", "ko": "후렌치파이", "price": "2,000", "origin": "Butter {Processed butter (Imported: NZ/NLD/AUS); Vegetable oil [Palm oil (Malaysia)]}; Strong wheat flour (USA / Canada); Raspberry jam (Denmark); Strawberry jam (Domestic)", "allergens": ["Egg", "Wheat", "Milk"]},
        {"id": 18, "name": "Almond Croissant", "ko": "아몬드크로와상", "price": "3,500", "origin": "Butter (France); Strong wheat flour (USA / Canada); Wheat flour (Wheat: USA); Almond (USA)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 19, "name": "Stone-Ground Whole Wheat Bread", "ko": "맷돌로갈은통밀빵", "price": "4,500", "origin": "Organic strong wheat flour (Türkiye); Whole wheat flour (Domestic); Walnut (USA)", "allergens": ["Wheat", "Walnut"]},
        {"id": 20, "name": "Squid Ink Baton", "ko": "오징어먹물방망이", "price": "3,300", "origin": "Strong wheat flour (USA / Canada); Butter (New Zealand); Condensed milk [Raw milk (Domestic), Lactose (USA)]; Squid ink (Spain)", "allergens": ["Egg", "Pork", "Wheat", "Squid", "Milk"]},
        {"id": 21, "name": "Red Wine Bread", "ko": "레드와인", "price": "4,500", "origin": "Organic strong wheat flour (Türkiye); Wine (Spain); Rye (Germany)", "allergens": ["Wheat", "Sulfites", "Walnut"]},
        {"id": 22, "name": "Walnut Bread", "ko": "월넛브레드", "price": "4,000", "origin": "Strong wheat flour (USA / Canada); Walnut (USA); Egg (White egg: Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"]},
        {"id": 23, "name": "Toyo Bread", "ko": "토요빵", "price": "3,800", "origin": "Strong wheat flour (USA / Canada); Milk (Raw milk: Domestic); Cream cheese (New Zealand); Sweet potato (Domestic)", "allergens": ["Soybean", "Wheat", "Beef", "Milk"]},
        {"id": 24, "name": "Plain Croissant", "ko": "플레인크로와상", "price": "2,800", "origin": "Butter sheet (France); Wheat flour (Wheat: USA); Strong wheat flour (USA / Canada); Milk (Raw milk: Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 25, "name": "Bomunsan Echo", "ko": "보문산메아리", "price": "6,000", "origin": "Strong wheat flour (USA / Canada); Butter sheet (France); Milk (Raw milk: Domestic); Egg (Domestic)", "allergens": ["Egg", "Soybean", "Wheat", "Milk"]},
        {"id": 26, "name": "Pie Manju Set", "ko": "파이만주세트", "price": "9,600", "origin": "Whole red bean paste [Red bean (China), Refined salt (Domestic)]; Strong wheat flour (USA / Canada); Almond powder (USA); Margarine (Imported)", "allergens": ["Egg", "Soybean", "Wheat", "Milk", "Walnut"]},
        {"id": 27, "name": "Pantaloon Chive Bread", "ko": "판타롱부추빵", "price": "2,000", "origin": "Korean chives (Domestic); Strong wheat flour (USA / Canada); Egg (Domestic)", "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)"]},
        {"id": 28, "name": "Twiso-guma", "ko": "튀소구마", "price": "1,700", "origin": "Sweet potato (Domestic); Wheat flour (USA/Canada); Skim milk powder (Imported); Cake flour (USA)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"]},
        {"id": 29, "name": "Twigim Soboro", "ko": "튀김소보로", "price": "1,700", "origin": "Whole red bean paste (China); Wheat flour (USA/Canada); Skim milk powder (Imported); Cake flour (USA)", "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"]}
    ]

    st.markdown("<h1 style='text-align: center; color: #78350f;'>🥖 Sungsimdang Allergy Safe Guide</h1>", unsafe_allow_html=True)
    st.warning(f"**🏭 Shared Facility Notice:** {FACILITY_NOTICE}")

    filtered = [b for b in bread_data if not any(a in b["allergens"] for a in avoid)]
    
    # 가이드 유도 문구 추가
    st.info(f"ℹ️ Found **{len(filtered)}** items. Click a card for full details. Scroll down for the **Comprehensive Summary Table**.")

    # 7. 프리미엄 카드 그리드 (카드 내 가격/알러지 정보 복구)  [cite: 4-157, 164-320]
    bread_json = json.dumps(filtered)
    html_code = f"""
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .modal-overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 10000; align-items: center; justify-content: center; padding: 20px; }}
        .modal-content {{ background: white; padding: 35px; border-radius: 2.5rem; max-width: 650px; width: 100%; position: relative; max-height: 85vh; overflow-y: auto; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }}
    </style>

    <div id="modal" class="modal-overlay" onclick="closeModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <button class="absolute top-5 right-7 text-3xl font-bold text-gray-400" onclick="closeModal()">×</button>
            <h2 id="m-title" class="text-2xl font-bold text-[#78350f] mb-1"></h2>
            <p id="m-ko" class="text-sm text-orange-700 font-bold mb-5"></p>
            <div class="space-y-4 text-sm text-gray-700">
                <p><strong>💰 Price:</strong> <span id="m-price"></span> KRW</p>
                <div><p class="font-bold text-orange-900 mb-1 uppercase text-xs">🌾 Detailed Origin Info:</p><p id="m-origin" class="bg-gray-50 p-3 rounded-xl leading-relaxed"></p></div>
                <div><p class="font-bold text-orange-900 mb-1 uppercase text-xs">🚫 Allergens Found:</p><p id="m-allergens" class="font-semibold"></p></div>
                <div class="bg-orange-50 p-4 rounded-xl border border-orange-100 text-[10px] italic">"{FACILITY_NOTICE}"</div>
            </div>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 p-4 bg-orange-50">
        <script>
            const data = {bread_json};
            const baseUrl = "{GITHUB_BASE_URL}";

            function openModal(id) {{
                const b = data.find(x => x.id === id);
                document.getElementById('m-title').innerText = b.name;
                document.getElementById('m-ko').innerText = b.ko;
                document.getElementById('m-price').innerText = b.price;
                document.getElementById('m-origin').innerText = b.origin;
                document.getElementById('m-allergens').innerText = b.allergens.join(', ');
                document.getElementById('modal').style.display = 'flex';
            }}
            function closeModal() {{ document.getElementById('modal').style.display = 'none'; }}

            data.forEach(bread => {{
                document.write(`
                    <div class="bg-white rounded-[2rem] overflow-hidden border border-orange-100 flex flex-col h-full shadow-lg transform transition hover:-translate-y-2">
                        <div class="h-60 overflow-hidden bg-gray-100 relative">
                            <img src="${{encodeURI(baseUrl + 'images/' + bread.id + '. ' + bread.name + '.png')}}" 
                                 style="width: 115%; height: 115%; object-fit: cover; object-position: left top; max-width: none;">
                        </div>
                        <div class="p-6 flex flex-col flex-grow text-center">
                            <h3 class="text-md font-bold text-gray-800 leading-tight">${{bread.name}}</h3>
                            <p class="text-[10px] text-orange-700 font-bold mb-2 opacity-60">${{bread.ko}}</p>
                            
                            <div class="text-orange-600 font-bold text-sm mb-3">${{bread.price}}W</div>
                            <div class="flex flex-wrap justify-center gap-1 mb-5">
                                ${{bread.allergens.slice(0, 3).map(a => `<span class="px-2 py-0.5 bg-orange-50 text-orange-600 text-[8px] rounded-full border border-orange-100 font-bold uppercase">${{a}}</span>`).join('')}}
                                ${{bread.allergens.length > 3 ? `<span class="text-[8px] text-gray-400 font-bold">...</span>` : ''}}
                            </div>

                            <button onclick="openModal(${{bread.id}})" 
                               class="mt-auto block w-full text-center bg-[#78350f] text-white py-3 rounded-2xl text-[9px] font-bold hover:bg-[#92400e] transition-colors shadow-md uppercase">
                               Comprehensive Guide ↗
                            </button>
                        </div>
                    </div>
                `);
            }});
        </script>
    </div>
    """
    components.html(html_code, height=1200, scrolling=True)

    # 8. 하단 전체 요약 데이터 시트 (체류 시간 극대화 장치) 
    st.markdown("---")
    st.markdown("### 📊 Comprehensive Bread Data Summary Table")
    st.caption("Review all 29 items at once. This table includes all technical data from the official documentation.")
    st.table([{"ID": b["id"], "Bread Name": f"{b['name']} ({b['ko']})", "Price": f"{b['price']}W", "Origin": b["origin"], "Allergens": ", ".join(b["allergens"])} for b in bread_data])
