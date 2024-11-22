#!/usr/bin/env bash
set -o errexit

# Poetry로 의존성 설치
poetry install --no-root

# Streamlit 앱 실행
poetry run streamlit run app.py --host=0.0.0.0 --port=8000