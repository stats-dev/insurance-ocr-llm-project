import streamlit as st
import easyocr
import google.generativeai as genai
import cv2
import numpy as np
import pandas as pd
import json
import os

# ---------------------------------------------------------
# 1. 설정 및 초기화
# ---------------------------------------------------------
# 페이지 설정
st.set_page_config(page_title="Insurance Claim OCR Agent", layout="wide")

# 제목 및 설명
st.title("📄 보험금 청구서 OCR/LLM 자동화 에이전트")
st.markdown("""
**보험금 청구서** 이미지를 업로드하면 OCR로 읽고, 
**LLM** 으로 주요 정보를 추출하여 정형 데이터(JSON)로 변환해줍니다.
""")

# Gemini API 설정
try:
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    else:
        # 로컬 개발 환경에서만 사용하는 fallback (권장하지 않음, secrets.toml 사용 권장)
        pass
except FileNotFoundError:
    # secrets.toml 파일이 없을 때의 처리
    pass

# API Key 확인 및 설정
if "GOOGLE_API_KEY" not in os.environ:
    st.error("API Key가 설정되지 않았습니다. .streamlit/secrets.toml 파일에 GOOGLE_API_KEY를 설정하거나 배포 환경의 Secrets에 추가하세요.")
    st.stop()
    
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# EasyOCR Reader 로드 (한국어, 영어) -> 캐싱하여 속도 향상
@st.cache_resource
def load_ocr_model():
    # Streamlit Cloud는 CPU 환경이므로 gpu=False로 설정하여 경고 제거 및 호환성 확보
    return easyocr.Reader(['ko', 'en'], gpu=False)

reader = load_ocr_model()

# ---------------------------------------------------------
# 2. 핵심 기능 함수 (OCR & LLM)
# ---------------------------------------------------------

def extract_text_from_image(image_bytes):
    """EasyOCR을 사용하여 이미지에서 텍스트(Raw Data) 추출"""
    # 이미지를 numpy array로 변환
    file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # OCR 실행
    results = reader.readtext(img, detail=0)
    raw_text = " ".join(results)
    return raw_text, img

def correction_with_llm(raw_text):
    """Gemini를 사용하여 OCR 결과 보정 및 구조화"""
    # 사용 가능한 모델: gemini-3-pro-preview 등
    model = genai.GenerativeModel('gemini-3-pro-preview')
    
    # 프롬프트 엔지니어링 (여기가 핵심!)
    # OCR의 오타를 문맥으로 파악해 수정하고, JSON으로 뽑아내도록 지시
    prompt = f"""
    당신은 베테랑 보험 심사역입니다. 
    아래 텍스트는 '보험금 청구서'를 OCR로 읽어낸 결과(Raw Data)입니다. 
    인식 오류나 오타가 많이 포함되어 있을 수 있습니다.
    
    [수행 미션]
    1. 문맥을 파악하여 오타를 교정하세요. 
    2. 아래 항목을 찾아 JSON 형식으로만 출력하세요. (Markdown 코드 블럭 없이 순수 JSON만 출력)
    
    [추출 항목]
    - claimant_name (청구인/피보험자 성명)
    - accident_date (사고일자/발병일, YYYY-MM-DD 형식)
    - diagnosis_name (진단명 또는 청구사유. 예: '발목 염좌', '독감' 등)
    - bank_name (지급받을 계좌 은행명)
    - account_number (지급받을 계좌번호, 숫자만)

    [OCR Raw Text]
    {raw_text}
    """
    
    response = model.generate_content(prompt)
    return response.text

# ---------------------------------------------------------
# 3. UI 레이아웃 구성
# ---------------------------------------------------------

# 사이드바: 관리자 인증
with st.sidebar:
    st.header("🔐 관리자 로그인")
    password = st.text_input("접속 암호를 입력하세요", type="password")
    
    is_admin = False
    if "ADMIN_PASSWORD" in st.secrets:
        if password == st.secrets["ADMIN_PASSWORD"]:
            is_admin = True
            st.success("인증 성공! ✅")
        else:
            if password:
                st.error("암호가 틀렸습니다.")
    else:
        st.warning("secrets.toml에 ADMIN_PASSWORD가 설정되지 않았습니다.")

col1, col2 = st.columns(2)

# --- 관리자 모드: 실제 기능 수행 ---
if is_admin:
    with col1:
        st.header("1️⃣ 청구서 업로드 (Input)")
        uploaded_file = st.file_uploader("보험금 청구서 이미지를 올려주세요", type=['png', 'jpg', 'jpeg'])

        if uploaded_file is not None:
            # 이미지 표시
            st.image(uploaded_file, caption="업로드된 청구서", use_column_width=True)
            
            with st.status("🔍 OCR 분석 중...", expanded=True) as status:
                st.write("이미지에서 텍스트를 추출하고 있습니다...")
                # OCR 수행
                uploaded_file.seek(0) # 파일 포인터 초기화
                raw_text, _ = extract_text_from_image(uploaded_file)
                st.write("✅ 추출 완료!")
                status.update(label="OCR 완료!", state="complete", expanded=False)
            
            st.subheader("Raw OCR Result (전처리 전)")
            st.code(raw_text, language='text')

    with col2:
        st.header("2️⃣ LLM 후처리 결과 (Output)")
        
        if uploaded_file is not None:
            if st.button("🚀 AI 보정 및 구조화 실행"):
                with st.spinner("🤖 LLM이 데이터를 보정하고 구조화하는 중입니다..."):
                    try:
                        # LLM 수행
                        json_result = correction_with_llm(raw_text)
                        
                        # JSON 파싱 (혹시 모를 마크다운 제거 처리)
                        clean_json = json_result.replace("```json", "").replace("```", "").strip()
                        data = json.loads(clean_json)
                        
                        # 결과 표시
                        st.success("데이터 구조화 성공!")
                        
                        # 1. 보기 좋은 JSON 트리
                        st.json(data)
                        
                        # 2. 비교 테이블 (데이터프레임)
                        df = pd.DataFrame([data])
                        st.subheader("📊 정형 데이터 테이블")
                        st.dataframe(df, use_container_width=True)
                        
                        # 3. 다운로드 버튼
                        st.download_button(
                            label="📥 JSON 다운로드",
                            data=json.dumps(data, ensure_ascii=False, indent=2),
                            file_name="insurance_claim_data.json",
                            mime="application/json"
                        )
                        
                    except Exception as e:
                        st.error(f"구조화 중 오류가 발생했습니다: {e}")
                        st.warning("OCR 결과가 너무 부정확하거나, API 키를 확인해주세요.")

# --- 게스트 모드: 데모만 표시 ---
else:
    st.divider()
    st.warning("🔒 **게스트 모드:** API 사용량 제한을 위해 파일 업로드는 관리자에게만 허용됩니다.")
    st.info("아래는 AI 에이전트가 어떻게 동작하는지 보여주는 **Demo** 입니다.")
    
    demo_col1, demo_col2 = st.columns(2)
    
    with demo_col1:
        st.subheader("[Demo] 입력 이미지")
        # 로컬 데모 이미지 사용
        sample_img_path = "assets/sample_image.jpg"
        if os.path.exists(sample_img_path):
            st.image(sample_img_path, caption="데모 보험금 청구서", use_column_width=True)
        else:
             st.error("데모 이미지를 찾을 수 없습니다.")
        
        st.subheader("Raw OCR Result")
        st.code("... 청구인: 홍길동 ... 사고일: 2024년 1월 1일 ... 진단명: 골절 ...", language="text")

    with demo_col2:
        st.subheader("[Demo] AI 구조화 결과")
        st.json({
            "claimant_name": "홍길동",
            "accident_date": "2024-01-01",
            "diagnosis_name": "우측 발목 골절",
            "bank_name": "신한은행",
            "account_number": "110-123-456789"
        })
        st.caption("AI가 위와 같이 주요 정보를 자동으로 추출하고 정형화합니다.")

# 하단 설명
st.divider()
st.info("💡 **Tip:** 일반 OCR 라이브러리 한계를 LLM의 '문맥 이해 능력'으로 보정하는 **Data-Centric AI** 접근 방식을 보여줍니다")
