# Developer Guide: IELTS Study Coach Capstone

## What This Does
Dự án cung cấp một trợ lý học tập IELTS thông minh giúp cá nhân hóa lịch học 4 kỹ năng (L/R/W/S) dựa trên thuật toán Genetic Algorithm và mô hình mệt mỏi nhận thức phi tuyến. Dự án phục vụ các học viên thi IELTS cần một lộ trình tối ưu hóa học tập khoa học.

## Quick Setup
Để cài đặt và chạy thử hệ thống cục bộ:

```bash
# 1. Tạo môi trường ảo Python
python -m venv .venv
source .venv/bin/activate  # Hoặc: .venv\Scripts\activate trên Windows

# 2. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 3. Tạo file cấu hình biến môi trường
cp .env.example .env
# Chỉnh sửa file .env để điền GEMINI_API_KEY=your_key_here

# 4. Chạy ứng dụng Streamlit UI
streamlit run app.py

# 5. Chạy thử nghiệm CLI (chỉ số năng lực học tập)
python cli.py
```

## Key Files
- `system_design_v3.md` — Bản thiết kế hệ thống Multi-Agent (Agno) được đề xuất làm kiến trúc chính.
- `Specs-5565918f-f1cf-5191-bbb5-e43fc8cbf30d.md` — Đặc tả toán học cho Genetic Algorithm, Fatigue function và Learning curve.
- `CLAUDE.md` — Cấu hình và lệnh chạy nhanh của dự án dành cho AI Agent.
- `docs/agno_agent_lessons.md` — Các bài học thực tiễn về Agno framework.

## How to Contribute
1. Tạo branch mới từ main để triển khai các module.
2. Viết mã nguồn tuân thủ các quy tắc trong `.rune/conventions.md`.
3. Kiểm tra mã nguồn bằng cách chạy kiểm thử (nếu có).
4. Tạo Pull Request và mô tả rõ các thay đổi.

## Common Issues
- **ModuleNotFoundError**: Môi trường ảo chưa được kích hoạt. Hãy chạy `source .venv/bin/activate`.
- **API Key Missing**: Chưa cấu hình file `.env` hoặc chưa import `GEMINI_API_KEY`. Hãy kiểm tra file `.env`.
- **GA Optimization takes too long**: Hãy giảm số lượng `population` xuống còn 100 hoặc `generations` xuống còn 50 trong cấu hình để chạy debug nhanh hơn.
