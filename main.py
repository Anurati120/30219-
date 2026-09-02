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

    /* 메탈릭 엠블럼 박스 */
    .emblem-box {
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
    }

    .gallery-emblem-box {
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
    }
    .gallery-emblem-box:hover {
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

# 3. 고품질 리얼 SVG 메탈릭 엠블럼이 포함된 데이터베이스
CAR_DATABASE = {
    "닛산 gtr": {
        "title": "Nissan GT-R (R35)", "brand": "NISSAN", "release": "2007년 12월",
        "desc": "일명 '고질라'. 3.8L V6 트윈터보 엔진과 전설적인 ATTESA E-TS 4륜구동 시스템을 탑재한 일본의 대표 슈퍼카입니다.",
        "price_new": "약 1억 4,000만 ~ 2억 5,000만 원", "price_used": "약 7,500만 ~ 1억 3,000만 원",
        "logo_svg": '''
        <svg width="180" height="180" viewBox="0 0 200 200">
            <defs>
                <linearGradient id="nissanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ffffff"/>
                    <stop offset="50%" stop-color="#a6a6a6"/>
                    <stop offset="100%" stop-color="#404040"/>
                </linearGradient>
            </defs>
            <circle cx="100" cy="100" r="85" fill="none" stroke="url(#nissanGrad)" stroke-width="8"/>
            <rect x="35" y="82" width="130" height="36" fill="url(#nissanGrad)" rx="4"/>
            <text x="100" y="108" font-size="24" font-weight="900" fill="#111" text-anchor="middle" font-family="sans-serif" letter-spacing="3">GT-R</text>
        </svg>'''
    },
    "포르쉐 911": {
        "title": "Porsche 911 (992)", "brand": "PORSCHE", "release": "1963년 최초 출시 (현행 8세대)",
        "desc": "후면 엔진(RR) 구조를 수십 년간 고수해 온 스포츠카의 살아있는 전설. 완벽한 핸들링과 데일리 성능을 자랑합니다.",
        "price_new": "약 1억 7,000만 원 ~ 3억 5,000만 원+", "price_used": "약 9,000만 ~ 2억 원대",
        "logo_svg": '''
        <svg width="150" height="180" viewBox="0 0 160 200">
            <defs>
                <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ffe600"/>
                    <stop offset="50%" stop-color="#c99e10"/>
                    <stop offset="100%" stop-color="#7a5c00"/>
                </linearGradient>
            </defs>
            <path d="M80 10 L145 45 L145 130 C145 170 80 190 80 190 C80 190 15 170 15 130 L15 45 Z" fill="none" stroke="url(#goldGrad)" stroke-width="6"/>
            <text x="80" y="55" font-size="14" font-weight="900" fill="#ffd700" text-anchor="middle" font-family="serif" letter-spacing="2">PORSCHE</text>
            <path d="M70 80 L90 80 L85 110 L75 110 Z" fill="#ffd700"/>
            <circle cx="80" cy="135" r="25" fill="none" stroke="#ffd700" stroke-width="3"/>
            <text x="80" y="142" font-size="12" font-weight="bold" fill="#ffd700" text-anchor="middle">STUTTGART</text>
        </svg>'''
    },
    "테슬라 모델3": {
        "title": "Tesla Model 3 Performance", "brand": "TESLA", "release": "2017년 글로벌 최초 출시",
        "desc": "전기차 혁명을 이끈 주역. 미니멀한 인테리어와 폭발적인 제로백, OTA 무선 업데이트 기능이 특징입니다.",
        "price_new": "약 5,200만 ~ 6,800만 원", "price_used": "약 3,000만 ~ 4,500만 원",
        "logo_svg": '''
        <svg width="180" height="180" viewBox="0 0 200 200">
            <defs>
                <linearGradient id="redGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff4d4d"/>
                    <stop offset="100%" stop-color="#990000"/>
                </linearGradient>
            </defs>
            <circle cx="100" cy="100" r="85" fill="none" stroke="url(#redGrad)" stroke-width="5"/>
            <path d="M50 65 L150 65 L150 82 L112 82 L112 150 L88 150 L88 82 L50 82 Z" fill="url(#redGrad)" filter="drop-shadow(0px 4px 6px rgba(0,0,0,0.5))"/>
        </svg>'''
    },
    "제네시스 g80": {
        "title": "Genesis G80 (3세대)", "brand": "GENESIS", "release": "2020년 3세대 출시",
        "desc": "'역동적인 우아함'을 담아낸 대한민국 프리미엄 럭셔리 세단의 기준. 정숙성과 첨단 편의 사양이 일품입니다.",
        "price_new": "약 5,500만 ~ 8,500만 원", "price_used": "약 3,500만 ~ 6,000만 원",
        "logo_svg": '''
        <svg width="180" height="180" viewBox="0 0 200 200">
            <defs>
                <linearGradient id="silverGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ffffff"/>
                    <stop offset="50%" stop-color="#silver"/>
                    <stop offset="100%" stop-color="#707070"/>
                </linearGradient>
            </defs>
            <path d="M40 90 Q 100 130 160 90 Q 100 160 40 90 Z" fill="url(#silverGrad)"/>
            <path d="M60 80 Q 100 110 140 80" fill="none" stroke="#ffffff" stroke-width="4"/>
            <text x="100" y="150" font-size="12" font-weight="700" fill="#cccccc" text-anchor="middle" letter-spacing="5">GENESIS</text>
        </svg>'''
    },
    "bmw 5시리즈": {
        "title": "BMW 5 Series (G60)", "brand": "BMW", "release": "2023년 8세대 풀체인지",
        "desc": "전 세계 비즈니스 세단 시장의 절대강자. 다이내믹한 주행 성능과 순수 전기차(i5) 라인업까지 확장되었습니다.",
        "price_new": "약 6,800만 ~ 1억 1,000만 원", "price_used": "약 4,000만 ~ 8,000만 원",
        "logo_svg": '''
        <svg width="180" height="180" viewBox="0 0 200 200">
            <defs>
                <linearGradient id="bmwMetal" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ffffff"/>
                    <stop offset="50%" stop-color="#8c8c8c"/>
                    <stop offset="100%" stop-color="#262626"/>
                </linearGradient>
            </defs>
            <circle cx="100" cy="100" r="85" fill="#111" stroke="url(#bmwMetal)" stroke-width="8"/>
            <path d="M100 20 A 80 80 0 0 1 180 100 L 100 100 Z" fill="#0066b2"/>
            <path d="M100 180 A 80 80 0 0 1 20 100 L 100 100 Z" fill="#0066b2"/>
            <path d="M20 100 A 80 80 0 0 1 100 20 L 100 100 Z" fill="#ffffff"/>
            <path d="M180 100 A 80 80 0 0 1 100 180 L 100 100 Z" fill="#ffffff"/>
            <circle cx="100" cy="100" r="85" fill="none" stroke="url(#bmwMetal)" stroke-width="4"/>
            <text x="100" y="42" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="3">B M W</text>
        </svg>'''
    },
    "현대 그랜저": {
        "title": "Hyundai Grandeur (GN7)", "brand": "HYUNDAI", "release": "2022년 11월 7세대",
        "desc": "대한민국 플래그십 세단의 상징. 일체형 심리스 호라이즌 램프와 광활한 실내 공간을 갖추었습니다.",
        "price_new": "약 3,700만 ~ 5,500만 원", "price_used": "약 2,800만 ~ 4,500만 원",
        "logo_svg": '''
        <svg width="180" height="180" viewBox="0 0 200 200">
            <defs>
                <linearGradient id="hyundaiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#00f2fe"/>
                    <stop offset="100%" stop-color="#0055ff"/>
                </linearGradient>
            </defs>
            <ellipse cx="100" cy="100" rx="80" ry="50" fill="none" stroke="url(#hyundaiGrad)" stroke-width="8" transform="rotate(-15 100 100)"/>
            <path d="M65 70 L 80 130 L 95 100 L 120 100 L 135 130 L 150 70" fill="none" stroke="#ffffff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>'''
    },
    "메르세데스 벤츠 e클래스": {
        "title": "Mercedes-Benz E-Class", "brand": "MERCEDES-BENZ", "release": "2023년 11세대 공개",
        "desc": "럭셔리의 대명사. 화려한 MBUX 슈퍼스크린과 극상의 승차감으로 수입차 시장을 평정한 모델입니다.",
        "price_new": "약 7,300만 ~ 1억 3,000만 원", "price_used": "약 4,000만 ~ 9,000만 원",
        "logo_svg": '''
        <svg width="180" height="180" viewBox="0 0 200 200">
            <defs>
                <linearGradient id="benzMetal" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ffffff"/>
                    <stop offset="50%" stop-color="#b3b3b3"/>
                    <stop offset="100%" stop-color="#333333"/>
                </linearGradient>
            </defs>
            <!-- 바깥 원 -->
            <circle cx="100" cy="100" r="82" fill="none" stroke="url(#benzMetal)" stroke-width="7" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.6))"/>
            <!-- 삼각별 입체 날개 -->
            <polygon points="100,25 107,95 100,105" fill="url(#benzMetal)"/>
            <polygon points="100,25 93,95 100,105" fill="#555555"/>
            
            <polygon points="35,135 97,102 100,108" fill="url(#benzMetal)"/>
            <polygon points="35,135 95,112 100,108" fill="#555555"/>
            
            <polygon points="165,135 103,102 100,108" fill="url(#benzMetal)"/>
            <polygon points="165,135 105,112 100,108" fill="#444444"/>
        </svg>'''
    },
    "포드 머스탱": {
        "title": "Ford Mustang (Dark Horse)", "brand": "FORD", "release": "1964년 최초 / 현행 7세대",
        "desc": "아메리칸 머슬카의 살아있는 영혼. 가슴을 울리는 V8 배기음과 상징적인 디자인이 매력입니다.",
        "price_new": "약 5,900만 ~ 8,600만 원", "price_used": "약 3,000만 ~ 6,000만 원",
        "logo_svg": '''
        <svg width="180" height="180" viewBox="0 0 200 200">
            <defs>
                <linearGradient id="orangeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff9900"/>
                    <stop offset="100%" stop-color="#cc3300"/>
                </linearGradient>
            </defs>
            <circle cx="100" cy="100" r="85" fill="none" stroke="url(#orangeGrad)" stroke-width="6"/>
            <text x="100" y="110" font-size="28" font-weight="900" fill="url(#orangeGrad)" text-anchor="middle" font-family="sans-serif" letter-spacing="4">MUSTANG</text>
        </svg>'''
    },
    "아우디 a6": {
        "title": "Audi A6", "brand": "AUDI", "release": "2018년 8세대",
        "desc": "디지털 라이팅 기술의 선두주자. 첨단 버츄얼 콕핏과 안정적인 콰트로 시스템을 자랑합니다.",
        "price_new": "약 7,000만 ~ 9,500만 원", "price_used": "약 3,500만 ~ 6,000만 원",
        "logo_svg": '''
        <svg width="180" height="180" viewBox="0 0 200 200">
            <defs>
                <linearGradient id="audiMetal" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ffffff"/>
                    <stop offset="50%" stop-color="#cccccc"/>
                    <stop offset="100%" stop-color="#555555"/>
                </linearGradient>
            </defs>
            <circle cx="65" cy="100" r="30" fill="none" stroke="url(#audiMetal)" stroke-width="7"/>
            <circle cx="90" cy="100" r="30" fill="none" stroke="url(#audiMetal)" stroke-width="7"/>
            <circle cx="115" cy="100" r="30" fill="none" stroke="url(#audiMetal)" stroke-width="7"/>
            <circle cx="140" cy="100" r="30" fill="none" stroke="url(#audiMetal)" stroke-width="7"/>
        </svg>'''
    },
    "기아 쏘렌토": {
        "title": "Kia Sorento (Hybrid)", "brand": "KIA", "release": "2020년 4세대 (페이스리프트)",
        "desc": "대한민국 패밀리 SUV 시장의 독보적인 1위. 뛰어난 공간 활용성과 친환경 하이브리드 조합이 강점입니다.",
        "price_new": "약 3,500만 ~ 4,800만 원", "price_used": "약 2,500만 ~ 4,000만 원",
        "logo_svg": '''
        <svg width="180" height="180" viewBox="0 0 200 200">
            <defs>
                <linearGradient id="kiaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#2ecc71"/>
                    <stop offset="100%" stop-color="#1abc9c"/>
                </linearGradient>
            </defs>
            <text x="100" y="112" font-size="45" font-weight="900" fill="url(#kiaGrad)" text-anchor="middle" font-family="sans-serif" letter-spacing="2">KIΛ</text>
        </svg>'''
    }
}

# 4. 상단 메인 헤더 및 검색창 중앙 배치
st.write("\n")
st.markdown("<h1 class='hero-title'>NEON AUTO VAULT</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>⚡ 리얼 메탈릭 엠블럼과 실시간 시세를 완벽하게 확인하세요</p>", unsafe_allow_html=True)

st.write("\n")
col_space1, col_search, col_space2 = st.columns([1, 2.2, 1])
with col_search:
    search_query = st.text_input(
        "검색", 
        placeholder="🔍 차량 이름을 입력하세요 (예: 닛산 GTR, 포르쉐 911, 그랜저...)", 
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
            # 리얼 메탈릭 SVG 엠블럼 출력
            st.markdown(f"""
            <div class="emblem-box">
                {matched_data['logo_svg']}
                <div style="font-size: 0.85srem; color: #8b8b9e; margin-top: 15px; letter-spacing: 3px; font-weight: 600;">METALLIC EMBLEM VERIFIED</div>
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
            <p style="color: #aaa;">등록된 차량 이름(GTR, 911, 모델3, G80, 5시리즈, 그랜저, E클래스, 머스탱, A6, 쏘렌토)으로 다시 검색해 주세요.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    # 6. 첫 화면 추천 쇼케이스 갤러리
    st.divider()
    st.markdown("<h3 style='text-align: center; color: #fff; margin-bottom: 30px; font-weight: 800; letter-spacing: 1px;'>🔥 FEATURED SHOWCASE</h3>", unsafe_allow_html=True)
    
    feat_col1, feat_col2, feat_col3 = st.columns(3, gap="large")
    
    with feat_col1:
        st.markdown(f"""
        <div class="gallery-emblem-box">
            {CAR_DATABASE["포르쉐 911"]["logo_svg"]}
        </div>
        <h4 style='text-align: center; margin-top: 15px; color: #fff;'>포르쉐 911 (992)</h4>
        """, unsafe_allow_html=True)
    with feat_col2:
        st.markdown(f"""
        <div class="gallery-emblem-box">
            {CAR_DATABASE["닛산 gtr"]["logo_svg"]}
        </div>
        <h4 style='text-align: center; margin-top: 15px; color: #fff;'>닛산 GT-R (R35)</h4>
        """, unsafe_allow_html=True)
    with feat_col3:
        st.markdown(f"""
        <div class="gallery-emblem-box">
            {CAR_DATABASE["메르세데스 벤츠 e클래스"]["logo_svg"]}
        </div>
        <h4 style='text-align: center; margin-top: 15px; color: #fff;'>메르세데스 벤츠 E-Class</h4>
        """, unsafe_allow_html=True)
