import streamlit as st
import math

st.set_page_config(page_title="고급 계산기", page_icon="🧮")

st.title("🧮 고급 계산기 웹앱")
st.write("사칙연산, 모듈러연산, 지수연산, 로그연산을 지원합니다.")

# 연산 종류 선택
operation = st.selectbox(
    "연산을 선택하세요",
    (
        "덧셈",
        "뺄셈",
        "곱셈",
        "나눗셈",
        "모듈러 연산",
        "지수 연산",
        "로그 연산"
    )
)

# 입력값
num1 = st.number_input("첫 번째 숫자", value=0.0)

# 로그 연산은 입력 방식이 다름
if operation == "로그 연산":
    base = st.number_input("로그 밑(base)", value=10.0, min_value=0.1)
else:
    num2 = st.number_input("두 번째 숫자", value=0.0)

# 계산 버튼
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
