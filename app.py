import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import os

from diagnosis import show_diagnosis  # diagnosis.py에서 함수 호출

# 문제 및 정답 설정 (이미지 경로와 5지선다 선택지)
problems = [
    {
        "question": "문제 1",
        "image_path": "images/problem_1.png",
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "②",
    },
    {
        "question": "문제 2",
        "image_path": "images/problem_2.png",
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "③",
    },
    {
        "question": "문제 3",
        "image_path": "images/problem_3.png",
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "③",
    },
    {
        "question": "문제 4",
        "image_path": "images/problem_4.png",
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "②",
    },
    {
        "question": "문제 5",
        "image_path": "images/problem_5.png",
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "①",
    },
    {
        "question": "문제 6",
        "image_path": "images/problem_6.png",
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "③",
    },
    {
        "question": "문제 7",
        "image_path": "images/problem_7.png",
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "④",
    },
    {
        "question": "문제 8",
        "image_path": "images/problem_8.png",
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "②",
    },
    {
        "question": "문제 9",
        "image_path": "images/problem_9.png",
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "②",
    },
    {
        "question": "문제 10",
        "image_path": "images/problem_10.png",
        "options": ["①", "②", "③", "④", "⑤"],
        "answer": "④",
    },
]

# 반응형 스타일 적용
st.markdown(
    """
    <style>
    .css-1v3fvcr {
        max-width: 100% !important;
        background-color: #ffffff;
    }
    .stRadio label {
        font-size: 16px;
    }
    .stSubheader {
        font-size: 20px;
    }
    .stButton > button {
        font-size: 18px;
        padding: 10px 20px;
    }
    .animation {
        animation: fadeIn 1s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 로그인 상태 관리
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 로그인 화면
if not st.session_state.logged_in:
    st.image("src/header.png", use_container_width=True)  # {{ edit_1 }}

    st.title("수학 진단 테스트 로그인")
    
    # 캠퍼스 선택 추가 (라디오 버튼)
    campus_options = ["서초캠퍼스", "강화캠퍼스", "안성캠퍼스"]
    selected_campus = st.radio("캠퍼스를 선택하세요:", campus_options)  # 캠퍼스 선택 라디오 버튼


    # 단계 선택 (중3~고3)
    step_options = ["중3 1학기", "중3 2학기", "고1 1학기", "고1 2학기", "고2 1학기", "고2 2학기", "고3 1학기", "고3 2학기"]  # 학년 및 학기 옵션
    selected_step = st.select_slider("현재 학년을 설정해주세요.", options=step_options)  # 단계 선택 슬라이더

    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if username == "72camp" and password == "1234":
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            st.session_state.page = "main"
            st.rerun()  # 페이지 새로고침
        else:
            st.error("사용자 이름 또는 비밀번호가 잘못되었습니다.")

else:
    # 기존 코드 시작
    st.image("src/header.png", use_container_width=True)  # {{ edit_1 }}
    st.markdown("<h1 style='text-align: center; white-space: nowrap;'>수학 진단 테스트</h1>", unsafe_allow_html=True)  # {{ edit_2 }}
    st.write("다음 수학 문제를 푸세요. 펜 모드를 켜서 문제 옆에 메모할 수 있습니다.")

    # 문제 번호 상태 관리
    if 'problem_index' not in st.session_state:
        st.session_state.problem_index = 0
    if 'correct_count' not in st.session_state:
        st.session_state.correct_count = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'pen_mode' not in st.session_state:
        st.session_state.pen_mode = False

    # 문제 인덱스 유효성 검사
    if st.session_state.problem_index >= len(problems):
        st.session_state.problem_index = len(problems) - 1  # 마지막 문제로 설정

    current_problem = problems[st.session_state.problem_index]

    # 사이드바에 페이지 선택 추가
    page = st.sidebar.selectbox("페이지 선택", ["문제 풀이", "진단 결과지"])

    if page == "문제 풀이":
        # 두 열로 나누기
        col1, col2 = st.columns([3, 1])

        with col1:
            # 문제 출력
            st.subheader(current_problem["question"])

            # 문제 이미지 로드 및 표시
            image = Image.open(current_problem["image_path"])
            st.image(image, caption="", use_container_width=True)

            # 5지선다 옵션 생성
            user_answer = st.radio(
                "선택지를 고르세요:",
                current_problem["options"],
                key=f"radio_{st.session_state.problem_index}_{current_problem['question']}",
            )

        # 펜 모드 토글 버튼 (문제 아래로 이동)
        if st.button("펜 모드 켜기/끄기"):
            st.session_state.pen_mode = not st.session_state.pen_mode

        # 그리기 캔버스 (메모 공간) 문제 아래에 위치
        if st.session_state.pen_mode:
            st.write("메모 공간:")
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",  # 채우기 색상
                stroke_width=2,
                stroke_color="#000000",
                background_color="#ffffff",  # 하얀 배경
                height=400,
                drawing_mode="freedraw" if st.session_state.pen_mode else "transform",
                key=f"canvas_{st.session_state.problem_index}",
            )
        else:
            st.write("")

        # 답안 기록
        if len(st.session_state.answers) <= st.session_state.problem_index:
            st.session_state.answers.append(user_answer)
        else:
            st.session_state.answers[st.session_state.problem_index] = user_answer

        # 다음 문제로 넘어가기 버튼
        if st.session_state.problem_index < len(problems) - 1:
            if st.button("다음 문제"):
                st.session_state.problem_index += 1
                if len(st.session_state.answers) <= st.session_state.problem_index:
                    st.session_state.answers.append("")
                st.rerun()
        else:
            # 모든 문제를 푼 후 결과 표시
            if st.button("결과 확인"):
                st.session_state.correct_count = 0
                for idx, problem in enumerate(problems):
                    correct_answer = problem["answer"]
                    user_answer = st.session_state.answers[idx]

                    if user_answer == correct_answer:
                        st.success(f"{problem['question']} 정답입니다!")
                        st.session_state.correct_count += 1
                        # 문제 1을 맞췄을 때의 시지
                        if idx == 0:
                            st.markdown(
                                """
                                <div class="animation">
                                    정확한 전개과정을 이해하고 있습니다. 전개는 인수분해의 역과정이므로, 인수분해로 넘어갈 수 있습니다.
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    else:
                        st.error(f"{problem['question']} 틀렸습니다. 정답은 {correct_answer}입니다.")
                        # 문제 1번은 맞추고 2번은 틀렸을 때의 메시지
                        if idx == 1:
                            st.markdown(
                                """
                                <div class="animation">
                                    전개과정을 이해하고 있으나, 2번 문제를 풀때는 무작정 대입하는 것이아니라, 준식을 먼저 전개하여 주어진 X를 A,B로 간결하게 표현한 뒤, 대입하는 과정이 요구됩니다.
                                    즉, 전개의 과정은 이해하였으나, 문제를 접근하는 응용력을 확인할 필요가 있습니다.
                                    쎈B단계 대표유형을 통해 다양한 유형을 접하는 것이 필요합니다.
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                st.write(f"정답 개수: {st.session_state.correct_count}/{len(problems)}")
                if st.session_state.correct_count == len(problems):
                    st.success("완벽합니다! 모든 문제를 맞췄습니다.")
                else:
                    st.warning("모든 문제를 풀지 못했습니다. 다시 시도해보세요.")

            # 진단 결과지로 이동하는 버튼 추가
            if st.button("진단 결과지로 이동"):
                st.session_state.problem_index = len(problems)  # 결과 페이지로 이동
                st.session_state.answers = []  # 이전 답안 초기화 (선택 사항)
                show_diagnosis(st.session_state.correct_count, len(problems))  # 진단 결과 표시
                st.stop()  # 이후 코드 실행 중지

        # 이전 문제로 돌아가기 버튼
        if st.session_state.problem_index > 0:
            if st.button("이전 문제"):
                st.session_state.problem_index -= 1
                st.rerun()

        # 테스트 다시 시작 버튼을 사이드바에 추가
        if st.sidebar.button("테스트 다시 시작", key="restart_button"):
            st.session_state.problem_index = 0
            st.session_state.correct_count = 0
            st.session_state.answers = []
            st.session_state.pen_mode = False
            st.rerun()
    else:  # "진단 결과지" 페이지
        show_diagnosis(st.session_state.correct_count, len(problems))