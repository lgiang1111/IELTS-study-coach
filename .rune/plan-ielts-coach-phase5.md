# Phase 5 Plan: Evaluation & Kaggle Submission

## 1. Data Flow
```
Simulation (1000 users) ──► simulation.py ──► Convergence Stats & Graphs
                                                      │
                                                      ▼
YouTube Video Demo & CLI Demo ◄─────────────── KAGGLE_SUBMISSION.md
```

## 2. Code Contracts (`simulation.py` & `KAGGLE_SUBMISSION.md`)
- `simulation.py` tự động sinh 1000 hồ sơ người dùng ảo ngẫu nhiên, chạy GA lập lịch học và tính toán: tỷ lệ hội tụ (convergence rate), điểm fitness trung bình, và độ mệt mỏi được kiểm soát như thế nào. Lưu đồ thị thống kê thành tệp ảnh `docs/simulation_results.png`.
- `KAGGLE_SUBMISSION.md` chứa bài viết Writeup hoàn thiện (< 2500 từ) chuẩn định dạng Kaggle Capstone.

## 3. Tasks
### Wave 1 (Simulation & Writeup)
- [x] **Task 5.1**: Tạo `simulation.py`. Viết mã nguồn mô phỏng chạy tối ưu hóa lịch học cho 1000 users ảo. Trích xuất các chỉ số định lượng (tổng điểm fitness, độ giảm fatigue trung bình) và vẽ biểu đồ phân phối điểm bằng `matplotlib`.
  - *Verify*: Chạy `python simulation.py` sinh ra file ảnh đồ thị trong thư mục `docs/`.
- [x] **Task 5.2**: Tạo `KAGGLE_SUBMISSION.md`. Soạn thảo bài viết Kaggle Writeup chi tiết: giới thiệu dự án, kiến trúc tác nhân Agno, giao thức MCP Server tích hợp, các tính năng bảo mật (Security), hướng dẫn chạy ứng dụng qua CLI và link Web App công khai.
  - *Verify*: Kiểm tra số lượng từ của bài viết đảm bảo dưới 2500 từ.

### Wave 2 (Video Demo Plan)
- [x] **Task 5.3**: Soạn thảo kịch bản và kế hoạch quay video demo trên YouTube (<= 5 phút). Video cần thể hiện:
  - Giới thiệu bài toán phân bổ thời gian học IELTS (1 phút).
  - Quá trình viết code ("Vibe Coding") cùng trợ lý AI Antigravity (2 phút).
  - Demo chạy thử CLI và Streamlit Web UI cùng biểu đồ phân tích và hộp thoại trace log (2 phút).
  - *Verify*: Kịch bản video đầy đủ, rõ ràng và mạch lạc.

## 4. Failure Scenarios
| When (Sự kiện lỗi) | Then (Hành vi mong muốn) | Error Format / Code |
| :--- | :--- | :--- |
| Chạy mô phỏng 1000 users quá chậm | Tối ưu hóa mảng tính toán bằng NumPy hoặc giảm số lượng user xuống 300 | Giảm thời gian chạy simulation xuống dưới 1 phút |
| Writeup vượt quá giới hạn 2500 từ | Cắt bớt phần lý thuyết hàn lâm, tập trung vào mô tả kỹ thuật và kết quả | Đảm bảo đếm từ luôn < 2500 |

## 5. Rejection Criteria
- **DO NOT** nộp bài viết dạng hàn lâm nghiên cứu thuần túy mà thiếu phần mô tả cách hoạt động của **Agent** và **MCP**.
- **DO NOT** bỏ quên việc chèn các hình ảnh biểu đồ mô phỏng và sơ đồ thiết kế vào bài viết Writeup để tăng tính trực quan.

## 6. Cross-Phase Context
- **Assumes:** GA Engine từ Phase 1 và Hệ thống Agent/UI từ Phase 2, 4 hoạt động ổn định.
- **Exports:** Toàn bộ hồ sơ nộp bài Capstone (Kaggle Writeup, Video Link, GitHub repo, public Streamlit Web URL) sẵn sàng gửi trước hạn chót 6/7/2026.

## 7. Acceptance Criteria
- File mô phỏng chạy thành công, trích xuất dữ liệu khoa học rõ ràng chứng minh thuật toán GA hoạt động tốt.
- Bài viết Kaggle Writeup hoàn thiện và đạt tiêu chuẩn nộp bài của cuộc thi.

## 8. Traceability Matrix
- **Kaggle Pitch Requirement (30 pts):** Thực hiện tại Task 5.2 (Writeup) và Task 5.3 (Video).
- **Kaggle Concept 3 (Antigravity Video):** Thực hiện tại Task 5.3 (quay video lập trình cùng Antigravity).

---
## Outcome Block

### What Was Planned
Thiết lập kế hoạch chi tiết cho Phase 5 tập trung chạy thử nghiệm mô phỏng quy mô lớn, biên soạn bài nộp Kaggle Writeup và lên kịch bản video demo.

### Immediate Next Action
Chuẩn bị kịch bản quay video và chạy simulation sau khi ứng dụng web và CLI đã hoàn thành.

### How to Measure
| Metric | Measurement Command | Expected Result |
| :--- | :--- | :--- |
| File existence | `ls -la .rune/plan-ielts-coach-phase5.md` | Tệp kế hoạch Phase 5 tồn tại ở đúng đường dẫn. |
