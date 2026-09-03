import streamlit as st
import plotly.graph_objects as go
import math

# 1. 페이지 설정 및 플롯리(Plotly) 레이아웃 설정
st.set_page_config(page_title="NEON AUTO VAULT | PRO", page_icon="🏎️", layout="wide")

# 2. 울트라 프리미엄 CSS
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #161625 0%, #050508 100%);
        color: #e0e0e0;
        font-family: 'SF Pro Display', -apple-system, sans-serif;
    }
    
    .hero-title {
        text-align: center; font-size: 4.5rem; font-weight: 900; letter-spacing: -2px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #f093fb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px;
    }
    .hero-subtitle {
        text-align: center; color: #8b8b9e; font-size: 1.2rem; margin-bottom: 40px; letter-spacing: 2px;
    }

    div[data-baseweb="input"] > div {
        background-color: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(79, 172, 254, 0.5) !important;
        border-radius: 12px !important; color: #fff !important;
    }
    input { color: #ffffff !important; font-weight: 700 !important; font-size: 1.2rem !important; text-align: center; }

    .glass-card {
        background: rgba(20, 20, 30, 0.6); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 25px; margin-bottom: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }

    .typo-box {
        width: 100%; height: 300px; background: linear-gradient(135deg, #11111a 0%, #08080c 100%);
        border-radius: 20px; border: 1px solid rgba(79, 172, 254, 0.2);
        display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
        box-shadow: inset 0 0 50px rgba(0,242,254,0.05);
    }

    .badge-depreciation {
        display: inline-block; padding: 8px 15px; border-radius: 8px; font-weight: 800; font-size: 1rem;
        background: rgba(231, 76, 60, 0.1); color: #e74c3c; border: 1px solid rgba(231, 76, 60, 0.3); margin-top: 10px;
    }
    .badge-good { color: #2ecc71; background: rgba(46, 204, 113, 0.1); border-color: rgba(46, 204, 113, 0.3); }

    .highlight-value {
        font-size: 2.2rem; font-weight: 900; background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# 3. 데이터베이스 (스펙 데이터 & 계산용 수치 추가)
# specs: [최고출력, 가속력(제로백), 최고속도, 핸들링/코너링, 실용성/공간] (100점 만점 기준)
CAR_DATABASE = {
    "람보르기니 아벤타도르": {
        "title": "Lamborghini Aventador", "brand": "LAMBORGHINI", "release": "2011년",
        "desc": "자연흡기 V12 엔진의 황홀한 배기음. 궁극의 트랙 머신입니다.",
        "price_new_str": "6억 5,000만 원", "price_used_str": "4억 8,000만 원",
        "price_new_num": 65000, "price_used_num": 48000, # 만원 단위
        "specs": [95, 95, 98, 90, 20],
        "typo_html": '<div style="font-size: 3.5rem; font-weight: 900; color: #f39c12; letter-spacing: 2px; text-shadow: 0 0 20px rgba(243,156,18,0.5);">AVENTADOR</div>'
    },
    "람보르기니 우루스": {
        "title": "Lamborghini Urus", "brand": "LAMBORGHINI", "release": "2018년",
        "desc": "슈퍼카의 DNA를 이식받은 고성능 럭셔리 SUV의 끝판왕.",
        "price_new_str": "3억 2,000만 원", "price_used_str": "2억 6,000만 원",
        "price_new_num": 32000, "price_used_num": 26000,
        "specs": [85, 88, 85, 80, 85],
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #f1c40f; letter-spacing: 6px; text-shadow: 0 0 20px rgba(241,196,15,0.5);">URUS</div>'
    },
    "포르쉐 911": {
        "title": "Porsche 911 (992)", "brand": "PORSCHE", "release": "1963년",
        "desc": "완벽한 밸런스를 자랑하는 외계인이 고문해서 만든 스포츠카.",
        "price_new_str": "2억 2,000만 원", "price_used_str": "1억 8,000만 원",
        "price_new_num": 22000, "price_used_num": 18000,
        "specs": [75, 85, 85, 98, 40],
        "typo_html": '<div style="font-size: 3.5rem; font-weight: 900; color: #d4af37; font-family: serif; letter-spacing: 4px;">PORSCHE</div>'
    },
    "기아 쏘렌토": {
        "title": "Kia Sorento (Hybrid)", "brand": "KIA", "release": "2020년",
        "desc": "대한민국 패밀리 SUV의 정석. 압도적인 연비와 공간성을 자랑합니다.",
        "price_new_str": "4,500만 원", "price_used_str": "3,800만 원",
        "price_new_num": 4500, "price_used_num": 3800,
        "specs": [40, 50, 45, 60, 95],
        "typo_html": '<div style="font-size: 3.5rem; font-weight: 900; color: #2ecc71; letter-spacing: 4px; text-shadow: 0 0 20px rgba(46,204,113,0.5);">KIΛ SORENTO</div>'
    },
    "기아 카니발": {
        "title": "Kia Carnival", "brand": "KIA", "release": "1998년",
        "desc": "아빠들의 영원한 드림카, 비교불가 패밀리 미니밴.",
        "price_new_str": "4,800만 원", "price_used_str": "3,900만 원",
        "price_new_num": 4800, "price_used_num": 3900,
        "specs": [45, 40, 40, 50, 100],
        "typo_html": '<div style="font-size: 3.5rem; font-weight: 900; color: #2ecc71; letter-spacing: 4px; text-shadow: 0 0 20px rgba(46,204,113,0.5);">KIΛ CARNIVAL</div>'
    },
    "기아 ev9": {
        "title": "Kia EV9", "brand": "KIA", "release": "2023년",
        "desc": "플래그십 대형 전기 SUV. 미래지향적 디자인과 고출력 듀얼모터.",
        "price_new_str": "8,500만 원", "price_used_str": "6,800만 원",
        "price_new_num": 8500, "price_used_num": 6800,
        "specs": [70, 75, 65, 65, 95],
        "typo_html": '<div style="font-size: 4rem; font-weight: 900; color: #00f2fe; letter-spacing: 6px; text-shadow: 0 0 20px rgba(0,242,254,0.5);">KIΛ EV9</div>'
    }
}

# 4. 헤더 및 검색
st.markdown("<h1 class='hero-title'>NEON AUTO VAULT</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>데이터로 증명하는 럭셔리 모빌리티 갤러리</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_query = st.text_input("차량 검색", placeholder="아벤타도르, 쏘렌토, 911 등 입력...", label_visibility="collapsed").strip().lower()

# 5. 검색 결과 및 대시보드 렌더링
if search_query:
    matched_data = None
    search_nospace = search_query.replace(" ", "")
    for key, data in CAR_DATABASE.items():
        if search_nospace in key.replace(" ", ""):
            matched_data = data
            break

    if matched_data:
        st.divider()
        
        # 감가율 계산 로직
        depreciation_rate = ((matched_data['price_new_num'] - matched_data['price_used_num']) / matched_data['price_new_num']) * 100
        badge_class = "badge-good" if depreciation_rate < 20 else "badge-depreciation"
        badge_text = f"🛡️ 방어율 우수 (감가 {depreciation_rate:.1f}%)" if depreciation_rate < 20 else f"📉 감가 진행 (신차대비 -{depreciation_rate:.1f}%)"

        # [상단 헤더 정보]
        st.markdown(f"<h2 style='text-align: center; margin-bottom: 5px;'>{matched_data['title']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; margin-bottom: 30px;'><span class='{badge_class}'>{badge_text}</span></div>", unsafe_allow_html=True)
        
        # [섹션 1] 브랜드 로고 & 기본 정보
        c_logo, c_info = st.columns([1.2, 1.8], gap="large")
        with c_logo:
            st.markdown(f"<div class='typo-box'>{matched_data['typo_html']}</div>", unsafe_allow_html=True)
        with c_info:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:#fff;'>📋 Identity & Market Price</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#bbb;'><b>브랜드:</b> {matched_data['brand']} &nbsp;|&nbsp; <b>출시:</b> {matched_data['release']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#ddd;'>{matched_data['desc']}</p>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(f"<p style='color:#888; margin:0;'>신차 출고가: {matched_data['price_new_str']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#fff; font-size:1.5rem; margin:0;'><b>중고 시세: <span class='highlight-value'>{matched_data['price_used_str']}</span></b></p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("\n")
        
        # [섹션 2] 전문가용 탭 UI (스펙 시각화 vs 금융 계산기)
        tab1, tab2 = st.tabs(["🚀 다이내믹 스펙 레이더", "💳 맞춤형 할부 금융 계산기"])
        
        with tab1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            t_col1, t_col2 = st.columns([2, 1])
            with t_col1:
                # Plotly 레이더 차트 생성
                categories = ['최고출력 (Power)', '가속력 (0-100km/h)', '최고속도 (Top Speed)', '핸들링 (Handling)', '실용/공간성 (Space)']
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=matched_data['specs'],
                    theta=categories,
                    fill='toself',
                    fillcolor='rgba(0, 242, 254, 0.2)',
                    line=dict(color='#00f2fe', width=3),
                    marker=dict(color='#4facfe', size=8)
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor='rgba(255,255,255,0.1)'),
                        angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='#e0e0e0', font=dict(size=13, weight="bold"))
                    ),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=40, r=40, t=20, b=20),
                    height=350
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with t_col2:
                st.markdown("<br><br><h4 style='color:#fff;'>🔥 퍼포먼스 인사이트</h4>", unsafe_allow_html=True)
                st.markdown("<p style='color:#aaa; font-size:0.95rem;'>본 차량의 성능 밸런스를 시각화한 육각형 지표입니다. 면적이 넓을수록 전천후 성능이 뛰어나며, 특정 방향으로 뾰족할수록 해당 목적(스포츠/패밀리)에 특화된 모델을 의미합니다.</p>", unsafe_allow_html=True)
                st.progress(matched_data['specs'][0], text=f"엔진 퍼포먼스 점수 ({matched_data['specs'][0]}/100)")
                st.progress(matched_data['specs'][4], text=f"실용성 및 편의 점수 ({matched_data['specs'][4]}/100)")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#fff;'>💰 중고차 실시간 할부 시뮬레이터</h4>", unsafe_allow_html=True)
            f_col1, f_col2 = st.columns(2, gap="large")
            
            with f_col1:
                base_price = matched_data['price_used_num']
                down_payment_pct = st.slider("선수금 비율 (%)", min_value=0, max_value=100, value=30, step=10)
                months = st.selectbox("할부 기간", options=[12, 24, 36, 48, 60], index=2, format_func=lambda x: f"{x}개월")
                interest_rate = st.number_input("예상 금리 (%)", min_value=1.0, max_value=15.0, value=5.5, step=0.1)
                
            with f_col2:
                # 금융 계산 로직
                down_payment = base_price * (down_payment_pct / 100)
                principal = base_price - down_payment
                
                if principal > 0:
                    monthly_rate = (interest_rate / 100) / 12
                    monthly_payment = (principal * monthly_rate) / (1 - math.pow(1 + monthly_rate, -months))
                else:
                    monthly_payment = 0
                
                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.1);">
                    <p style="color:#aaa; margin:0;">차량 기준가: <b>{base_price:,}만 원</b></p>
                    <p style="color:#aaa; margin-bottom:15px;">선수금 ({down_payment_pct}%): <b>{int(down_payment):,}만 원</b></p>
                    <p style="color:#fff; font-size:1.1rem;">할부 원금: <b>{int(principal):,}만 원</b> (금리 {interest_rate}%)</p>
                    <hr style="border-color: rgba(255,255,255,0.1);">
                    <p style="color:#00f2fe; font-size:1.2rem; margin:0;">월 예상 납입금</p>
                    <p style="color:#fff; font-size:2.5rem; font-weight:900; margin:0;">약 {int(monthly_payment):,}만 원</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("데이터베이스에 없는 차량입니다. 쏘렌토, 911, 우루스 등을 검색해 보세요.")
else:
    st.info("👆 위 검색창에 '아벤타도르', '카니발' 등 차량 이름을 검색하여 프로페셔널 대시보드를 확인하세요.")
