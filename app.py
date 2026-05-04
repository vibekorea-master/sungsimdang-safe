import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Sungsimdang Allergy Guide", page_icon="🍞")

# 2. 강력한 영문 경고문 (Disclaimer) 섹션
st.error("🚨 IMPORTANT: MEDICAL DISCLAIMER")
disclaimer_text = """
**Please read carefully before using this guide:**
1. **Informational Purposes Only:** This application is an unofficial guide and is provided for informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.
2. **No Medical Guarantee:** We do not guarantee the 100% accuracy of the data. Recipe changes or cross-contamination at the facility may occur.
3. **Use at Your Own Risk:** By using this app, you acknowledge that you do so at your own risk. The developer and Sungsimdang are not liable for any allergic reactions or adverse effects.
4. **Final Verification:** If you have severe allergies, please consult with the bakery staff or a medical professional before consumption.
"""
st.markdown(disclaimer_text)

# 사용자의 동의 확인
agreed = st.checkbox("I have read the disclaimer and I understand that I am using this app at my own risk.")

# 3. 동의했을 때만 프로그램 작동
if agreed:
    st.success("Disclaimer Accepted. You may now use the guide.")
    st.divider()
    
    # [데이터베이스 및 메인 로직 시작]
    facility_allergens = [
        "Egg", "Milk", "Buckwheat", "Peanut", "Soy", "Wheat", "Mackerel", 
        "Crab", "Shrimp", "Pork", "Peach", "Tomato", "Sulfites", "Walnut", 
        "Chicken", "Beef", "Squid", "Shellfish", "Pine nut", "Sesame", "Macadamia"
    ]

    products = [
        {"name": "Fried Soboro", "desc": "Fried streusel bread with red bean.", "allergens": ["Egg", "Soy", "Wheat", "Sulfites", "Milk"]},
        {"name": "Pantaloon Chive Bread", "desc": "Soft bun with fresh chives and egg salad.", "allergens": ["Egg", "Chicken", "Soy", "Pork", "Wheat", "Beef", "Milk", "Shellfish"]},
        # ... (이전 코드의 제품 리스트 동일하게 유지)
    ]

    st.subheader("Step 1: Select your Allergies")
    user_selected = st.multiselect("Check all that apply to you:", options=sorted(facility_allergens))

    if st.button("Check My Safety"):
        if not user_selected:
            st.warning("Please select at least one allergen.")
        else:
            st.subheader("Step 2: Analysis Results")
            tab1, tab2, tab3 = st.tabs(["🚨 DANGER", "⚠️ WARNING", "✅ SAFE"])
            
            for p in products:
                danger_list = [a for a in user_selected if a in p["allergens"]]
                # 교차 오염 주의 성분 확인
                warning_list = [a for a in user_selected if a in facility_allergens]
                
                with (tab1 if danger_list else tab2 if warning_list else tab3):
                    with st.expander(f"{p['name']}"):
                        st.write(f"**Desc:** {p['desc']}")
                        if danger_list:
                            st.error(f"CONTAINS: {', '.join(danger_list)}")
                        elif warning_list:
                            st.warning("Risk of cross-contact at the facility.")
                        else:
                            st.success("No known risks for selected allergens.")
else:
    st.info("Please check the box above to start the allergy analysis.")