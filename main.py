import streamlit as st

# 1. 페이지 설정 (넓은 레이아웃)
st.set_page_config(page_title="Premium Auto Gallery", page_icon="🏎️", layout="wide")

# 2. UI/UX 개선을 위한 커스텀 CSS (검색창 글씨 검정색 수정, 고급스러운 첫 화면)
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #f0f0f0; }
    /* 검색창 배경 흰색, 글씨 검정색으로 강제 고정하여 가독성 100% 확보 */
    div[data-baseweb="input"] > div { background-color: #ffffff !important; }
    input { color: #000000 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    
    .info-card { background-color: #141414; padding: 25px; border-radius: 12px; border: 1px solid #2a2a2a; margin-bottom: 20px; }
    .price-text { font-size: 1.2rem; font-weight: 500; color: #e0b0ff; }
    .hero-title { text-align: center; font-size: 3.5rem; font-weight: 900; background: -webkit-linear-gradient(#eee, #333); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;}
</style>
""", unsafe_allow_html=True)

# 3. 확장된 자동차 데이터베이스 (안정적인 이미지 링크로 교체 및 10개 차종 세팅)
CAR_DATABASE = {
    "닛산 gtr": {
        "title": "Nissan GT-R (R35)",
        "release": "2007년 12월",
        "desc": "일명 '고질라'. 3.8L V6 트윈터보 엔진을 탑재한 일본의 전설적인 슈퍼카입니다.",
        "price_new": "약 1억 4,000만 ~ 2억 5,000만 원", "price_used": "약 7,500만 ~ 1억 3,000만 원",
        "image_url": "https://images.unsplash.com/photo-1629897048514-3dd741427139?w=800&q=80"
    },
    "포르쉐 911": {
        "title": "Porsche 911 (992)",
        "release": "1963년 최초 출시 (현행 8세대)",
        "desc": "후면 엔진(RR) 구조를 고수하는 포르쉐의 상징이자 데일리 스포츠카의 정석입니다.",
        "price_new": "약 1억 7,000만 원 이상", "price_used": "약 9,000만 ~ 2억 원대",
        "image_url": "https://images.unsplash.com/photo-1503376712341-ea7823f0340a?w=800&q=80"
    },
    "테슬라 모델3": {
        "title": "Tesla Model 3",
        "release": "2017년",
        "desc": "전기차의 대중화를 이끈 혁신적인 중형 세단. 압도적인 오토파일럿이 특징입니다.",
        "price_new": "약 5,200만 ~ 6,800만 원", "price_used": "약 3,000만 ~ 4,500만 원",
        "image_url": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&q=80"
    },
    "제네시스 g80": {
        "title": "Genesis G80",
        "release": "2020년 (3세대)",
        "desc": "역동적인 우아함을 강조한 대한민국의 대표 프리미엄 럭셔리 세단입니다.",
        "price_new": "약 5,500만 ~ 8,500만 원", "price_used": "약 3,500만 ~ 6,000만 원",
        "image_url": "https://images.unsplash.com/photo-1619405399517-d7fce0f13302?w=800&q=80"
    },
    "bmw 5시리즈": {
        "title": "BMW 5 Series",
        "release": "2023년 (8세대)",
        "desc": "스포티한 주행 감각을 자랑하는 글로벌 베스트셀링 비즈니스 세단입니다.",
        "price_new": "약 6,800만 ~ 1억 1,000만 원", "price_used": "약 4,000만 ~ 8,000만 원",
        "image_url": "https://images.unsplash.com/photo-1555097486-cb8292866b59?w=800&q=80"
    },
    "현대 그랜저": {
        "title": "Hyundai Grandeur (GN7)",
        "release": "2022년 11월 (7세대)",
        "desc": "대한민국 성공의 상징. 미래지향적인 '끊김없는 호라이즌 램프'가 특징인 플래그십 세단입니다.",
        "price_new": "약 3,700만 ~ 5,500만 원", "price_used": "약 2,800만 ~ 4,500만 원",
        "image_url": "https://images.unsplash.com/photo-1673857827827-2c9e78fb5635?w=800&q=80"
    },
    "메르세데스 벤츠 e클래스": {
        "title": "Mercedes-Benz E-Class",
        "release": "2023년 (11세대)",
        "desc": "수입차 판매 1위를 다투는 벤츠의 핵심 모델로, 럭셔리한 실내와 부드러운 승차감이 일품입니다.",
        "price_new": "약 7,300만 ~ 1억 3,000만 원", "price_used": "약 4,000만 ~ 9,000만 원",
        "image_url": "https://images.unsplash.com/photo-1616422285623-14bf73f85955?w=800&q=80"
    },
    "포드 머스탱": {
        "title": "Ford Mustang",
        "release": "1964년 (현행 7세대)",
        "desc": "아메리칸 머슬카의 아이콘. 거친 V8 엔진 배기음과 스포티한 디자인이 매력적입니다.",
        "price_new": "약 5,900만 ~ 8,600만 원", "price_used": "약 3,000만 ~ 6,000만 원",
        "image_url": "https://images.unsplash.com/photo-1584345604476-8cc5e302029b?w=800&q=80"
    },
    "아우디 a6": {
        "title": "Audi A6",
        "release": "2018년 (8세대)",
        "desc": "세련된 조명 기술과 기계식 콰트로(사륜구동) 시스템을 바탕으로 한 독일 프리미엄 세단입니다.",
        "price_new": "약 7,000만 ~ 9,500만 원", "price_used": "약 3,500만 ~ 6,000만 원",
        "image_url": "https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?w=800&q=80"
    },
    "기아 쏘렌토": {
        "title": "Kia Sorento",
        "release": "2020년 (4세대, 페이스리프트 진행)",
        "desc": "넓은 실내 공간과 하이브리드 파워트레인으로 대한민국 패밀리 SUV 시장을 장악한 모델입니다.",
        "price_new": "약 3,500만 ~ 4,800만 원", "price_used": "약 2,500만 ~ 4,000만 원",
        "image_url": "https://images.unsplash.com/photo-1632734185791-766a506bb03c?w=800&q=80"
    }
}

# 4. 헤더 및 검색창
st.write("\n")
st.markdown("<h1 class='hero-title'>PREMIUM AUTO GALLERY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; font-size: 1.1rem;'>현대 그랜저, 벤츠 E클래스, 포드 머스탱 등을 검색해보세요.</p>", unsafe_allow_html=True)

st.write("\n")
col1, col_search, col3 = st.columns([1, 2, 1])
with col_search:
    search_query = st.text_input("검색어", placeholder="차량 이름을 입력하세요 (예: 그랜저, 머스탱, g80)", label_visibility="collapsed").strip().lower()

# 5. 검색 결과 OR 첫 화면(추천 차량) 로직
st.write("\n")

if search_query:
    matched_data = None
    search_query_nospace = search_query.replace(" ", "")
    for key, data in CAR_DATABASE.items():
        if search_query_nospace in key.replace(" ", "") or key.replace(" ", "") in search_query_nospace:
            matched_data = data
            break

    if matched_data:
        st.divider()
        st.markdown(f"<h2 style='text-align: center;'>{matched_data['title']}</h2>", unsafe_allow_html=True)
        col_img, col_info = st.columns(2, gap="large")
        
        with col_img:
            # 에러 방지를 위해 Unsplash의 가장 안정적인 URL 구조 사용
            st.image(matched_data["image_url"], use_container_width=True)
            
        with col_info:
            st.markdown(f"""
            <div class="info-card">
                <h3 style="margin-top: 0;">📅 History & Specs</h3>
                <p><b>출시 시기:</b> {matched_data['release']}</p>
                <p><b>상세 설명:</b> {matched_data['desc']}</p>
            </div>
            <div class="info-card">
                <h3 style="margin-top: 0;">💰 Market Value</h3>
                <p><b>신차 출고가:</b><br><span class="price-text">{matched_data['price_new']}</span></p>
                <p><b>중고차 시세:</b><br><span class="price-text">{matched_data['price_used']}</span></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error(f"'{search_query}'에 대한 데이터를 찾을 수 없습니다. (현재 등록된 차량: GTR, 911, 모델3, G80, 5시리즈, 그랜저, E클래스, 머스탱, A6, 쏘렌토)")
else:
    # 6. 검색어가 없을 때 보여주는 첫 화면 (갤러리 뷰)
    st.divider()
    st.markdown("<h3 style='text-align: center; color: #fff;'>✨ Featured Vehicles</h3>", unsafe_allow_html=True)
    st.write("\n")
    
    # 3개의 열로 나누어 추천 차량 3대 전시
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.image(CAR_DATABASE["포르쉐 911"]["image_url"], use_container_width=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>포르쉐 911</p>", unsafe_allow_html=True)
    with feat_col2:
        st.image(CAR_DATABASE["현대 그랜저"]["image_url"], use_container_width=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>현대 그랜저</p>", unsafe_allow_html=True)
    with feat_col3:
        st.image(CAR_DATABASE["포드 머스탱"]["image_url"], use_container_width=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>포드 머스탱</p>", unsafe_allow_html=True)
