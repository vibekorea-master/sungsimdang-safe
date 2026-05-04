import streamlit as st

# 1. 페이지 설정 및 디자인 개선 (넓은 화면 사용)
st.set_page_config(page_title="Sungsimdang Safety Guide", page_icon="🥐", layout="wide")

# 커스텀 CSS로 디자인 입히기
st.markdown("""
    <style>
    .main { background-color: #fffaf0; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #e67e22; color: white; }
    .bread-card { border: 1px solid #ddd; padding: 15px; border-radius: 15px; background-color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .badge { padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: bold; }
    .best-seller { background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. 강력한 영문 경고문 (상단 고정)
with st.container():
    st.error("🚨 IMPORTANT: MEDICAL DISCLAIMER")
    with st.expander("Read Safety Information Before Use"):
        st.write("""
        1. **Informational Purposes Only:** This is an unofficial guide.
        2. **No Medical Guarantee:** Recipe changes or cross-contamination may occur.
        3. **Use at Your Own Risk:** Developer and Sungsimdang are not liable for any reactions.
        4. **Final Verification:** Always check with staff if you have severe allergies.
        """)
    agreed = st.checkbox("I understand and agree to the terms above.")

if agreed:
    st.divider()
    
    # 데이터베이스 (정보를 더 풍성하게 추가)
    products = [
        {"name": "Fried Soboro (튀김소보로)", "category": "Best Seller", "price": "1,700 KRW", "desc": "Crunchy streusel bread with sweet red bean paste inside.", "allergens": ["Egg", "Soy", "Wheat", "Milk", "Sulfites"]},
        {"name": "Pantaloon Chive Bread (판타롱부추빵)", "category": "Signature", "price": "2,000 KRW", "desc": "Soft bun filled with fresh chives and egg salad.", "allergens": ["Egg", "Chicken", "Soy", "Pork", "Wheat", "Beef", "Milk", "Shellfish"]},
        {"name": "Myeongnan Baguette (명란바게트)", "category": "Hot Item", "price": "3,800 KRW", "desc": "Salty and savory baguette with pollack roe.", "allergens": ["Wheat", "Soy", "Egg", "Milk", "Fish"]},
        {"name": "Plain Scone", "category": "Classic", "price": "2,500 KRW", "desc": "Simple, buttery, and flaky scone.", "allergens": ["Wheat", "Milk", "Egg"]},
    ]

    # 왼쪽 사이드바: 필터 설정
    with st.sidebar:
        st.title("🛡️ Allergy Filter")
        st.info("Select ingredients you must avoid.")
        all_allergens = sorted(list(set([a for p in products for a in p["allergens"]])))
        user_selected = st.multiselect("Your Allergies:", options=all_allergens)
        st.divider()
        st.write("📖 **Tip:** Items marked as 'Safe' do not contain your selected allergens in their main recipe.")

    # 메인 섹션
    st.title("🥐 Find Your Safe Bread")
    search_query = st.text_input("Search bread name (e.g., Soboro)", "")

    # 검색 및 필터링 로직
    filtered_products = [p for p in products if search_query.lower() in p["name"].lower()]

    # 카드형 레이아웃 구성 (3열)
    cols = st.columns(3)
    for i, p in enumerate(filtered_products):
        with cols[i % 3]:
            danger_list = [a for a in user_selected if a in p["allergens"]]
            
            st.markdown(f"""
                <div class="bread-card">
                    <span class="badge best-seller">{p['category']}</span>
                    <h3>{p['name']}</h3>
                    <p style="color: #666; font-size: 0.9em;">{p['desc']}</p>
                    <p><b>Price:</b> {p['price']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if danger_list:
                st.error(f"⚠️ CONTAINS: {', '.join(danger_list)}")
            elif user_selected:
                st.success("✅ Safe for you")
            
            with st.expander("See All Ingredients"):
                st.write(f"This product contains: {', '.join(p['allergens'])}")
            st.write("") # 간격 조절

else:
    st.info("👋 Welcome! Please agree to the safety disclaimer above to start your journey at Sungsimdang.")
