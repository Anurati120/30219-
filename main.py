import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(page_title="차량 정보 검색 포털", page_icon="🏎️", layout="centered")

# 2. 저작권 걱정 없는 Unsplash 라이선스 이미지와 자동차 데이터베이스
CAR_DATABASE = {
    "닛산 gtr": {
        "title": "닛산 GT-R (Nissan GT-R R35)",
        "release": "2007년 12월 첫 출시",
        "desc": "일명 '고질라'라는 별명을 가진 일본의 대표적인 고성능 슈퍼카입니다. 3.8리터 V6 트윈터보 엔진과 4륜구동(AWD) 시스템이 결합하여 압도적인 서킷 주행 성능을 자랑합니다.",
        "price_new": "약 1억 4,000만 ~ 2억 5,000만 원",
        "price_used": "약 7,500만 ~ 1억 3,000만 원 (연식/상태별 상이)",
        "image_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1000&q=80"
    },
    "포르쉐 911": {
        "title": "포르쉐 911 (Porsche 911)",
        "release": "1963년 최초 출시 (현행 8세대 992)",
        "desc": "독일 포르쉐의 정체성을 상징하는 RR(후륜 엔진) 구조의 명품 스포츠카입니다. 데일리 카로 사용할 수 있을 만큼 뛰어난 내구성과 탁월한 코너링 성능을 갖추었습니다.",
        "price_new": "약 1억 7,000만 ~ 3억 5,000만 원 이상",
        "price_used": "약 9,000만 ~ 2억 원대",
        "image_url": "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=1000&q=80"
    },
    "테슬라 모델3": {
        "title": "테슬라 모델 3 (Tesla Model 3)",
        "release": "2017년 글로벌 최초 출시",
        "desc": "전 세계 전기차 대중화를 이끈 테슬라의 대표 중형 세단입니다. 압도적인 가속력, 최첨단 오토파일럿 자율주행 기능, 미니멀한 실내 인테웨어가 핵심 특징입니다.",
        "price_new": "약 5,200만 ~ 6,800만 원",
        "price_used": "약 3,000만 ~ 4,500만 원",
        "image_url": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=1000&q=80"
    }
}

# 3. 화면 상단 타이틀 및 안내 문구
st.markdown("<h1 style='text-align: center;'>🏎️ 자동차 정보 검색 포털</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>궁금한 자동차의 이름이나 모델명을 검색해 보세요.</p>", unsafe_allow_html=True)
st.write("")

# 4. 화면 가운데 위치한 검색창
search_query = st.text_input(
    label="자동차 이름 검색",
    placeholder="예: 닛산 GTR, 포르쉐 911, 테슬라 모델3",
    label_visibility="collapsed"
).strip().lower()

# 5. 검색 결과 출력 로직
if search_query:
    # 입력한 단어가 데이터베이스에 있는지 확인
    matched_data = None
    for key, data in CAR_DATABASE.items():
        if search_query in key or key in search_query:
            matched_data = data
            break

    if matched_data:
        st.divider()
        st.subheader(f"🔍 {matched_data['title']}")
        
        # 저작권 무료(Unsplash) 고화질 자동차 사진 출력
        st.image(matched_data["image_url"], use_container_width=True, caption="출처: Unsplash (상업적 이용 가능 무료 이미지)")
        
        # 정보 레이아웃 (2개 열로 분할)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📅 출시 시기")
            st.info(matched_data["release"])
            
            st.markdown("### 📝 차량 상세 설명")
            st.write(matched_data["desc"])
            
        with col2:
            st.markdown("### 💰 현재 가격 정보")
            st.metric(label="신차 출고가", value=matched_data["price_new"])
            st.metric(label="중고차 시세", value=matched_data["price_used"])
    else:
        st.warning("⚠️ 입력하신 자동차 정보를 찾을 수 없습니다. (검색 예시: 닛산 GTR, 포르쉐 911, 테슬라 모델3)")
