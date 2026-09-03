import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 기본 설정 (고급스러운 넓은 화면 적용)
st.set_page_config(page_title="Premium Car Explorer", page_icon="🚘", layout="wide")

# 2. 자동차 데이터 준비 (저작권 무료인 위키미디어 공용 사진 링크 사용)
cars = {
    "포르쉐 타이칸 (Porsche Taycan)": {
        "price": "₩ 130,000,000 ~ 240,000,000",
        "desc": "포르쉐의 영혼을 담은 순수 전기 스포츠카. 내연기관의 감성을 전기차에서도 그대로 느낄 수 있도록 설계된 걸작입니다.",
        "pros": ["압도적인 코너링과 주행 성능", "포르쉐 특유의 유려한 디자인", "초고속 충전 지원(800V 시스템)"],
        "cons": ["다소 부담스러운 가격대", "경쟁 모델 대비 짧은 1회 충전 주행거리", "비좁은 2열 공간"],
        "stats": {"최고속도": 90, "가속력": 95, "주행거리": 70, "승차감": 80, "혁신기술": 85, "디자인": 100},
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Porsche_Taycan_Turbo_S_Genf_2019_1Y7A5565.jpg/800px-Porsche_Taycan_Turbo_S_Genf_2019_1Y7A5565.jpg"
    },
    "현대 아이오닉 5 (Hyundai IONIQ 5)": {
        "price": "₩ 52,000,000 ~ 65,000,000",
        "desc": "미래지향적인 파라메트릭 픽셀 디자인과 넓은 실내 공간을 자랑하는 현대자동차의 전용 전기차 모델입니다.",
        "pros": ["V2L 기능으로 야외 활동에 최적화", "광활하고 쾌적한 실내(E-GMP 플랫폼)", "우수한 가격 대비 성능(가성비)"],
        "cons": ["호불호가 갈릴 수 있는 레트로 디자인", "소프트웨어 인포테인먼트의 한계", "고속 주행 시 풍절음"],
        "stats": {"최고속도": 75, "가속력": 75, "주행거리": 85, "승차감": 90, "혁신기술": 95, "디자인": 80},
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Hyundai_Ioniq_5_Project_45_IAA_2021_1X7A0065.jpg/800px-Hyundai_Ioniq_5_Project_45_IAA_2021_1X7A0065.jpg"
    },
    "테슬라 모델 S (Tesla Model S)": {
        "price": "₩ 115,000,000 ~ 135,000,000",
        "desc": "전기차 혁명의 시작을 알린 플래그십 세단. 압도적인 주행거리와 강력한 오토파일럿 기술을 탑재했습니다.",
        "pros": ["독보적인 자율주행 기술(FSD)", "가장 긴 수준의 1회 충전 주행거리", "슈퍼차저 생태계의 편리함"],
        "cons": ["다소 아쉬운 실내 마감 품질", "요크 스티어링 휠의 적응 문제", "부품 수리 및 AS 대기 시간"],
        "stats": {"최고속도": 95, "가속력": 100, "주행거리": 95, "승차감": 75, "혁신기술": 100, "디자인": 85},
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Tesla_Model_S_facelift_2022_1.jpg/800px-Tesla_Model_S_facelift_2022_1.jpg"
    }
}

# 3. 사이드바 구성 (차량 선택)
st.sidebar.header("차량 선택")
selected_car = st.sidebar.selectbox("상세 정보를 확인할 차량을 고르세요.", list(cars.keys()))
car_info = cars[selected_car]

# 4. 메인 화면 헤더
st.title(f"차량 상세 제원: {selected_car}")
st.markdown("---")

# 5. 레이아웃 분할 (왼쪽: 사진, 오른쪽: 기본 정보)
col1, col2 = st.columns([1, 1])

with col1:
    st.image(car_info["image"], caption=f"ⓒ Wikimedia Commons (CC BY-SA) - {selected_car}", use_container_width=True)

with col2:
    st.subheader("💰 가격대")
    st.write(f"**{car_info['price']}**")
    st.subheader("📝 차량 설명")
    st.write(car_info['desc'])
    
    # 핵심 스탯 요약 (Streamlit Metric 활용)
    st.subheader("⚡ 핵심 스탯")
    m1, m2, m3 = st.columns(3)
    m1.metric(label="가속력", value=f"{car_info['stats']['가속력']}/100")
    m2.metric(label="주행거리", value=f"{car_info['stats']['주행거리']}/100")
    m3.metric(label="기술력", value=f"{car_info['stats']['혁신기술']}/100")

st.markdown("---")

# 6. 상세 탭 구성 (장단점 / 육각형 차트 / 할부 계산기)
tab1, tab2, tab3 = st.tabs(["👍 장점 & 👎 단점", "📊 능력치 차트(육각형)", "💸 월 할부금 계산기 (추가 기능)"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.success("### 장점 (Pros)")
        for p in car_info["pros"]:
            st.write(f"- {p}")
    with c2:
        st.error("### 단점 (Cons)")
        for c in car_info["cons"]:
            st.write(f"- {c}")

with tab2:
    st.subheader(f"'{selected_car}' 종합 능력치")
    # Plotly를 이용한 육각형(Radar) 차트 생성
    categories = list(car_info["stats"].keys())
    values = list(car_info["stats"].values())
    
    # 시작점과 끝점을 맞춰주어 도형을 닫음
    categories = categories + [categories[0]]
    values = values + [values[0]]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(0, 114, 178, 0.4)',
        line=dict(color='rgba(0, 114, 178, 1)')
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        margin=dict(t=30, b=30, l=30, r=30)
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("인터랙티브 금융 계산기")
    st.info("차량의 대략적인 최소 가격을 기준으로 월 할부금을 계산해 봅니다. (이자율 미포함)")
    
    # 텍스트에서 최소 가격 숫자만 추출
    min_price_str = car_info["price"].split("~")[0].replace("₩", "").replace(",", "").strip()
    min_price = int(min_price_str)
    
    months = st.slider("할부 개월 수를 선택하세요.", min_value=12, max_value=60, value=36, step=12)
    monthly_payment = min_price // months
    
    st.write(f"선수금 및 이자가 없을 경우, **{months}개월** 동안 매월 납부해야 할 예상 금액은")
    st.markdown(f"### ₩ {monthly_payment:,} 원")
