import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="고급 계산기 & 그래프", page_icon="🧮")

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
        ("일차함수 (y = ax + b)", "이차함수 (y = ax² + bx + c)", "사인함수 (y = sin(x))", "코사인함수 (y = cos(x))", "로그함수 (y = log(x))")
    )

    x_min, x_max = st.slider("x축 범위 설정", -50.0, 50.0, (-10.0, 10.0))

    if x_min >= x_max:
        st.error("최솟값은 최댓값보다 작아야 합니다.")
        st.stop()

    x = np.linspace(x_min, x_max, 400)
    y = np.zeros_like(x)
    title_label = ""

    if func_type == "일차함수 (y = ax + b)":
        col1, col2 = st.columns(2)
        a = col1.number_input("기울기 (a)", value=1.0)
        b = col2.number_input("y절편 (b)", value=0.0)
        y = a * x + b
        title_label = f"y = {a}x + {b}"

    elif func_type == "이차함수 (y = ax² + bx + c)":
        col1, col2, col3 = st.columns(3)
        a = col1.number_input("a (이차항)", value=1.0)
        b = col2.number_input("b (일차항)", value=0.0)
        c = col3.number_input("c (상수항)", value=0.0)
        y = a * (x**2) + b * x + c
        title_label = f"y = {a}x² + {b}x + {c}"

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
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=title_label, line=dict(color='#1f77b4', width=3)))
    
    # 레이아웃 스타일 설정 (축 레이블, 그리드 등)
    fig.update_layout(
        title=title_label,
        xaxis_title="x",
        yaxis_title="y",
        template="plotly_white",
        hovermode="x unified" # 마우스를 대면 x축 기준 값이 한눈에 보임
    )
    
    # x=0, y=0 기준선 추가구현
    fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
    fig.add_vline(x=0, line_dash="dash", line_color="gray", line_width=1)

    # Streamlit에 Plotly 차트 띄우기
    st.plotly_chart(fig, use_container_width=True)
