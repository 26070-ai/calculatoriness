import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time

# 페이지 설정
st.set_page_config(page_title="고급 계산기 & 그래프", page_icon="🧮", layout="wide")

# 무지개색 배경 - 시간에 따라 변하는 색상
def get_rainbow_colors():
    """시간에 따라 무지개 색상 2개를 반환"""
    colors = [
        ("#FF0000", "#FF7F00"),  # 빨강-주황
        ("#FF7F00", "#FFFF00"),  # 주황-노랑
        ("#FFFF00", "#00FF00"),  # 노랑-초록
        ("#00FF00", "#0000FF"),  # 초록-파랑
        ("#0000FF", "#4B0082"),  # 파랑-남색
        ("#4B0082", "#9400D3"),  # 남색-보라
        ("#9400D3", "#FF0000"),  # 보라-빨강
    ]
    current_millisecond = (datetime.now().second * 1000 + datetime.now().microsecond // 1000)
    color_index = (current_millisecond // 500) % len(colors)
    return colors[color_index]

# 무지개색 배경을 위한 CSS 스타일 (매 0.5초마다 색상 변경)
col1, col2 = get_rainbow_colors()

st.markdown(f"""
    <style>
        * {{
            margin: 0;
            padding: 0;
        }}
        
        html, body {{
            width: 100%;
            height: 100%;
        }}
        
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(135deg, {col1} 0%, {col2} 100%) !important;
        }}
        
        [data-testid="stSidebar"] {{
            background: linear-gradient(135deg, {col1} 0%, {col2} 100%) !important;
        }}
        
        [data-testid="stMainBlockContainer"] {{
            background: rgba(255, 255, 255, 0.93) !important;
            border-radius: 15px;
            margin: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        .stSelectbox, .stNumberInput, .stSlider, .stButton {{
            background: rgba(255, 255, 255, 0.98) !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# 자동 새로고침을 위한 placeholder
placeholder = st.empty()

st.title("🧮 고급 계산기 & Plotly 그래프 웹앱")
st.write("사칙연산, 모듈러, 지수, 로그 연산 및 반응형 함수 그래프 그리기를 지원합니다.")

# 대메뉴 선택 (일반 계산기 vs 그래프 모드)
mode = st.sidebar.selectbox("모드를 선택하세요", ("기본 계산기", "함수 그래프 그리기"))

# --- 1. 기본 계산기 모드 ---
if mode == "기본 계산기":
    st.header("🔢 일반 계산기")
    
    operation = st.selectbox(
        "연산을 선택하세요",
        ("덧셈", "뺄셈", "곱셈", "나눗셈", "모듈러 연산", "지수 연산", "로그 연산")
    )

    num1 = st.number_input("첫 번째 숫자", value=0.0)
    num2 = 0.0
    base = 10.0

    if operation == "로그 연산":
        base = st.number_input("로그 밑(base)", value=10.0, min_value=0.1)
    else:
        num2 = st.number_input("두 번째 숫자", value=0.0)

    if st.button("계산하기"):
        try:
            if operation == "덧셈":
                result = num1 + num2
            elif operation == "뺄셈":
                result = num1 - num2
            elif operation == "곱셈":
                result = num1 * num2
            elif operation == "나눗셈":
                if num2 == 0:
                    st.error("0으로 나눌 수 없습니다.")
                    st.stop()
                result = num1 / num2
            elif operation == "모듈러 연산":
                if num2 == 0:
                    st.error("0으로 나머지 연산을 할 수 없습니다.")
                    st.stop()
                result = num1 % num2
            elif operation == "지수 연산":
                result = num1 ** num2
            elif operation == "로그 연산":
                if num1 <= 0:
                    st.error("로그 입력값은 0보다 커야 합니다.")
                    st.stop()
                if base <= 0 or base == 1:
                    st.error("로그 밑은 0보다 크고 1이 아니어야 합니다.")
                    st.stop()
                result = math.log(num1, base)

            st.success(f"결과: {result}")
        except Exception as e:
            st.error(f"오류 발생: {e}")

# --- 2. 함수 그래프 그리기 모드 (Plotly 버전) ---
elif mode == "함수 그래프 그리기":
    st.header("📈 Plotly 반응형 그래프")
    st.write("마우스를 올리면 좌표가 보이고, 드래그로 확대가 가능합니다.")

    func_type = st.selectbox(
        "함수 종류 선택",
        ("일차함수 (y = ax + b)", "이차함수 (y = ax² + bx + c)", "지수함수 (y = a^x)", "사인함수 (y = sin(x))", "코사인함수 (y = cos(x))", "로그함수 (y = log(x))")
    )

    x_min, x_max = st.slider("x축 범위 설정", -50.0, 50.0, (-10.0, 10.0))

    if x_min >= x_max:
        st.error("최솟값은 최댓값보다 작아야 합니다.")
        st.stop()

    x = np.linspace(x_min, x_max, 400)
    y = np.zeros_like(x)
    title_label = ""

    if func_type == "일차함수 (y = ax + b)":
        col1_input, col2_input = st.columns(2)
        a = col1_input.number_input("기울기 (a)", value=1.0)
        b = col2_input.number_input("y절편 (b)", value=0.0)
        y = a * x + b
        title_label = f"y = {a}x + {b}"

    elif func_type == "이차함수 (y = ax² + bx + c)":
        col1_input, col2_input, col3_input = st.columns(3)
        a = col1_input.number_input("a (이차항)", value=1.0)
        b = col2_input.number_input("b (일차항)", value=0.0)
        c = col3_input.number_input("c (상수항)", value=0.0)
        y = a * (x**2) + b * x + c
        title_label = f"y = {a}x² + {b}x + {c}"

    elif func_type == "지수함수 (y = a^x)":
        a = st.number_input("밑 (a)", value=2.0, min_value=0.1)
        if a == 1.0:
            st.warning("밑이 1이면 상수함수가 됩니다.")
        try:
            y = a ** x
            title_label = f"y = {a}^x"
        except:
            st.error("지수 계산 중 오류가 발생했습니다.")
            st.stop()

    elif func_type == "사인함수 (y = sin(x))":
        y = np.sin(x)
        title_label = "y = sin(x)"

    elif func_type == "코사인함수 (y = cos(x))":
        y = np.cos(x)
        title_label = "y = cos(x)"

    elif func_type == "로그함수 (y = log(x))":
        if x_min <= 0:
            x = np.linspace(0.1, max(x_max, 1.0), 400)
            st.warning("로그함수 특성상 x축 범위가 0.1부터 시작하도록 자동 조정되었습니다.")
        y = np.log(x)
        title_label = "y = ln(x)"

    # Plotly로 그래프 그리기
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=title_label, line=dict(color='#00FF00', width=4)))
    
    # 레이아웃 스타일 설정 (축 레이블, 그리드 등)
    fig.update_layout(
        title=title_label,
        xaxis_title="x",
        yaxis_title="y",
        template="plotly_white",
        hovermode="x unified", # 마우스를 대면 x축 기준 값이 한눈에 보임
        plot_bgcolor='rgba(200, 100, 255, 0.1)',  # 밝은 보라 배경
        paper_bgcolor='rgba(255, 200, 100, 0.2)'  # 밝은 주황 배경
    )
    
    # x=0, y=0 기준선 추가구현 (밝은 색)
    fig.add_hline(y=0, line_dash="dash", line_color="#FF00FF", line_width=2)
    fig.add_vline(x=0, line_dash="dash", line_color="#00FFFF", line_width=2)

    # Streamlit에 Plotly 차트 띄우기
    st.plotly_chart(fig, use_container_width=True)

# 배경색 자동 업데이트를 위한 JavaScript
st.markdown("""
    <script>
        // 0.5초마다 페이지 새로고침
        setInterval(function() {
            location.reload();
        }, 500);
    </script>
    """, unsafe_allow_html=True)
