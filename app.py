from flask import Flask, render_template, request, send_file
from pdf_generator import generate_vocab_pdf
import random
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    english = request.form.getlist("english[]")
    korean = request.form.getlist("korean[]")
    hide_mode = request.form.get("hide_mode", "korean")
    student_name = request.form.get("student_name")

    # 빈 값 필터링 (둘 다 비어있는 항목 제외)
    pairs = [(e.strip(), k.strip()) for e, k in zip(english, korean) if e.strip() or k.strip()]
    
    # 순서 무작위 섞기
    random.shuffle(pairs)

    # PDF 생성
    pdf_buffer = generate_vocab_pdf(pairs, hide_mode=hide_mode, student_name=student_name)

    return send_file(pdf_buffer, as_attachment=True,
                     download_name="vocab_test.pdf",
                     mimetype="application/pdf")

if __name__ == "__main__":
    # Use PORT env var when available (Render sets $PORT)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
