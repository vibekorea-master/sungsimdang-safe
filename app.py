import streamlit as st
import streamlit.components.v1 as components
import json

# ─────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sungsimdang Allergy Reference Guide",
    page_icon="🥖",
    layout="wide",
    initial_sidebar_state="collapsed",   # 사이드바 완전히 숨김
)

if "disclaimer_accepted" not in st.session_state:
    st.session_state.disclaimer_accepted = False

# ─────────────────────────────────────────────
# 2. CONSTANTS
# ─────────────────────────────────────────────
GITHUB_BASE_URL = "https://raw.githubusercontent.com/vibekorea-master/sungsimdang-safe/main/"
DATA_AS_OF = "May 2025"
FACILITY_NOTICE = (
    "This product is manufactured in the same facility as products containing eggs (poultry), "
    "milk, buckwheat, peanuts, soybeans, wheat, mackerel, crab, shrimp, pork, peaches, tomatoes, "
    "sulfites, walnuts, chicken, beef, squid, shellfish (including oysters, abalone, and mussels), "
    "and pine nuts."
)

ALL_ALLERGENS = sorted([
    "Wheat", "Milk", "Egg", "Soybean", "Pork", "Beef", "Chicken",
    "Shrimp", "Squid", "Walnut", "Peanut", "Sulfites",
    "Shellfish (Oyster)", "Tomato"
])

# ─────────────────────────────────────────────
# 3. BREAD DATA (29 items)
# ─────────────────────────────────────────────
BREAD_DATA = [
    {
        "id": 1, "name": "Malami Croquette", "ko": "마라미고로케",
        "price": "3,000", "category": "Savory",
        "description": "Crispy fried croquette filled with spicy Mala-style pork and sauce.",
        "origin": "Medium-strength wheat flour (USA / Australia); Minced pork (Pork: Domestic); Breadcrumbs [Strong wheat flour (USA / Canada); Breadcrumb mix (Wheat: USA / Canada, Gluten: France)]; Mala Xiangguo sauce [Mala Xiangguo sauce base (China — doubanjiang, soybean oil, dried chili, brewed soy sauce, green Sichuan pepper); Pork bone extract (Pork bone: Domestic)]; Classic Malatang sauce (China)",
        "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Shrimp", "Beef", "Squid", "Milk"]
    },
    {
        "id": 2, "name": "Pain au Chocolat", "ko": "뺑오쇼콜라",
        "price": "3,000", "category": "Pastry",
        "description": "Flaky laminated dough wrapped around a rich French chocolate stick.",
        "origin": "Butter sheet (Netherlands); Wheat flour (USA); Strong wheat flour (USA / Canada); Chocolate stick (France)",
        "allergens": ["Egg", "Soybean", "Wheat", "Milk"]
    },
    {
        "id": 3, "name": "Mochi-Mochi Milk Bread", "ko": "모찌모찌식빵",
        "price": "3,500", "category": "Bread",
        "description": "Pillowy soft milk bread with a chewy mochi-like texture.",
        "origin": "Strong wheat flour (USA / Canada); Whole milk powder (Netherlands); Butter (New Zealand)",
        "allergens": ["Soybean", "Pork", "Wheat", "Milk"]
    },
    {
        "id": 4, "name": "Vegetable Croquette", "ko": "야채고로케",
        "price": "2,300", "category": "Savory",
        "description": "Crispy fried croquette filled with seasoned vegetables and sausage.",
        "origin": "Medium-strength wheat flour (USA / Australia); Onion (Domestic); Sausage — Chicken (Domestic), Pork (Domestic), Pork fat (Domestic)",
        "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]
    },
    {
        "id": 5, "name": "Little Echo", "ko": "작은메아리",
        "price": "3,000", "category": "Pastry",
        "description": "A smaller version of the signature Bomunsan Echo — buttery laminated pastry.",
        "origin": "Butter sheet (Netherlands); Wheat flour (Wheat: USA); Strong wheat flour (USA / Canada); Milk (Raw milk: Domestic)",
        "allergens": ["Egg", "Soybean", "Wheat", "Milk"]
    },
    {
        "id": 6, "name": "Noix Raisin", "ko": "노아레즌",
        "price": "7,000", "category": "Artisan",
        "description": "Rustic artisan loaf made with organic Turkish wheat, walnuts, and raisins.",
        "origin": "Organic strong wheat flour (Türkiye); Walnut (USA); Organic cake flour (Türkiye)",
        "allergens": ["Wheat", "Sulfites", "Walnut"]
    },
    {
        "id": 7, "name": "October Fig", "ko": "시월의무화과",
        "price": "5,000", "category": "Artisan",
        "description": "Artisan bread with organic Turkish wheat and sweet figs from Türkiye.",
        "origin": "Organic strong wheat flour (Türkiye); Fig (Türkiye); Strong wheat flour (USA / Canada)",
        "allergens": ["Wheat", "Sulfites", "Walnut"]
    },
    {
        "id": 8, "name": "Big Match", "ko": "빅매치",
        "price": "2,300", "category": "Bread",
        "description": "Soft bread filled with New Zealand cream cheese and butter.",
        "origin": "Cream cheese (New Zealand); Strong wheat flour (USA / Canada); Butter (New Zealand)",
        "allergens": ["Egg", "Soybean", "Wheat", "Milk"]
    },
    {
        "id": 9, "name": "Under the Fig Tree", "ko": "무화과그늘아래",
        "price": "3,000", "category": "Artisan",
        "description": "Organic wheat bread layered with fig and US cream cheese.",
        "origin": "Organic strong wheat flour (Türkiye); Cream cheese (USA); Wheat flour (Wheat: Domestic); Fig (Türkiye)",
        "allergens": ["Wheat", "Sulfites", "Milk", "Walnut"]
    },
    {
        "id": 10, "name": "Steak Bread", "ko": "스테이크빵",
        "price": "2,300", "category": "Savory",
        "description": "Soft bread stuffed with Korean-style marinated pork (Neobiani) and onion.",
        "origin": "Neobiani (Korean-style sliced grilled pork) [Pork: Imported (USA, Spain, Canada, etc.); Green onion (China)]; Onion (Domestic); Strong wheat flour (USA / Canada)",
        "allergens": ["Egg", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]
    },
    {
        "id": 11, "name": "Sunflower", "ko": "해바라기",
        "price": "2,000", "category": "Savory",
        "description": "Sunflower-shaped bread filled with onion and Frankfurt sausage.",
        "origin": "Onion (Domestic); Frankfurt sausage — Chicken (Domestic), Pork (Domestic); Strong wheat flour (USA / Canada)",
        "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)", "Tomato"]
    },
    {
        "id": 12, "name": "Soboro Bun", "ko": "소보로",
        "price": "1,300", "category": "Sweet",
        "description": "Classic Korean streusel bun with a crumbly, sweet topping.",
        "origin": "Strong wheat flour (USA / Canada); Cake flour (USA); Egg (Domestic)",
        "allergens": ["Egg", "Soybean", "Peanut", "Wheat", "Milk"]
    },
    {
        "id": 13, "name": "Sweet Red Bean Bun", "ko": "단팥빵",
        "price": "1,700", "category": "Sweet",
        "description": "Soft bun filled with smooth red bean paste — a Korean bakery classic.",
        "origin": "Whole red bean paste — Red bean (China), Refined salt (Domestic); Strong wheat flour (USA / Canada); Egg (Domestic)",
        "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"]
    },
    {
        "id": 14, "name": "Cream Cheese White Bun", "ko": "크림치즈화이트번",
        "price": "3,300", "category": "Sweet",
        "description": "Fluffy white bun generously filled with New Zealand cream cheese.",
        "origin": "Strong wheat flour (USA / Canada); Cream cheese (New Zealand); Milk (Raw milk: Domestic)",
        "allergens": ["Wheat", "Sulfites", "Milk"]
    },
    {
        "id": 15, "name": "Bread Donut", "ko": "빵도넛",
        "price": "1,700", "category": "Sweet",
        "description": "Soft baked donut filled with sweet red bean paste.",
        "origin": "Whole red bean paste — Red bean (China), Refined salt (Domestic); Strong wheat flour (USA / Canada); Egg (Domestic)",
        "allergens": ["Egg", "Soybean", "Wheat", "Milk"]
    },
    {
        "id": 16, "name": "Long Twist", "ko": "키다리트위스트",
        "price": "3,000", "category": "Sweet",
        "description": "Long twisted pastry made with imported butter and palm oil.",
        "origin": "Strong wheat flour (USA / Canada); Cake flour (USA); Butter — Processed butter (Imported: NZ, NLD, AUS); Vegetable oil (Malaysia)",
        "allergens": ["Egg", "Soybean", "Wheat", "Milk"]
    },
    {
        "id": 17, "name": "French Pie", "ko": "후렌치파이",
        "price": "2,000", "category": "Pastry",
        "description": "Flaky pastry filled with Danish raspberry jam and domestic strawberry jam.",
        "origin": "Butter {Processed butter (Imported: New Zealand, Netherlands, Australia, etc.); Vegetable oil [Palm oil (Malaysia), Palm stearin oil (Malaysia)]}; Strong wheat flour (USA / Canada); Raspberry jam (Denmark); Strawberry jam (Strawberry: Domestic)",
        "allergens": ["Egg", "Wheat", "Milk"]
    },
    {
        "id": 18, "name": "Almond Croissant", "ko": "아몬드크로와상",
        "price": "3,500", "category": "Pastry",
        "description": "Buttery French croissant topped with almond cream and sliced almonds.",
        "origin": "Butter (France); Strong wheat flour (USA / Canada); Wheat flour (USA); Almond (USA)",
        "allergens": ["Egg", "Soybean", "Wheat", "Milk"]
    },
    {
        "id": 19, "name": "Stone-Ground Whole Wheat Bread", "ko": "맷돌로갈은통밀빵",
        "price": "4,500", "category": "Artisan",
        "description": "Hearty loaf made with stone-ground organic wheat and walnuts.",
        "origin": "Organic strong wheat flour (Türkiye); Whole wheat flour (Domestic); Walnut (USA)",
        "allergens": ["Wheat", "Walnut"]
    },
    {
        "id": 20, "name": "Squid Ink Baton", "ko": "오징어먹물방망이",
        "price": "3,300", "category": "Savory",
        "description": "Baton bread colored and flavored with Spanish squid ink.",
        "origin": "Strong wheat flour (USA / Canada); Butter (New Zealand); Condensed milk — Raw milk (Domestic), Lactose (USA); Squid ink (Spain)",
        "allergens": ["Egg", "Pork", "Wheat", "Squid", "Milk"]
    },
    {
        "id": 21, "name": "Red Wine Bread", "ko": "레드와인",
        "price": "4,500", "category": "Artisan",
        "description": "Artisan rye loaf made with organic Turkish wheat and Spanish red wine.",
        "origin": "Organic strong wheat flour (Türkiye); Wine (Spain); Rye (Germany)",
        "allergens": ["Wheat", "Sulfites", "Walnut"]
    },
    {
        "id": 22, "name": "Walnut Bread", "ko": "월넛브레드",
        "price": "4,000", "category": "Artisan",
        "description": "Classic walnut loaf packed with American walnuts.",
        "origin": "Strong wheat flour (USA / Canada); Walnut (USA); Egg white (Domestic)",
        "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk", "Walnut"]
    },
    {
        "id": 23, "name": "Toyo Bread", "ko": "토요빵 (토요일 특별빵)",
        "price": "3,800", "category": "Sweet",
        "description": "Soft Saturday special bread with cream cheese and sweet potato.",
        "origin": "Strong wheat flour (USA / Canada); Milk (Raw milk: Domestic); Cream cheese (New Zealand); Sweet potato (Domestic)",
        "allergens": ["Soybean", "Wheat", "Beef", "Milk"]
    },
    {
        "id": 24, "name": "Plain Croissant", "ko": "플레인크로와상",
        "price": "2,800", "category": "Pastry",
        "description": "Classic French croissant with premium French butter sheet.",
        "origin": "Butter sheet (France); Wheat flour (Wheat: USA); Strong wheat flour (USA / Canada); Milk (Raw milk: Domestic)",
        "allergens": ["Egg", "Soybean", "Wheat", "Milk"]
    },
    {
        "id": 25, "name": "Bomunsan Echo", "ko": "보문산메아리",
        "price": "6,000", "category": "Pastry",
        "description": "Sungsimdang's signature buttery French-style pastry — a must-try icon.",
        "origin": "Strong wheat flour (USA / Canada); Butter sheet (France); Raw milk (Domestic); Egg (Domestic)",
        "allergens": ["Egg", "Soybean", "Wheat", "Milk"]
    },
    {
        "id": 26, "name": "Pie Manju Set (8 pcs)", "ko": "파이만주세트 (8개)",
        "price": "9,600", "category": "Sweet",
        "description": "Set of 8 pie-pastry manju filled with red bean paste and almond.",
        "origin": "Whole red bean paste [Red bean (China), Refined salt (Domestic)]; Strong wheat flour (USA / Canada); Almond powder (USA); Margarine {Processed fats and oils [Palm esterified oil (Malaysia), Palm kernel esterified oil (Malaysia)]; Prepared edible fat (New Zealand, Australia, Malaysia, etc.)}",
        "allergens": ["Egg", "Soybean", "Wheat", "Milk", "Walnut"]
    },
    {
        "id": 27, "name": "Pantaloon Chive Bread", "ko": "판타롱부추빵",
        "price": "2,000", "category": "Savory",
        "description": "Savory bread generously filled with domestic Korean chives.",
        "origin": "Korean chives (Domestic); Strong wheat flour (USA / Canada); Egg (Domestic)",
        "allergens": ["Egg", "Chicken", "Soybean", "Pork", "Wheat", "Beef", "Milk", "Shellfish (Oyster)"]
    },
    {
        "id": 28, "name": "Twiso-guma", "ko": "튀소구마",
        "price": "1,700", "category": "Sweet",
        "description": "Fried sweet potato bun with soboro topping — a sweet potato twist on a classic.",
        "origin": "Sweet potato (Domestic); Processed cereal product [Wheat flour (Wheat: USA, Canada); Mixed skim milk powder (Skim milk powder — Imported: USA, France, Belgium, etc.)]; Cake flour (USA)",
        "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"]
    },
    {
        "id": 29, "name": "Twigim Soboro", "ko": "튀김소보로",
        "price": "1,700", "category": "Sweet",
        "description": "Sungsimdang's most iconic bread — fried streusel bun filled with red bean paste.",
        "origin": "Whole red bean paste [Red bean (China), Refined salt (Domestic)]; Processed cereal product [Wheat flour (Wheat: USA, Canada); Mixed skim milk powder (Skim milk powder — Imported: USA, France, Belgium, etc.)]; Cake flour (USA)",
        "allergens": ["Egg", "Soybean", "Wheat", "Sulfites", "Milk"]
    },
]

CATEGORY_COLORS = {
    "Sweet":   {"bg": "#fff7ed", "border": "#fb923c", "text": "#9a3412"},
    "Savory":  {"bg": "#f0fdf4", "border": "#4ade80", "text": "#166534"},
    "Pastry":  {"bg": "#fdf4ff", "border": "#c084fc", "text": "#6b21a8"},
    "Artisan": {"bg": "#fefce8", "border": "#facc15", "text": "#713f12"},
    "Bread":   {"bg": "#eff6ff", "border": "#60a5fa", "text": "#1e3a8a"},
}

# ─────────────────────────────────────────────
# 4. GLOBAL STYLES — 사이드바 토글 버튼 완전 숨김
# ─────────────────────────────────────────────
st.markdown("""
<style>
header, footer, #MainMenu { visibility: hidden; }
/* Streamlit 우하단 뱃지 / Deploy 버튼 완전 숨김 */
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.viewerBadge_container__r5tak,
.viewerBadge_link__qRIco,
#stDecoration,
.stDeployButton,
[data-testid="stDeployButton"],
.styles_viewerBadge__CvC9N,
.viewerBadge_text__1eB1_,
iframe[title="streamlit_viewer_badge"],
div[class*="viewerBadge"],
div[class*="StatusWidget"],
div[class*="stToolbar"] { display: none !important; visibility: hidden !important; }
/* 사이드바 완전 제거 */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
section[data-testid="stSidebar"] { display: none !important; }
/* 모바일 우선 레이아웃 */
.main .block-container {
    max-width: 720px;
    padding: 0.5rem 1rem 2rem 1rem;
}
/* 기본 버튼 스타일 */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #d97706, #78350f);
    border: none; border-radius: 50px;
    font-size: 16px; font-weight: 800;
    padding: 14px 24px; color: white;
    width: 100%;
    box-shadow: 0 8px 20px rgba(120,53,15,0.35);
    transition: transform .15s;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px);
}
/* Streamlit metric 모바일 폰트 조정 */
[data-testid="stMetricValue"] { font-size: 1.2rem !important; }
[data-testid="stMetricLabel"] { font-size: 0.7rem !important; }
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════
# GATE — Disclaimer screen
# ═════════════════════════════════════════════
if not st.session_state.disclaimer_accepted:

    # 배경 이미지 CSS (st.markdown — HTML 주석 없음)
    st.markdown(
        "<style>"
        ".stApp {"
        "background: linear-gradient(rgba(0,0,0,0.72), rgba(0,0,0,0.72)),"
        f"url('{GITHUB_BASE_URL}images/29. Twigim Soboro.png');"
        "background-size: cover; background-position: center; background-attachment: fixed;"
        "}"
        "</style>",
        unsafe_allow_html=True
    )

    # 게이트 카드 — components.html() 사용 / 모바일 최적화 / 한글 직접 삽입
    gate_html = (
        '<!DOCTYPE html>'
        '<html><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<style>'
        '*{box-sizing:border-box;margin:0;padding:0;}'
        'html,body{height:100%;background:transparent;'
        'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}'
        'body{padding:10px 10px 2px 10px;display:flex;flex-direction:column;}'
        '.card{background:white;border-radius:22px;'
        'padding:20px 18px 20px;'
        'box-shadow:0 20px 50px rgba(0,0,0,0.5);'
        'overflow-y:auto;flex:1;}'
        '.logo{font-size:32px;line-height:1;margin-bottom:5px;text-align:center;}'
        '.title{color:#78350f;font-size:19px;font-weight:900;margin-bottom:2px;'
        'line-height:1.2;text-align:center;}'
        '.subtitle{color:#92400e;font-size:11px;font-weight:600;margin-bottom:14px;'
        'opacity:.8;text-align:center;}'
        '.red-box{background:#fef2f2;border:2px solid #fca5a5;border-radius:14px;'
        'padding:13px 15px;margin-bottom:11px;text-align:left;}'
        '.red-title{color:#991b1b;font-size:12px;font-weight:900;letter-spacing:.3px;'
        'margin-bottom:9px;}'
        '.red-box ul{color:#b91c1c;font-size:12.5px;line-height:1.75;padding-left:18px;}'
        '.red-box li{margin-bottom:5px;}'
        '.orange-box{background:#fff7ed;border:1.5px solid #fed7aa;border-radius:12px;'
        'padding:11px 14px;margin-bottom:14px;text-align:left;}'
        '.orange-title{color:#92400e;font-size:10.5px;font-weight:900;text-transform:uppercase;'
        'letter-spacing:.4px;margin-bottom:6px;}'
        '.orange-text{color:#78350f;font-size:11px;line-height:1.65;font-style:italic;}'
        '.agree-text{color:#374151;font-size:12px;font-weight:700;text-align:center;'
        'margin-top:4px;}'
        '</style></head>'
        '<body>'
        '<div class="card">'
        '<div class="logo">&#x1F956;</div>'
        '<div class="title">Sungsimdang Allergy Reference Guide</div>'
        '<div class="subtitle">성심당 알러지 참고 가이드 &mdash; Unofficial Fan Guide</div>'
        '<div class="red-box">'
        '<div class="red-title">&#9888;&#65039; PLEASE READ BEFORE CONTINUING</div>'
        '<ul>'
        '<li><strong>NOT affiliated with Sungsimdang (성심당).</strong></li>'
        '<li>Author is <strong>NOT a medical professional</strong>, dietitian, or food scientist.</li>'
        '<li>This is a <strong>reference tool only</strong> &mdash; NOT medical advice.</li>'
        '<li>Recipes can change without notice &mdash; always check on-site.</li>'
        '<li><strong>Always confirm allergens with staff in person</strong> before purchasing.</li>'
        '<li>Severe allergies? <strong>Consult your physician</strong> before traveling.</li>'
        '</ul></div>'
        '<div class="orange-box">'
        '<div class="orange-title">&#x1F3ED; Shared Facility Notice</div>'
        '<div class="orange-text">'
        + FACILITY_NOTICE +
        '</div></div>'
        '<p class="agree-text">&#x2B07; Scroll up if needed, then tap the button below to continue.</p>'
        '</div>'
        '</body></html>'
    )
    components.html(gate_html, height=540, scrolling=True)

    # 버튼: 컬럼 분리 없이 전체 너비로 (모바일 최적화)
    if st.button("✅  I AGREE & VIEW 29 BREADS", use_container_width=True, type="primary"):
        st.session_state.disclaimer_accepted = True
        st.rerun()

    st.markdown(
        "<p style='text-align:center;color:rgba(255,255,255,0.65);"
        "font-size:11px;margin-top:8px;letter-spacing:.2px;'>"
        "&#x1F513; Free &nbsp;&bull;&nbsp; Unofficial &nbsp;&bull;&nbsp; "
        "Always verify allergens with Sungsimdang staff in person</p>",
        unsafe_allow_html=True
    )


# ═════════════════════════════════════════════
# MAIN APP
# ═════════════════════════════════════════════
else:
    st.markdown("""
    <style>
    .stApp { background-color: #fffaf5 !important; background-image: none !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── 헤더 (모바일 최적화: 컴팩트, 줄바꿈 방지) ─
    st.markdown(
        '<div style="text-align:center;padding:12px 0 10px;">'
        '<p style="font-size:30px;margin:0 0 4px;">&#x1F956;</p>'
        '<h1 style="color:#78350f;font-size:21px;font-weight:900;margin:0 0 4px;'
        'line-height:1.25;letter-spacing:-.2px;">'
        'Sungsimdang Allergy Reference Guide</h1>'
        '<p style="color:#92400e;font-size:12px;font-weight:600;margin:0 0 2px;">'
        '성심당 알러지 참고 가이드</p>'
        '<p style="color:#b45309;font-size:10.5px;font-weight:500;margin:0;opacity:.8;">'
        f'Unofficial Fan Guide &nbsp;&bull;&nbsp; Daejeon, Korea &nbsp;&bull;&nbsp; Data: {DATA_AS_OF}</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── 법적 고지 배너 (항상 표시, 모바일 최적화) ─
    st.markdown(
        '<div style="background:#fef2f2;border:2px solid #fca5a5;border-radius:12px;'
        'padding:10px 14px;margin:0 0 10px;">'
        '<p style="color:#991b1b;font-size:12px;line-height:1.6;margin:0;font-weight:600;">'
        '&#9888;&#65039;&nbsp; <strong>NOT affiliated with Sungsimdang.</strong>&nbsp; '
        '<strong>Not medical advice.</strong>&nbsp; '
        'Always confirm allergens <strong>with staff in person</strong> before purchasing. '
        'Prices subject to change without notice.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── 공동 시설 주의 ─────────────────────────
    st.warning(f"🏭 **Shared Facility Notice:** {FACILITY_NOTICE}")

    # ══════════════════════════════════════════
    # ★ 알러지 필터 패널 — 항상 보이는 메인 inline
    # ══════════════════════════════════════════
    st.markdown(
        '<div style="background:#fff8f0;border:2px solid #f59e0b;border-radius:16px;'
        'padding:12px 16px 12px 16px;margin:8px 0 0 0;">'
        '<p style="color:#78350f;font-size:14px;font-weight:900;margin:0;'
        'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'
        '&#x1F6AB;&nbsp; Allergy Filter &mdash; Select allergens to avoid.'
        ' Matching breads will be hidden.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── 알러지 멀티셀렉트 (핵심 기능, 레이블 크고 굵게, 눈에 띄는 하이라이트) ──
    st.markdown(
        '<div style="background:#fffbeb;border-left:5px solid #d97706;'
        'border-radius:0 10px 10px 0;padding:10px 14px;margin:10px 0 6px;">'
        '<p style="color:#78350f;font-size:15px;font-weight:900;margin:0;'
        'letter-spacing:.1px;">'
        '&#9888;&#65039;&nbsp; Select all allergens you need to avoid:</p>'
        '</div>',
        unsafe_allow_html=True
    )
    avoid = st.multiselect(
        "Select all allergens you need to avoid:",
        ALL_ALLERGENS,
        placeholder="Tap here — e.g. Wheat, Milk, Egg, Pork…",
        label_visibility="collapsed",
    )

    # ── 카테고리 필터 (접이식, 모바일 세로 배치) ──
    all_cats = sorted(set(b["category"] for b in BREAD_DATA))
    selected_cats = st.multiselect(
        "🗂 Show bread categories:",
        all_cats,
        default=all_cats,
        placeholder="Select categories…"
    )

    # ── 결과 요약 바 ───────────────────────────
    filtered = [
        b for b in BREAD_DATA
        if not any(a in b["allergens"] for a in avoid)
        and b["category"] in selected_cats
    ]
    total  = len(BREAD_DATA)
    shown  = len(filtered)
    hidden = total - shown

    # ── 결과 요약 (모바일: 수평 3칸 컴팩트) ────
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("✅ Showing", f"{shown}")
    col_b.metric("🚫 Hidden", f"{hidden}")
    col_c.metric("📋 Total", f"{total}")

    if avoid:
        avoid_str = ", ".join(avoid)
        st.markdown(
            f'<div style="background:#fef2f2;border:1.5px solid #fca5a5;border-radius:10px;'
            f'padding:8px 12px;margin:4px 0 6px;">'
            f'<p style="color:#991b1b;font-size:12px;font-weight:700;margin:0;">'
            f'&#x1F50D; Hiding breads with: <strong>{avoid_str}</strong></p></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div style="background:#f0fdf4;border:1.5px solid #86efac;border-radius:10px;'
            'padding:8px 12px;margin:4px 0 6px;">'
            '<p style="color:#166534;font-size:12px;font-weight:700;margin:0;">'
            'ℹ️ No allergen filter active &mdash; all breads shown. Select allergens above to filter.</p></div>',
            unsafe_allow_html=True
        )

    # ── 카드 그리드 (HTML component) ──────────
    bread_json     = json.dumps(filtered)
    cat_colors_json = json.dumps(CATEGORY_COLORS)

    html_code = (
        '<!DOCTYPE html><html><head><meta charset="UTF-8">'
        '<script src="https://cdn.tailwindcss.com"></script>'
        '<style>'
        'body{margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}'
        '.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.82);'
        'z-index:99999;align-items:center;justify-content:center;padding:20px;}'
        '.modal-content{background:white;padding:32px 36px;border-radius:2.5rem;'
        'max-width:660px;width:100%;position:relative;max-height:88vh;overflow-y:auto;'
        'box-shadow:0 30px 80px rgba(0,0,0,0.55);animation:popIn .2s ease;}'
        '@keyframes popIn{from{opacity:0;transform:scale(.93) translateY(12px)}'
        'to{opacity:1;transform:scale(1) translateY(0)}}'
        '.bread-card{background:white;border-radius:1.75rem;overflow:hidden;'
        'border:1.5px solid #ffe4c4;display:flex;flex-direction:column;height:100%;'
        'box-shadow:0 4px 18px rgba(120,53,15,.10);'
        'transition:transform .2s,box-shadow .2s;cursor:pointer;}'
        '.bread-card:hover{transform:translateY(-5px);'
        'box-shadow:0 14px 36px rgba(120,53,15,.18);}'
        '.chip{display:inline-block;padding:2px 9px;border-radius:9999px;'
        'font-size:10px;font-weight:700;border:1px solid;'
        'text-transform:uppercase;letter-spacing:.3px;}'
        '.chip-neutral{background:#f9fafb;border-color:#d1d5db;color:#4b5563;}'
        '.modal-disc{background:#fef2f2;border:1.5px solid #fca5a5;'
        'border-radius:14px;padding:14px 16px;margin-top:18px;}'
        '.card-grid{display:grid;'
        'grid-template-columns:repeat(auto-fill,minmax(220px,1fr));'
        'gap:22px;padding:8px 4px 24px;}'
        '.empty-state{text-align:center;padding:60px 20px;color:#9ca3af;}'
        '</style></head><body>'

        '<div id="modal" class="modal-overlay" onclick="closeModal()">'
        '<div class="modal-content" onclick="event.stopPropagation()">'
        '<button onclick="closeModal()" style="position:absolute;top:16px;right:22px;'
        'font-size:26px;line-height:1;color:#9ca3af;background:none;border:none;'
        'cursor:pointer;font-weight:700;">&times;</button>'
        '<div id="m-cat" style="display:inline-block;margin-bottom:10px;padding:3px 14px;'
        'border-radius:999px;font-size:11px;font-weight:800;'
        'text-transform:uppercase;letter-spacing:.5px;"></div>'
        '<h2 id="m-title" style="color:#78350f;font-size:22px;font-weight:900;margin:0 0 3px;"></h2>'
        '<p id="m-ko" style="color:#b45309;font-size:14px;font-weight:700;margin:0 0 16px;"></p>'
        '<div style="display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap;">'
        '<div style="background:#fff7ed;border:1.5px solid #fed7aa;border-radius:12px;'
        'padding:10px 16px;flex:1;min-width:110px;">'
        '<p style="color:#92400e;font-size:10px;font-weight:800;text-transform:uppercase;'
        'letter-spacing:.5px;margin:0 0 3px;">&#x1F4B0; Price</p>'
        '<p id="m-price" style="color:#78350f;font-size:20px;font-weight:900;margin:0;"></p></div>'
        '<div style="background:#f0fdf4;border:1.5px solid #86efac;border-radius:12px;'
        'padding:10px 16px;flex:2;min-width:150px;">'
        '<p style="color:#166534;font-size:10px;font-weight:800;text-transform:uppercase;'
        'letter-spacing:.5px;margin:0 0 4px;">&#x1F956; Description</p>'
        '<p id="m-desc" style="color:#14532d;font-size:12px;line-height:1.55;margin:0;"></p></div>'
        '</div>'
        '<div style="margin-bottom:14px;">'
        '<p style="color:#92400e;font-size:10px;font-weight:800;text-transform:uppercase;'
        'letter-spacing:.5px;margin:0 0 7px;">&#x1F33E; Ingredient Origin Info</p>'
        '<p id="m-origin" style="background:#fafafa;border:1px solid #e5e7eb;'
        'border-radius:14px;padding:14px 16px;font-size:13px;'
        'line-height:1.7;color:#374151;margin:0;"></p></div>'
        '<div style="margin-bottom:6px;">'
        '<p style="color:#92400e;font-size:10px;font-weight:800;text-transform:uppercase;'
        'letter-spacing:.5px;margin:0 0 8px;">&#x1F6AB; Allergens in This Item</p>'
        '<div id="m-allergens" style="display:flex;flex-wrap:wrap;gap:6px;"></div></div>'
        '<div class="modal-disc">'
        '<p style="color:#991b1b;font-size:11px;font-weight:800;margin:0 0 5px;">'
        '&#9888;&#65039; IMPORTANT DISCLAIMER</p>'
        '<p style="color:#b91c1c;font-size:11px;line-height:1.65;margin:0;">'
        'This tool is <strong>NOT affiliated with Sungsimdang</strong>. '
        'Author is <strong>NOT a medical professional</strong>. '
        'This is <strong>reference information only</strong> — NOT medical advice. '
        'Always confirm allergen information <strong>directly with Sungsimdang staff '
        'in person</strong> before purchasing.</p>'
        '<p style="color:#b91c1c;font-size:11px;line-height:1.65;margin:6px 0 0;'
        'font-style:italic;">&#x1F3ED; '
        + FACILITY_NOTICE +
        '</p></div>'
        '</div></div>'

        '<div class="card-grid" id="card-grid"></div>'
        '<div id="empty-state" class="empty-state" style="display:none;">'
        '<p style="font-size:44px;margin:0 0 12px;">&#x1F645;</p>'
        '<p style="font-size:17px;font-weight:700;color:#78350f;margin:0 0 8px;">'
        'No breads match your current filters.</p>'
        '<p style="font-size:13px;">Try removing some allergens or changing the category filter.</p>'
        '</div>'

        '<script>'
        f'const data={bread_json};'
        f'const catColors={cat_colors_json};'
        f'const baseUrl="{GITHUB_BASE_URL}";'

        'function openModal(id){'
        'const b=data.find(x=>x.id===id);if(!b)return;'
        'const cc=catColors[b.category]||{bg:"#f3f4f6",border:"#d1d5db",text:"#374151"};'
        'const badge=document.getElementById("m-cat");'
        'badge.innerText=b.category;'
        'badge.style.background=cc.bg;'
        'badge.style.border="1.5px solid "+cc.border;'
        'badge.style.color=cc.text;'
        'document.getElementById("m-title").innerText=b.name;'
        'document.getElementById("m-ko").innerText=b.ko;'
        'document.getElementById("m-price").innerText="\\u20A9"+b.price+" KRW";'
        'document.getElementById("m-desc").innerText=b.description;'
        'document.getElementById("m-origin").innerText=b.origin;'
        'const c=document.getElementById("m-allergens");c.innerHTML="";'
        'b.allergens.forEach(a=>{const s=document.createElement("span");'
        's.className="chip chip-neutral";s.innerText=a;c.appendChild(s);});'
        'document.getElementById("modal").style.display="flex";'
        'document.body.style.overflow="hidden";}'

        'function closeModal(){'
        'document.getElementById("modal").style.display="none";'
        'document.body.style.overflow="";}'

        'document.addEventListener("keydown",e=>{if(e.key==="Escape")closeModal();});'

        'const grid=document.getElementById("card-grid");'
        'if(data.length===0){'
        'document.getElementById("empty-state").style.display="block";'
        '}else{'
        'data.forEach(bread=>{'
        'const cc=catColors[bread.category]||{bg:"#f3f4f6",border:"#d1d5db",text:"#374151"};'
        'const img=baseUrl+"images/"+bread.id+". "+bread.name+".png";'
        'const chipHtml=bread.allergens.slice(0,4).map('
        'a=>`<span class="chip chip-neutral">${a}</span>`).join("")'
        '+(bread.allergens.length>4'
        '?`<span style="font-size:10px;color:#9ca3af;font-weight:700;">'
        '+${bread.allergens.length-4} more</span>`:"");'
        'const card=document.createElement("div");'
        'card.className="bread-card";'
        'card.onclick=()=>openModal(bread.id);'
        'card.innerHTML=`'
        '<div style="height:185px;overflow:hidden;background:#f5f5f0;position:relative;">'
        '<img src="${encodeURI(img)}" style="width:100%;height:100%;object-fit:cover;"'
        ' onerror="this.style.display=\'none\';this.parentElement.style.display=\'flex\';'
        'this.parentElement.style.alignItems=\'center\';'
        'this.parentElement.style.justifyContent=\'center\';'
        'this.parentElement.innerHTML=\'<span style=font-size:44px>&#x1F956;</span>\';">'
        '<div style="position:absolute;top:8px;left:8px;background:${cc.bg};'
        'border:1.5px solid ${cc.border};color:${cc.text};border-radius:999px;'
        'font-size:9px;font-weight:800;padding:2px 10px;text-transform:uppercase;">'
        '${bread.category}</div>'
        '<div style="position:absolute;top:8px;right:8px;background:rgba(0,0,0,0.42);'
        'color:white;border-radius:999px;font-size:9px;font-weight:700;'
        'padding:2px 8px;">#${bread.id}</div>'
        '</div>'
        '<div style="padding:14px 16px 18px;display:flex;flex-direction:column;flex:1;">'
        '<h3 style="font-size:14px;font-weight:800;color:#1f2937;'
        'margin:0 0 2px;line-height:1.3;">${bread.name}</h3>'
        '<p style="font-size:11px;color:#b45309;font-weight:700;'
        'margin:0 0 5px;opacity:.75;">${bread.ko}</p>'
        '<p style="font-size:11px;color:#6b7280;line-height:1.5;'
        'margin:0 0 9px;flex:1;">${bread.description}</p>'
        '<div style="font-size:15px;font-weight:900;color:#d97706;margin-bottom:8px;">'
        '&#x20A9;${bread.price}</div>'
        '<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:11px;">'
        '${chipHtml}</div>'
        '<button style="width:100%;background:linear-gradient(135deg,#d97706,#78350f);'
        'color:white;border:none;border-radius:1rem;padding:10px;font-size:11px;'
        'font-weight:800;cursor:pointer;letter-spacing:.3px;transition:opacity .15s;"'
        ' onmouseover="this.style.opacity=\'.85\'"'
        ' onmouseout="this.style.opacity=\'1\'">'
        'View Full Details &#x2197;</button>'
        '</div>`;'
        'grid.appendChild(card);});}'
        '</script>'
        '</body></html>'
    )

    components.html(html_code, height=1350, scrolling=True)

    # ── 전체 요약 테이블 ──────────────────────
    st.markdown("---")
    st.markdown("### 📊 Complete Reference Table — All 29 Breads")
    st.caption(
        "Full database shown regardless of active filters above. "
        "Reference only — always verify allergen info with Sungsimdang staff in person."
    )
    table_rows = []
    for b in BREAD_DATA:
        flagged = any(a in b["allergens"] for a in avoid)
        table_rows.append({
            "Status":         "🚫 Hidden" if flagged else "✅ Shown",
            "#":              b["id"],
            "English Name":   b["name"],
            "Korean (한국어)": b["ko"],
            "Category":       b["category"],
            "Price (KRW)":    f"₩{b['price']}",
            "Allergens":      ", ".join(b["allergens"]),
            "Key Origins":    b["origin"],
        })
    st.dataframe(table_rows, use_container_width=True, hide_index=True)

    # ── 응급 정보 ─────────────────────────────
    st.markdown("---")
    with st.expander("🚨 Emergency Information for Travelers in Korea", expanded=False):
        st.markdown(
            '<div style="background:#fef2f2;border:2px solid #fca5a5;'
            'border-radius:16px;padding:20px 24px;">'
            '<p style="color:#991b1b;font-size:16px;font-weight:900;margin:0 0 12px;">'
            '&#x1F6A8; Save These Numbers Before You Travel</p>'
            '<ul style="color:#b91c1c;font-size:14px;line-height:2;'
            'margin:0 0 12px;padding-left:20px;">'
            '<li><strong>119</strong> — National Emergency (Fire / Ambulance / Medical). '
            'Say "English please" for translation support.</li>'
            '<li><strong>1339</strong> — Korea Disease Control &amp; Prevention Agency '
            'Medical Hotline.</li>'
            '<li><strong>1330</strong> — Korea Travel Helpline (Korea Tourism Organization). '
            'Available 24/7 in English, Japanese, Chinese, and more.</li>'
            '</ul>'
            '<p style="color:#991b1b;font-size:13px;font-weight:700;margin:0;">'
            'If you feel unwell after eating, call 119 immediately.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    # ── Data Source & Limitations 박스 ──────────
    st.markdown("---")
    st.markdown(
        '<div style="background:#fef2f2;border-left:5px solid #dc2626;'
        'border-radius:10px;padding:16px 20px;margin-bottom:14px;">'
        '<p style="margin:0 0 10px 0;color:#991b1b;font-size:13px;font-weight:800;">'
        '&#x1F4CB; Data Source &amp; Limitations</p>'
        '<p style="margin:0 0 10px 0;color:#991b1b;font-size:12px;line-height:1.7;">'
        '<strong>Source:</strong> The bread information in this tool is primarily based on '
        "Sungsimdang's publicly accessible online ordering app, which is provided in Korean. "
        'The author has translated this information into English with the help of various '
        'supporting references. <strong>This is not an official translation, and minor '
        'inaccuracies in translation or interpretation are possible.</strong></p>'
        '<p style="margin:0 0 10px 0;color:#991b1b;font-size:12px;line-height:1.7;">'
        '<strong>Update frequency:</strong> The author updates the tool periodically when '
        'changes are noticed in the source app. However, the tool may not always reflect the '
        'very latest formulations, prices, or product lineup. '
        f'<strong>Data last verified: {DATA_AS_OF}.</strong> '
        "For the most current information, please refer to Sungsimdang's official channels "
        'or ask staff in person.</p>'
        '<p style="margin:0;color:#991b1b;font-size:12px;line-height:1.7;">'
        '<strong>Limitation:</strong> The author has no special access to '
        "Sungsimdang's internal recipes or supplier lists, and is not affiliated with the "
        'company in any way. <strong>Do not rely solely on this tool for allergy decisions '
        '— always verify with staff in person.</strong> The author is not a medical '
        'professional and assumes no liability for any health consequences arising from '
        'the use of this guide.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── 하단 전체 면책 조항 ────────────────────
    st.markdown(
        '<div style="background:#fef2f2;border:2px solid #fca5a5;'
        'border-radius:16px;padding:20px 24px;margin-bottom:14px;">'
        '<p style="color:#991b1b;font-size:12px;font-weight:900;'
        'letter-spacing:.5px;margin:0 0 10px;">&#9888;&#65039; FULL DISCLAIMER &amp; TERMS OF USE</p>'
        '<p style="color:#b91c1c;font-size:11.5px;line-height:1.75;margin:0;">'
        'This guide is an <strong>independent, unofficial fan resource</strong> and is '
        '<strong>NOT affiliated with, endorsed by, or sponsored by Sungsimdang (성심당)</strong>. '
        'The author is <strong>NOT a medical professional, registered dietitian, or food scientist</strong>. '
        'This tool is provided for general informational and language-accessibility purposes only. '
        'It is <strong>NOT medical advice</strong>. Information may be outdated, incomplete, or contain '
        'translation inaccuracies. Sungsimdang may update recipes or suppliers without notice. '
        'Prices are subject to change without notice. '
        'Shared-facility cross-contamination is possible at any bakery. '
        '<strong>By using this tool, you accept sole responsibility for any decisions '
        'made regarding food consumption.</strong> Always confirm allergen information '
        'directly with Sungsimdang staff in person before purchasing. '
        'In a medical emergency in Korea, call <strong>119</strong>. '
        'For travel assistance, call <strong>1330</strong>.'
        '</p></div>',
        unsafe_allow_html=True
    )

    # ── 저작권 / Copyright ─────────────────────
    st.markdown(
        '<p style="text-align:center;color:#9ca3af;font-size:10.5px;'
        'margin:0 0 24px;line-height:1.6;">'
        '&copy; 2025. Independent fan guide. All rights reserved.<br>'
        'This guide is not affiliated with, endorsed by, or sponsored by Sungsimdang (성심당).<br>'
        f'Data last verified: {DATA_AS_OF}. Always confirm allergens with staff in person.'
        '</p>',
        unsafe_allow_html=True
    )
