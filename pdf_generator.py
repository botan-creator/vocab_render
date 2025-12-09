import os
import io
from fpdf import FPDF
from datetime import datetime

def get_korean_font_path():
    """한글 폰트 경로를 찾습니다."""
    # 1. 프로젝트 루트 확인
    project_font = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
    if os.path.exists(project_font):
        print(f"[폰트] 프로젝트 폰트 사용: {project_font}")
        return project_font
    
    # 2. Windows 시스템 폰트
    windows_fonts = [
        "C:\\Windows\\Fonts\\NanumGothic.ttf",
        "C:\\Windows\\Fonts\\malgun.ttf",
        "C:\\Windows\\Fonts\\NotoSansCJKkr-Regular.otf",
    ]
    
    for font_path in windows_fonts:
        if os.path.exists(font_path):
            print(f"[폰트] 시스템 폰트 사용: {font_path}")
            return font_path
    
    raise FileNotFoundError("한글 폰트를 찾을 수 없습니다. NanumGothic.ttf를 프로젝트 루트에 놓으세요.")

# PDF 생성용 유틸: 표 스타일(영어학원 스타일)
def generate_vocab_pdf(vocab_pairs, hide_mode='korean', student_name=None):
    """
    vocab_pairs: list of (eng, kor)
    hide_mode: 'korean' -> 뜻 숨기기 (영어만 보임)
               'english' -> 영어 숨기기 (뜻만 보임)
    student_name: optional string
    returns: BytesIO containing PDF
    """
    pdf = FPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # 한글 폰트 등록 (fpdf2는 TTF 폰트를 직접 사용)
    font_path = get_korean_font_path()
    pdf.add_font("KoreanFont", fname=font_path)
    pdf.set_font("KoreanFont", size=14)
    
    # 제목
    pdf.cell(0, 10, "영단어 연습지", ln=True, align='C')
    pdf.ln(2)

    # 학생 이름 / 날짜 행
    today = datetime.now().strftime("%Y-%m-%d")
    name_text = f"이름: {student_name}" if student_name else "이름: __________________"
    pdf.set_font("KoreanFont", size=11)
    pdf.cell(0, 8, f"{name_text}    /    날짜: {today}", ln=True)
    pdf.ln(6)

    # 표 머리 (문제지)
    pdf.set_font("KoreanFont", size=11)
    col_w = (pdf.w - 2 * pdf.l_margin) / 3.0  # 3열: 번호 / 컬럼A / 컬럼B
    # 헤더 스타일
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(20, 10, "번호", 1, 0, 'C', fill=True)
    pdf.cell(col_w - 20, 10, "영단어", 1, 0, 'C', fill=True)
    pdf.cell(col_w - 20, 10, "뜻", 1, 1, 'C', fill=True)

    # 문제지 행들
    for idx, (eng, kor) in enumerate(vocab_pairs, start=1):
        pdf.cell(20, 9, str(idx), 1, 0, 'C')
        if hide_mode == 'korean':
            # 영어 표시, 뜻 빈칸
            pdf.cell(col_w - 20, 9, eng if eng else "", 1, 0)
            pdf.cell(col_w - 20, 9, "", 1, 1)
        else:
            # 영어 빈칸, 뜻 표시
            pdf.cell(col_w - 20, 9, "", 1, 0)
            pdf.cell(col_w - 20, 9, kor if kor else "", 1, 1)

    # ===== 정답지 페이지 =====
    pdf.add_page()
    pdf.set_font("KoreanFont", size=14)
    pdf.cell(0, 10, "정답지", ln=True, align='C')
    pdf.ln(4)
    pdf.set_font("KoreanFont", size=9)

    pdf.cell(20, 10, "번호", 1, 0, 'C', fill=True)
    pdf.cell(col_w - 20, 10, "영단어", 1, 0, 'C', fill=True)
    pdf.cell(col_w - 20, 10, "뜻", 1, 1, 'C', fill=True)

    for idx, (eng, kor) in enumerate(vocab_pairs, start=1):
        pdf.cell(20, 9, str(idx), 1, 0, 'C')
        pdf.cell(col_w - 20, 9, eng if eng else "", 1, 0)
        pdf.cell(col_w - 20, 9, kor if kor else "", 1, 1)

    pdf_bytes = pdf.output(dest='S')
    buffer = io.BytesIO(pdf_bytes)
    buffer.seek(0)
    return buffer


