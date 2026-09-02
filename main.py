import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="NEON AUTO VAULT", page_icon="🏎️", layout="wide")

# 2. 스타일링 CSS
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at center, #111118 0%, #050508 100%);
        color: #e0e0e0;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .hero-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .hero-subtitle {
        text-align: center;
        color: #8b8b9e;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }

    /* 검색창 배경 흰색 + 글씨 검정색 강제 고정 */
    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border: 2px solid #4facfe !important;
        border-radius: 16px !important;
        box-shadow: 0 0 20px rgba(79, 172, 254, 0.4);
    }
    input {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }

    /* 글래스모피즘 정보 카드 */
    .glass-card {
        background: rgba(18, 18, 28, 0.8);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .typo-box {
        width: 100%;
        height: 380px;
        background: linear-gradient(135deg, #161625 0%, #0b0b12 100%);
        border-radius: 20px;
        border: 2px solid rgba(79, 172, 254, 0.3);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.7);
        text-align: center;
        padding: 20px;
    }

    .gallery-typo-box {
        width: 100%;
        height: 200px;
        background: linear-gradient(135deg, #161625 0%, #0b0b12 100%);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        padding: 10px;
    }
    .gallery-typo-box:hover {
        transform: translateY(-5px);
        border-color: #4facfe;
        box-shadow: 0 10px 25px rgba(79, 172, 254, 0.2);
    }

    .price-highlight {
        font-size: 1.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-header {
        color: #ffffff;
        font-weight: 700;
        border-bottom: 2px solid #2d2d44;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 통합 차량 데이터베이스 (기아 전 차종 + 람보르기니 + 기존 주요 차량)
CAR_DATABASE = {
    # --- 람보르기니 라인업 ---
    "람보르기니 아벤타도르": {
        "title": "Lamborghini Aventador", "brand": "LAMBORGHINI", "release": "2011년 출시",
        "desc": "자연흡기 V12 엔진의 황홀한 배기음과 시그니처 시저 도어를 탑재한 플래그십 V12 슈퍼카입니다.",
        "price_new": "약 5억 ~ 6억 원대 이상", "price_used": "약 4억 ~ 5억 5,000만 원",
        "typo_html": '<div style="font-size: 3.2rem; font-weight: 900; color: #f39c12; letter-spacing: 2px; text-shadow: 0 0 25px rgba(243,156,18,0.6);">AVENTADOR</div><div style="font-size: 0.9rem; color: #a0a0b0; font-weight: 600; letter-spacing: 6px; margin-top: 10px;">LAMBORGHINI V12</div>'
    },
    "람보르기니 우라칸": {
        "title": "Lamborghini Huracan", "brand": "LAMBORGHINI", "release": "2014년 출시",
        "desc": "경쾌한 고회전 NA V10 엔진을 품은 베스트셀링 슈퍼카로, 짜릿한 드라이빙 퍼포먼스를 제공합니다.",
        "price_new": "약 3억 ~ 4억 원대", "price_used": "약 2억 5,000만 ~ 3억 5,000만 원",
        "typo_html": '<div style="font-size: 3.5rem; font-weight: 900; color: #e74c3c; letter-spacing: 3px; text-shadow: 0 0 25px rgba(231,76,60,0.6);">HURACAN</div><div style="font-size: 0.9rem; color: #a0a0b0; font-weight: 600; letter-spacing: 6px; margin-top: 10px;">V10 SUPERCAR</div>'
    },
    "람보르기니 우루스": {
        "title": "Lamborghini Urus S / Performante", "brand": "LAMBORGHINI", "release": "2018년 출시",
        "desc": "슈퍼카의 DNA를 이식받은 고성능 럭셔리 SUV의 끝판왕. 강력한 트윈터보 V8 파워를 자랑합니다.",
        "price_new": "약 3억 ~ 3억 6,000만 원+", "price_used": "약 2억 8,000만 ~ 3억 3,000만 원",
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #f1c40f; letter-spacing: 6px; text-shadow: 0 0 25px rgba(241,196,15,0.6);">URUS</div><div style="font-size: 0.9rem; color: #a0a0b0; font-weight: 600; letter-spacing: 6px; margin-top: 10px;">SUPER SUV</div>'
    },
    "람보르기니 레부엘토": {
        "title": "Lamborghini Revuelto", "brand": "LAMBORGHINI", "release": "2023년 공개",
        "desc": "아벤타도르의 뒤를 잇는 V12 자연흡기 기반의 고성능 하이브리드(HPEV) 플래그십 슈퍼카입니다.",
        "price_new": "약 7억 원대~", "price_used": "매물 희귀",
        "typo_html": '<div style="font-size: 3rem; font-weight: 900; color: #9b59b6; letter-spacing: 3px; text-shadow: 0 0 25px rgba(155,89,182,0.6);">REVUELTO</div><div style="font-size: 0.9rem; color: #a0a0b0; font-weight: 600; letter-spacing: 6px; margin-top: 10px;">V12 HYBRID HPEV</div>'
    },

    # --- 기아 전 차종 라인업 ---
    "기아 모닝": {
        "title": "Kia Morning (The New Morning)", "brand": "KIA", "release": "2004년 최초 출시",
        "desc": "도심 주행과 뛰어난 경제성을 자랑하는 대한민국 대표 경차입니다.",
        "price_new": "약 1,300만 ~ 1,650만 원", "price_used": "약 800만 ~ 1,300만 원",
        "typo_html": '<div style="font-size: 3.8rem; font-weight: 900; color: #2ecc71; letter-spacing: 6px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ MORNING</div>'
    },
    "기아 레이": {
        "title": "Kia Ray (The New Ray)", "brand": "KIA", "release": "2011년 최초 출시",
        "desc": "박스형 디자인과 조수석 슬라이딩 도로 광활한 실내 공간을 자랑하는 경차입니다.",
        "price_new": "약 1,350만 ~ 1,800만 원", "price_used": "약 900만 ~ 1,450만 원",
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #2ecc71; letter-spacing: 6px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ RAY</div>'
    },
    "기아 k3": {
        "title": "Kia K3", "brand": "KIA", "release": "2012년 출시",
        "desc": "세련된 디자인과 뛰어난 연비를 갖춘 준중형 세단입니다.",
        "price_new": "약 1,800만 ~ 2,600만 원", "price_used": "약 1,100만 ~ 2,100만 원",
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #2ecc71; letter-spacing: 6px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ K3</div>'
    },
    "기아 k5": {
        "title": "Kia K5 (The New K5)", "brand": "KIA", "release": "2010년 최초 출시",
        "desc": "스포티하고 역동적인 패스트백 스타일 디자인으로 사랑받는 중형 세단입니다.",
        "price_new": "약 2,400만 ~ 3,900만 원", "price_used": "약 1,500만 ~ 3,200만 원",
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #2ecc71; letter-spacing: 6px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ K5</div>'
    },
    "기아 k8": {
        "title": "Kia K8", "brand": "KIA", "release": "2021년 출시",
        "desc": "고급스러움과 혁신적인 첨단 사양이 조화로운 기아의 준대형 세단입니다.",
        "price_new": "약 3,300만 ~ 5,200만 원", "price_used": "약 2,500만 ~ 4,200만 원",
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #2ecc71; letter-spacing: 6px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ K8</div>'
    },
    "기아 k9": {
        "title": "Kia K9", "brand": "KIA", "release": "2012년 출시",
        "desc": "최상급 승차감과 정숙성을 자랑하는 기아의 플래그십 대형 세단입니다.",
        "price_new": "약 5,900만 ~ 8,800만 원", "price_used": "약 3,500만 ~ 7,000만 원",
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #2ecc71; letter-spacing: 6px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ K9</div>'
    },
    "기아 셀토스": {
        "title": "Kia Seltos", "brand": "KIA", "release": "2019년 출시",
        "desc": "소형 SUV 시장에서 탄탄한 주행 성능과 넓은 공간으로 압도적 인기를 누리는 모델입니다.",
        "price_new": "약 2,100만 ~ 3,000만 원", "price_used": "약 1,500만 ~ 2,500만 원",
        "typo_html": '<div style="font-size: 3.5rem; font-weight: 900; color: #2ecc71; letter-spacing: 4px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ SELTOS</div>'
    },
    "기아 니로": {
        "title": "Kia Niro (Hybrid / EV)", "brand": "KIA", "release": "2016년 출시",
        "desc": "친환경 전용 플랫폼으로 뛰어난 연비와 실용성을 겸비한 친환경 SUV입니다.",
        "price_new": "약 2,700만 ~ 5,000만 원", "price_used": "약 1,600만 ~ 3,800만 원",
        "typo_html": '<div style="font-size: 3.8rem; font-weight: 900; color: #2ecc71; letter-spacing: 5px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ NIRO</div>'
    },
    "기아 스포티지": {
        "title": "Kia Sportage (5세대)", "brand": "KIA", "release": "1993년 최초 출시",
        "desc": "혁신적인 디자인과 다재다능한 공간을 갖춘 대한민국 대표 준중형 SUV입니다.",
        "price_new": "약 2,500만 ~ 4,000만 원", "price_used": "약 1,700만 ~ 3,400만 원",
        "typo_html": '<div style="font-size: 3.2rem; font-weight: 900; color: #2ecc71; letter-spacing: 4px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ SPORTAGE</div>'
    },
    "기아 쏘렌토": {
        "title": "Kia Sorento (Hybrid)", "brand": "KIA", "release": "2020년 4세대",
        "desc": "대한민국 패밀리 SUV 시장의 독보적인 1위. 뛰어난 공간 활용성이 강점입니다.",
        "price_new": "약 3,500만 ~ 4,800만 원", "price_used": "약 2,500만 ~ 4,000만 원",
        "typo_html": '<div style="font-size: 3.2rem; font-weight: 900; color: #2ecc71; letter-spacing: 4px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ SORENTO</div>'
    },
    "기아 모하비": {
        "title": "Kia Mohave", "brand": "KIA", "release": "2008년 출시",
        "desc": "정통 프레임 바디와 V6 3.0 디젤 엔진의 묵직한 주행감을 자랑하는 대형 SUV입니다.",
        "price_new": "약 5,000만 ~ 6,000만 원대", "price_used": "약 2,800만 ~ 4,800만 원",
        "typo_html": '<div style="font-size: 3.5rem; font-weight: 900; color: #2ecc71; letter-spacing: 4px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ MOHAVE</div>'
    },
    "기아 카니발": {
        "title": "Kia Carnival", "brand": "KIA", "release": "1998년 최초 출시",
        "desc": "대체불가능한 대한민국 아빠들의 영원한 드림카, 패밀리 미니밴의 표준입니다.",
        "price_new": "약 3,500만 ~ 5,000만 원+", "price_used": "약 2,200만 ~ 4,200만 원",
        "typo_html": '<div style="font-size: 3.2rem; font-weight: 900; color: #2ecc71; letter-spacing: 4px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ CARNIVAL</div>'
    },
    "기아 스팅어": {
        "title": "Kia Stinger", "brand": "KIA", "release": "2017년 출시 (단종)",
        "desc": "국산 후륜구동 스포츠 세단의 지평을 열었던 매력적인 고성능 모델입니다.",
        "price_new": "단종 (출고가 약 3,900만 ~ 5,500만 원)", "price_used": "약 2,200만 ~ 4,000만 원",
        "typo_html": '<div style="font-size: 3.5rem; font-weight: 900; color: #2ecc71; letter-spacing: 4px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ STINGER</div>'
    },
    "기아 ev3": {
        "title": "Kia EV3", "brand": "KIA", "release": "2024년 출시",
        "desc": "기아의 보급형 전기차 대중화를 이끄는 컴팩트 순수 전기 SUV입니다.",
        "price_new": "약 3,900만 ~ 5,000만 원", "price_used": "약 3,200만 ~ 4,200만 원",
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #2ecc71; letter-spacing: 6px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ EV3</div>'
    },
    "기아 ev6": {
        "title": "Kia EV6 (GT 포함)", "brand": "KIA", "release": "2021년 출시",
        "desc": "초고속 충전 시스템과 압도적인 주행 성능을 지닌 전용 전기차입니다.",
        "price_new": "약 4,800만 ~ 7,200만 원", "price_used": "약 3,200만 ~ 5,500만 원",
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #2ecc71; letter-spacing: 6px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ EV6</div>'
    },
    "기아 ev9": {
        "title": "Kia EV9", "brand": "KIA", "release": "2023년 출시",
        "desc": "플래그십 전동화 SUV로서 웅장한 체급과 첨단 기술을 모두 담은 대형 전기 SUV입니다.",
        "price_new": "약 7,300만 ~ 8,800만 원+", "price_used": "약 5,200만 ~ 7,000만 원",
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #2ecc71; letter-spacing: 6px; text-shadow: 0 0 25px rgba(46,204,113,0.6);">KIΛ EV9</div>'
    },

    # --- 기존 주요 차량들 ---
    "닛산 gtr": {
        "title": "Nissan GT-R (R35)", "brand": "NISSAN", "release": "2007년 12월",
        "desc": "일명 '고질라'. 3.8L V6 트윈터보 엔진과 4륜구동 시스템을 탑재한 일본의 슈퍼카입니다.",
        "price_new": "약 1억 4,000만 ~ 2억 5,000만 원", "price_used": "약 7,500만 ~ 1억 3,000만 원",
        "typo_html": '<div style="font-size: 4.5rem; font-weight: 900; color: #ff3333; letter-spacing: 3px; text-shadow: 0 0 25px rgba(255,51,51,0.6);">GT-R</div><div style="font-size: 1.1rem; color: #a0a0b0; font-weight: 600; letter-spacing: 8px; margin-top: 10px;">NISSAN RACING</div>'
    },
    "포르쉐 911": {
        "title": "Porsche 911 (992)", "brand": "PORSCHE", "release": "1963년 최초 출시",
        "desc": "후면 엔진(RR) 구조를 고수해 온 스포츠카의 살아있는 전설입니다.",
        "price_new": "약 1억 7,000만 원 ~ 3억 5,000만 원+", "price_used": "약 9,000만 ~ 2억 원대",
        "typo_html": '<div style="font-size: 3.2rem; font-weight: 900; color: #f1c40f; font-family: serif; letter-spacing: 4px; text-shadow: 0 0 25px rgba(241,196,15,0.5);">PORSCHE</div><div style="font-size: 0.95rem; color: #d4af37; font-weight: 600; letter-spacing: 10px; margin-top: 10px;">STUTTGART</div>'
    },
    "현대 그랜저": {
        "title": "Hyundai Grandeur (GN7)", "brand": "HYUNDAI", "release": "2022년 11월",
        "desc": "대한민국 플래그십 세단의 상징. 일체형 심리스 호라이즌 램프가 특징입니다.",
        "price_new": "약 3,700만 ~ 5,500만 원", "price_used": "약 2,800만 ~ 4,500만 원",
        "typo_html": '<div style="font-size: 3.2rem; font-weight: 900; color: #00f2fe; letter-spacing: 6px; text-shadow: 0 0 25px rgba(0,242,254,0.6);">HYUNDAI</div><div style="font-size: 0.95rem; color: #a0a0b0; font-weight: 600; letter-spacing: 5px; margin-top: 10px;">FLAGSHIP SEDAN</div>'
    },
    "메르세데스 벤츠 e클래스": {
        "title": "Mercedes-Benz E-Class", "brand": "MERCEDES-BENZ", "release": "2023년 11세대",
        "desc": "럭셔리의 대명사. 화려한 슈퍼스크린과 극상의 승차감을 선사합니다.",
        "price_new": "약 7,300만 ~ 1억 3,000만 원", "price_used": "약 4,000만 ~ 9,000만 원",
        "typo_html": '<div style="font-size: 2.3rem; font-weight: 900; color: #ffffff; letter-spacing: 3px; text-shadow: 0 0 25px rgba(255,255,255,0.7);">MERCEDES-BENZ</div><div style="font-size: 0.9rem; color: #a0a0b0; font-weight: 600; letter-spacing: 8px; margin-top: 10px;">THE BEST OR NOTHING</div>'
    }
}

# 4. 상단 메인 헤더 및 검색창 중앙 배치
st.write("\n")
st.markdown("<h1 class='hero-title'>NEON AUTO VAULT</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>⚡ 기아 전 차종 및 람보르기니 타이포그래피 오토 갤러리</p>", unsafe_allow_html=True)

st.write("\n")
col_space1, col_search, col_space2 = st.columns([1, 2.2, 1])
with col_search:
    search_query = st.text_input(
        "검색", 
        placeholder="🔍 차량 이름을 입력하세요 (예: 쏘렌토, 아벤타도르, K5, 911...)", 
        label_visibility="collapsed"
    ).strip().lower()

st.write("\n")

# 5. 검색 결과 및 상세 정보 출력 로직
if search_query:
    matched_data = None
    search_query_nospace = search_query.replace(" ", "")
    for key, data in CAR_DATABASE.items():
        if search_query_nospace in key.replace(" ", "") or key.replace(" ", "") in search_query_nospace:
            matched_data = data
            break

    if matched_data:
        st.divider()
        st.markdown(f"<h2 style='text-align: center; font-size: 2.5rem; margin-bottom: 25px; color:#fff;'>{matched_data['title']}</h2>", unsafe_allow_html=True)
        
        col_logo, col_info = st.columns(2, gap="large")
        
        with col_logo:
            st.markdown(f"""
            <div class="typo-box">
                {matched_data['typo_html']}
            </div>
            """, unsafe_allow_html=True)
            
        with col_info:
            st.markdown(f"""
            <div class="glass-card">
                <h3 class="section-header">📅 History & Specification</h3>
                <p style="color: #b0b0c0; font-size: 1.05rem; margin-bottom: 8px;"><b>제조사 브랜드:</b> <span style="color:#00f2fe;">{matched_data['brand']}</span></p>
                <p style="color: #b0b0c0; font-size: 1.05rem; margin-bottom: 8px;"><b>최초 출시 시기:</b> {matched_data['release']}</p>
                <p style="color: #b0b0c0; font-size: 1.05rem; line-height: 1.6;"><b>상세 설명:</b> {matched_data['desc']}</p>
            </div>
            
            <div class="glass-card">
                <h3 class="section-header">💰 Market Value & Price</h3>
                <p style="color: #b0b0c0; font-size: 1.05rem; margin-bottom: 12px;"><b>신차 출고가:</b><br><span class="price-highlight">{matched_data['price_new']}</span></p>
                <p style="color: #b0b0c0; font-size: 1.05rem; margin-bottom: 0;"><b>실시간 중고 시세:</b><br><span class="price-highlight">{matched_data['price_used']}</span></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: rgba(255,0,0,0.05); border: 1px solid rgba(255,0,0,0.2); border-radius: 16px; margin-top: 20px;">
            <h3 style="color: #ff4b4b;">⚠️ 차량 정보를 찾을 수 없습니다</h3>
            <p style="color: #aaa;">모닝, 레이, K5, 쏘렌토, 카니발, 아벤타도르, 우루스 등 올바른 차량명을 검색해 주세요.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    # 6. 첫 화면 추천 쇼케이스 갤러리
    st.divider()
    st.markdown("<h3 style='text-align: center; color: #fff; margin-bottom: 30px; font-weight: 800; letter-spacing: 1px;'>🔥 FEATURED SHOWCASE</h3>", unsafe_allow_html=True)
    
    feat_col1, feat_col2, feat_col3 = st.columns(3, gap="large")
    
    with feat_col1:
        st.markdown(f"""
        <div class="gallery-typo-box">
            {CAR_DATABASE["람보르기니 아벤타도르"]["typo_html"]}
        </div>
        <h4 style='text-align: center; margin-top: 15px; color: #fff;'>람보르기니 아벤타도르</h4>
        """, unsafe_allow_html=True)
    with feat_col2:
        st.markdown(f"""
        <div class="gallery-typo-box">
            {CAR_DATABASE["기아 쏘렌토"]["typo_html"]}
        </div>
        <h4 style='text-align: center; margin-top: 15px; color: #fff;'>기아 쏘렌토</h4>
        """, unsafe_allow_html=True)
    with feat_col3:
        st.markdown(f"""
        <div class="gallery-typo-box">
            {CAR_DATABASE["기아 카니발"]["typo_html"]}
        </div>
        <h4 style='text-align: center; margin-top: 15px; color: #fff;'>기아 카니발</h4>
        """, unsafe_allow_html=True)
