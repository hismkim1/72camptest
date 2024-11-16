import streamlit as st
from pdf2image import convert_from_path
import os

def display_pdf(pdf_path):
    images = convert_from_path(pdf_path)

    # CSS를 사용하여 이미지 사이의 여백 제거
    st.markdown("""
        <style>
            .stImage > img {
                display: block;
                margin: 0;
                padding: 0;
            }
        </style>
    """, unsafe_allow_html=True)

    for i, image in enumerate(images):
        st.image(image, use_container_width=True)


def show_diagnosis(correct_count, total_problems):
    st.title("진단 결과지")
    st.write(f"정답 개수: {correct_count}/{total_problems}")
    if correct_count == total_problems:
        st.success("완벽합니다! 모든 문제를 맞췄습니다.")
    else:
        st.warning("모든 문제를 풀지 못했습니다. 다시 시도해보세요.")
        
        # 문제 1번을 맞췄을 때의 메시지
        if correct_count >= 1:
            st.markdown(
                """
                정확한 전개과정을 이해하고 있습니다. 전개는 인수분해의 역과정이므로, 인수분해로 넘어갈 수 있습니다.
                """
            )
        
        # 문제 1번을 맞추고 2번을 틀렸을 때의 메시지
        if correct_count == 1:
            st.markdown(
                """
                전개과정을 이해하고 있으나, 2번 문제를 풀때는 무작정 대입하는 것이아니라, 준식을 먼저 전개하여 주어진 X를 A,B로 간결하게 표현한 뒤, 대입하는 과정이 요구됩니다.
                즉, 전개의 과정은 이해하였으나, 문제를 접근하는 응용력을 확인할 필요가 있습니다.
                쎈B단계 대표유형을 통해 다양한 유형을 접하는 것이 필요합니다.
                """
            )
    doc_file = ('result/doc.pdf')            
    pdf_file_path = 'result/doc.pdf'

    if os.path.exists(pdf_file_path):
        display_pdf(pdf_file_path)
    else:
        st.error("PDF 파일을 찾을 수 없습니다.")