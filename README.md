# 📄 Insurance Claim OCR Agent

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-8E75B2?logo=google&logoColor=white)
![EasyOCR](https://img.shields.io/badge/EasyOCR-Vision-green)

> **"비정형 보험금 청구서를 정형 데이터(JSON)로 변환하는 AI 에이전트"**

이 프로젝트는 **OCR(광학 문자 인식)** 의 한계를 **LLM(대거대 언어 모델)** 의 문맥 이해 능력으로 보완하는 **Data-Centric AI** 접근 방식을 보여줍니다. 
뭉개지거나 흐릿한 보험금 청구서 이미지에서도 핵심 정보(`청구인`, `사고일`, `진단명`, `은행명`, `계좌번호` 등)를 추출합니다.

---

## ✨ Key Features

- **Hybrid Extraction**: `EasyOCR`로 1차 텍스트를 추출하고, `Google Gemini`가 오타 교정 및 정보 구조화를 수행합니다.
- **Data Structuring**: 비정형 텍스트를 분석 가능한 **JSON** 포맷으로 자동 변환합니다.
- **Secure Access Control**: 
  - **Admin Mode**: 비밀번호 인증을 통과한 사용자만 파일 업로드 및 API 호출 가능.
  - **Guest Mode**: 미인증 방문자에게는 데모(Demo) 결과만 표시하여 API 비용 보호.
- **Intuitive Dashboard**: `Streamlit` 기반의 직관적인 UI로 누구나 쉽게 사용 가능.

## 🛠️ Tech Stack

| Category | Technology | Usage |
|----------|------------|-------|
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive Web Dashboard & UI |
| **LLM** | [Google Gemini](https://deepmind.google/technologies/gemini/) | Context-aware Typo Correction & Entity Extraction |
| **OCR** | [EasyOCR](https://github.com/JaidedAI/EasyOCR) | Text Detection & Recognition (Korean/English) |
| **Image Proc**| [OpenCV](https://opencv.org/) | Image Preprocessing |
| **Data** | [Pandas](https://pandas.pydata.org/) | Data Manipulation & Table View |

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- Google Gemini API Key

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/stats-dev/insurance-ocr-llm-project.git
cd insurance-ocr-llm-project

# Initialize and install dependencies with uv
uv sync
```

### 3. Configuration (Secrets)
Create a `.streamlit/secrets.toml` file in the project directory:

```toml
# .streamlit/secrets.toml
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
ADMIN_PASSWORD = "YOUR_ADMIN_PASSWORD"
```

### 4. Run App
```bash
uv run streamlit run app.py
```

## 📸 Workflow

1.  **게스트 접속 (Guest Access)**: 데모 이미지와 사전 계산된 JSON 결과만 확인 가능합니다.
2.  **관리자 로그인 (Admin Login)**: 사이드바에 비밀번호를 입력하여 모든 기능을 잠금 해제합니다.
3.  **이미지 업로드 (Upload)**: '보험금 청구서' 이미지를 업로드합니다.
4.  **AI 분석 (Process)**: 
    - **1단계 (OCR)**: 이미지에서 원시 텍스트를 추출합니다 (오타 포함 가능).
    - **2단계 (LLM)**: 문맥을 파악하여 오타를 수정하고 핵심 정보(`claimant_name`, `accident_date`, `diagnosis_name`, `bank_name`, `account_number`)를 추출합니다.
5.  **결과 다운로드 (Export)**: 분석된 결과를 `.json` 파일로 다운로드합니다.

## 📂 Project Structure

```
├── app.py                  # Main Application Logic
├── .streamlit/
│   └── secrets.toml        # API Keys & Passwords (Not committed)
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation
```
## 🌠 Demo Image

<img width="1643" height="838" alt="exampleimg" src="https://github.com/user-attachments/assets/10e4e68c-9842-45e1-8053-89028d4eef53" />  

(한글) 본 프로젝트는 과학기술정보통신부의 재원으로 한국지능정보사회진흥원의 지원을 받아 구축된 "OCR 데이터(금융 및 물류)"을 활용하여 수행된 연구입니다. 본 프로젝트에 활용된 데이터는 AI 허브(aihub.or.kr)에서 다운로드 받으실 수 있습니다.  
(영문) This project used datasets from 'The Open AI Dataset Project (AI-Hub, S. Korea)'. All data information can be accessed through 'AI-Hub (www.aihub.or.kr)'.





---
*Created with ❤️ by Antigravity*
