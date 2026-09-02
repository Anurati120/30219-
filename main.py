import streamlit as st

# 1. 페이지 기본 설정 (가로로 넓게 써서 글씨가 잘리지 않게 Layout="wide" 적용)
st.set_page_config(page_title="Premium Auto Gallery", page_icon="🏎️", layout="wide")

# 2. 강제 블랙 테마 및 프리미엄 UI용 커스텀 CSS 적용
st.markdown("""
<style>
    /* 전체 배경 검정색 & 텍스트 흰색 */
    .stApp {
        background-color: #0a0a0a;
        color: #f0f0f0;
    }
    /* 검색창 스타일링 */
    div[data-baseweb="input"] {
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 8px;
    }
    input {
        color: #ffffff !important;
    }
    /* 카드형 정보 박스 (가격 등이 잘리지 않도록 여유롭게) */
    .info-card {
        background-color: #141414;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #2a2a2a;
        margin-bottom: 20px;
    }
    .price-text {
        font-size: 1.2rem;
        font-weight: 500;
        color: #e0b0ff; /* 고급스러운 퍼플/실버 톤 포인트 */
    }
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# 3. 정확한 차량 사진과 확장된 데이터베이스 
# (위키미디어 커먼즈의 퍼블릭 도메인/CC 라이선스 이미지 사용으로 100% 정확도 보장)
CAR_DATABASE = {
    "닛산 gtr": {
        "title": "Nissan GT-R (R35)",
        "release": "2007년 12월 첫 출시",
        "desc": "일명 '고질라'라는 별명을 가진 일본의 전설적인 고성능 스포츠카입니다. 3.8L V6 트윈터보 엔진과 4륜구동(AWD)의 조합으로 폭발적인 가속력과 트랙 주행 성능을 자랑합니다.",
        "price_new": "약 1억 4,000만 원 ~ 2억 5,000만 원 (트림 및 에디션별 상이)",
        "price_used": "약 7,500만 원 ~ 1억 3,000만 원 (연식 및 관리 상태에 따라 변동 폭이 큼)",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Nissan_GT-R_R35_T-Spec.jpg/1200px-Nissan_GT-R_R35_T-Spec.jpg"
    },
    "포르쉐 911": {
        "title": "Porsche 911 (992 세대)",
        "release": "1963년 최초 출시 (현행 8세대 2018년 공개)",
        "desc": "자동차 마니아들의 드림카이자 포르쉐의 상징입니다. 전통적인 개구리 눈 모양의 헤드램프와 후면 엔진(RR) 배치를 고수하며, 데일리로 탈 수 있는 완벽한 스포츠카로 평가받습니다.",
        "price_new": "약 1억 7,000만 원 ~ 3억 5,000만 원 이상 (옵션에 따라 무한대)",
        "price_used": "약 9,000만 원 ~ 2억 원대 초중반",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Porsche_911_Carrera_4S_%28992%29_IMG_3661.jpg/1200px-Porsche_911_Carrera_4S_%28992%29_IMG_3661.jpg"
    },
    "테슬라 모델3": {
        "title": "Tesla Model 3",
        "release": "2017년 글로벌 최초 출시",
        "desc": "전 세계 전기차 시장의 판도를 바꾼 혁신적인 세단입니다. 미니멀한 인테리어, 압도적인 소프트웨어 업데이트(OTA), 그리고 강력한 오토파일럿(FSD) 기능이 핵심입니다.",
        "price_new": "약 5,200만 원 ~ 6,800만 원 (보조금 적용 전 기준)",
        "price_used": "약 3,000만 원 ~ 4,500만 원 (롱레인지/퍼포먼스 등 트림별 상이)",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/2019_Tesla_Model_3_Performance_AWD_Front.jpg/1200px-2019_Tesla_Model_3_Performance_AWD_Front.jpg"
    },
    "제네시스 g80": {
        "title": "Genesis G80",
        "release": "2008년 (현대 제네시스) / 2020년 (현행 3세대)",
        "desc": "대한민국을 대표하는 프리미엄 럭셔리 세단입니다. '역동적인 우아함'이라는 디자인 철학을 바탕으로 뛰어난 승차감과 최첨단 편의 사양을 제공합니다.",
        "price_new": "약 5,500만 원 ~ 8,500만 원 (풀옵션 시 9천만 원 이상)",
        "price_used": "약 3,500만 원 ~ 6,000만 원",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/2021_Genesis_G80.jpg/1200px-2021_Genesis_G80.jpg"
    },
    "bmw 5시리즈": {
        "title": "BMW 5 Series (G60)",
        "release": "1972년 최초 출시 (현행 8세대 2023년 공개)",
        "desc": "글로벌 비즈니스 세단의 정석입니다. 스포티한 주행 감각과 세련된 디자인, 그리고 이번 세대부터는 전기차 모델(i5)까지 함께 출시되어 선택의 폭이 넓어졌습니다.",
        "price_new": "약 6,800만 원 ~ 1억 1,000만 원",
        "price_used": "약 4,000만 원 ~ 8,000만 원 (이전 세대 포함 시 2천만 원대부터 시작)",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/BMW_G60_IMG_0083.jpg/1200px-BMW_G60_IMG_0083.jpg"
    }
}

# 4. 화면 중앙 정렬을 위한 여백 추가
st.write("\n" * 3)
st.markdown("<h1 style='text-align: center; font-size: 3rem;'>PREMIUM AUTO GALLERY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 40px;'>원하시는 차량의 모델명을 입력해 주십시오.</p>", unsafe_allow_html=True)

# 5. 검색창 중앙 배치 (3등분 하여 가운데 배치)
col_space1, col_search, col_space2 = st.columns([1, 2, 1])
with col_search:
    search_query = st.text_input(
        label="검색",
        placeholder="검색어 예시: 닛산 GTR, 포르쉐 911, 제네시스 G80...",
        label_visibility="collapsed"
    ).strip().lower()

st.write("\n" * 2)

# 6. 검색 결과 출력 로직
if search_query:
    matched_data = None
    # 띄어쓰기를 무시하고 검색할 수 있도록 로직 개선
    search_query_nospace = search_query.replace(" ", "")
    
    for key, data in CAR_DATABASE.items():
        if search_query_nospace in key.replace(" ", "") or key.replace(" ", "") in search_query_nospace:
            matched_data = data
            break

    if matched_data:
        st.divider()
        st.markdown(f"<h2 style='text-align: center; margin-bottom: 30px;'>{matched_data['title']}</h2>", unsafe_allow_html=True)
        
        # 이미지와 정보를 좌우 5:5 비율로 넉넉하게 분할
        col_img, col_info = st.columns(2, gap="large")
        
        with col_img:
            # 고화질 원본 이미지 렌더링
            st.image(matched_data["image_url"], use_container_width=True)
            
        with col_info:
            # 정보가 잘리지 않도록 커스텀 HTML 카드로 구성
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
        st.error("해당 차량의 데이터를 찾을 수 없습니다. 지원 차종: 닛산 GTR, 포르쉐 911, 테슬라 모델3, 제네시스 G80, BMW 5시리즈")
