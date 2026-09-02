import streamlit as st

# 1. 페이지 설정 (와이드 레이아웃)
st.set_page_config(page_title="Premium Auto Gallery", page_icon="🏎️", layout="wide")

# 2. 고급스러운 블랙 테마 및 텍스트/카드 디자인 CSS
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #f0f0f0; }
    
    /* 검색창 가독성 최우선 세팅 */
    div[data-baseweb="input"] > div { background-color: #ffffff !important; }
    input { color: #000000 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    
    /* 정보 카드 박스 */
    .info-card { 
        background-color: #141414; 
        padding: 25px; 
        border-radius: 12px; 
        border: 1px solid #2a2a2a; 
        margin-bottom: 20px; 
    }
    .price-text { 
        font-size: 1.2rem; 
        font-weight: 600; 
        color: #e0b0ff; 
    }
    .hero-title { 
        text-align: center; 
        font-size: 3.2rem; 
        font-weight: 900; 
        color: #ffffff;
        margin-bottom: 0;
    }
    /* 차량 카드 이미지 스타일링 */
    .car-img-box {
        width: 100%;
        height: 380px;
        object-fit: cover;
        border-radius: 12px;
        border: 1px solid #333333;
    }
</style>
""", unsafe_allow_html=True)

# 3. 로딩 에러 원천 차단을 위해 가장 안정적이고 깨끗한 공식 자동차 고화질 이미지로 교체
CAR_DATABASE = {
    "닛산 gtr": {
        "title": "Nissan GT-R (R35)",
        "release": "2007년 12월",
        "desc": "일명 '고질라'. 3.8L V6 트윈터보 엔진을 탑재한 일본의 전설적인 슈퍼카입니다.",
        "price_new": "약 1억 4,000만 ~ 2억 5,000만 원", "price_used": "약 7,500만 ~ 1억 3,000만 원",
        "image_url": "https://images.unsplash.com/photo-1607853585095-26e955f2f53b?w=1000&q=80"
    },
    "포르쉐 911": {
        "title": "Porsche 911 (992)",
        "release": "1963년 최초 출시 (현행 8세대)",
        "desc": "후면 엔진(RR) 구조를 고수하는 포르쉐의 상징이자 데일리 스포츠카의 정석입니다.",
        "price_new": "약 1억 7,000만 원 이상", "price_used": "약 9,000만 ~ 2억 원대",
        "image_url": "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=1000&q=80"
    },
    "테슬라 모델3": {
        "title": "Tesla Model 3",
        "release": "2017년",
        "desc": "전기차의 대중화를 이끈 혁신적인 중형 세단. 압도적인 오토파일럿이 특징입니다.",
        "price_new": "약 5,200만 ~ 6,800만 원", "price_used": "약 3,000만 ~ 4,500만 원",
        "image_url": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=1000&q=80"
    },
    "제네시스 g80": {
        "title": "Genesis G80",
        "release": "2020년 (3세대)",
        "desc": "역동적인 우아함을 강조한 대한민국의 대표 프리미엄 럭셔리 세단입니다.",
        "price_new": "약 5,500만 ~ 8,500만 원", "price_used": "약 3,500만 ~ 6,000만 원",
        "image_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=1000&q=80"
    },
    "bmw 5시리즈": {
        "title": "BMW 5 Series",
        "release": "2023년 (8세대)",
        "desc": "스포티한 주행 감각을 자랑하는 글로벌 베스트셀링 비즈니스 세단입니다.",
        "price_new": "약 6,800만 ~ 1억 1,000만 원", "price_used": "약 4,000만 ~ 8,000만 원",
        "image_url": "https://images.unsplash.com/photo-1555097486-cb8292866b59?w=1000&q=80"
    },
    "현대 그랜저": {
        "title": "Hyundai Grandeur (GN7)",
        "release": "2022년 11월 (7세대)",
        "desc": "대한민국 성공의 상징. 미래지향적인 '끊김없는 호라이즌 램프'가 특징인 플래그십 세단입니다.",
        "price_new": "약 3,700만 ~ 5,500만 원", "price_used": "약 2,800만 ~ 4,500만 원",
        "image_url": "https://images.unsplash.com/photo-1629897048514-3dd741427139?w=1000&q=80"
    },
    "메르세데스 벤츠 e클래스": {
        "title": "Mercedes-Benz E-Class",
        "release": "2023년 (11세대)",
        "desc": "수입차 판매 1위를 다투는 벤츠의 핵심 모델로, 럭셔리한 실내와 부드러운 승차감이 일품입니다.",
        "price_new": "약 7,300만 ~ 1억 3,000만 원", "price_used": "약 4,000만 ~ 9,000만 원",
        "image_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=1000&q=80"
    },
    "포드 머스탱": {
        "title": "Ford Mustang",
        "release": "1964년 (현행 7세대)",
        "desc": "아메리칸 머슬카의 아이콘. 거친 V8 엔진 배기음과 스포티한 디자인이 매력적입니다.",
        "price_new": "약 5,900만 ~ 8,600만 원", "price_used": "약 3,000만 ~ 6,000만 원",
        "image_url": "https://images.unsplash.com/photo-1584345604476-8cc5e302029b?w=1000&q=80"
    },
    "아우디 a6": {
        "title": "Audi A6",
        "release": "2018년 (8세대)",
        "desc": "세련된 조명 기술과 기계식 콰트로(사륜구동) 시스템을 바탕으로 한 독일 프리미엄 세단입니다.",
        "price_new": "약 7,000만 ~ 9,500만 원", "price_used": "약 3,500만 ~ 6,000만 원",
        "image_url": "https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?w=1000&q=80"
    },
    "기아 쏘렌토": {
        "title": "Kia Sorento",
        "release": "2020년 (4세대, 페이스리프트)",
        "desc": "넓은 실내 공간과 하이브리드 파워트레인으로 대한민국 패밀리 SUV 시장을 장악한 모델입니다.",
        "price_new": "약 3,500만 ~ 4,800만 원", "price_used": "약 2,500만 ~ 4,000만 원",
        "image_url": "https://images.unsplash.com/photo-1632734185791-766a506bb03c?w=1000&q=80"
    }
}

# 4. 헤더 및 검색창 UI
st.write("\n")
st.markdown("<h1 class='hero-title'>PREMIUM AUTO GALLERY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.1rem;'>원하시는 차량의 이름을 검색하여 상세 정보를 확인하세요.</p>", unsafe_allow_html=True)

st.write("\n")
col_space1, col_search, col_space2 = st.columns([1, 2, 1])
with col_search:
    search_query = st.text_input("검색", placeholder="🔍 예: 그랜저, 벤츠 E클래스, 머스탱, GTR...", label_visibility="collapsed").strip().lower()

st.write("\n")

# 5. 검색 및 결과 렌더링 로직
if search_query:
    matched_data = None
    search_query_nospace = search_query.replace(" ", "")
    for key, data in CAR_DATABASE.items():
        if search_query_nospace in key.replace(" ", "") or key.replace(" ", "") in search_query_nospace:
            matched_data = data
            break

    if matched_data:
        st.divider()
        st.markdown(f"<h2 style='text-align: center; margin-bottom: 25px;'>{matched_data['title']}</h2>", unsafe_allow_html=True)
        
        col_img, col_info = st.columns(2, gap="large")
        
        with col_img:
            # HTML 태그를 사용해 이미지 로딩 오류를 방지하고 일정한 크기로 예쁘게 출력
            st.markdown(f"""
                <img src="{matched_data['image_url']}" class="car-img-box">
            """, unsafe_allow_html=True)
            
        with col_info:
            st.markdown(f"""
            <div class="info-card">
                <h3 style="margin-top: 0; color: #fff;">📅 History & Specs</h3>
                <p style="color: #ccc;"><b>출시 시기:</b> {matched_data['release']}</p>
                <p style="color: #ccc;"><b>상세 설명:</b> {matched_data['desc']}</p>
            </div>
            <div class="info-card">
                <h3 style="margin-top: 0; color: #fff;">💰 Market Value</h3>
                <p style="color: #ccc;"><b>신차 출고가:</b><br><span class="price-text">{matched_data['price_new']}</span></p>
                <p style="color: #ccc;"><b>중고차 시세:</b><br><span class="price-text">{matched_data['price_used']}</span></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error(f"'{search_query}'에 대한 차량 정보를 찾을 수 없습니다. (등록된 차량: 닛산 GTR, 포르쉐 911, 모델3, G80, 5시리즈, 그랜저, E클래스, 머스탱, A6, 쏘렌토)")
else:
    # 6. 첫 화면 추천 갤러리 뷰
    st.divider()
    st.markdown("<h3 style='text-align: center; color: #fff;'>✨ Featured Vehicles</h3>", unsafe_allow_html=True)
    st.write("\n")
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown(f'<img src="{CAR_DATABASE["포르쉐 911"]["image_url"]}" style="width:100%; height:220px; object-fit:cover; border-radius:8px;">', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold; margin-top: 10px;'>포르쉐 911</p>", unsafe_allow_html=True)
    with feat_col2:
        st.markdown(f'<img src="{CAR_DATABASE["현대 그랜저"]["image_url"]}" style="width:100%; height:220px; object-fit:cover; border-radius:8px;">', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold; margin-top: 10px;'>현대 그랜저</p>", unsafe_allow_html=True)
    with feat_col3:
        st.markdown(f'<img src="{CAR_DATABASE["포드 머스탱"]["상태"] if "상태" in CAR_DATABASE["포드 머스탱"] else CAR_DATABASE["포드 머스탱"]["image_url"]}" style="width:100%; height:220px; object-fit:cover; border-radius:8px;">', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold; margin-top: 10px;'>포드 머스탱</p>", unsafe_allow_html=True)
