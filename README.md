# 📄 Insurance Claim OCR Agent

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-8E75B2?logo=google&logoColor=white)
![EasyOCR](https://img.shields.io/badge/EasyOCR-Vision-green)

> **"비정형 보험금 청구서를 정형 데이터(JSON)로 변환하는 AI 에이전트"**

이 프로젝트는 **OCR(광학 문자 인식)**의 한계를 **LLM(대거대 언어 모델)**의 문맥 이해 능력으로 보완하는 **Data-Centric AI** 접근 방식을 보여줍니다. 
뭉개지거나 흐릿한 보험금 청구서 이미지에서도 핵심 정보(청구인, 사고일, 진단명, 계좌번호 등)를 정확하게 추출합니다.

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
git clone https://github.com/your-username/medical-ocr-agent.git
cd medical-ocr-agent

# Install dependencies
pip install streamlit easyocr google-generativeai opencv-python pandas
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
streamlit run app.py
```

## 📸 Workflow

1.  **Guest Access**: View demo images and pre-computed JSON results.
2.  **Admin Login**: Enter password in the sidebar to unlock features.
3.  **Upload**: Upload an image of an "Insurance Claim Form".
4.  **Process**: 
    - **Step 1 (OCR)**: Extracts raw text (often contains errors).
    - **Step 2 (LLM)**: Corrects errors and extracts fields: `claimant_name`, `accident_date`, `diagnosis_name`, `claim_amount`, `bank_name`, `account_number`.
5.  **Export**: Download the result as a `.json` file.

## 📂 Project Structure

```
├── app.py                  # Main Application Logic
├── .streamlit/
│   └── secrets.toml        # API Keys & Passwords (Not committed)
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation
```

---
*Created with ❤️ by Antigravity*
