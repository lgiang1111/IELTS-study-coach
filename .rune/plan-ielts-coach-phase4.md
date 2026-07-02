# Phase 4 Plan: Streamlit Web UI & Deployability

## 1. Data Flow
```
User (Browser) ──► app.py (Streamlit UI) ──► [agents.py]
                        │                        │
                        ▼                        ▼
               matplotlib chart          st.expander (Đọc logs/agent.log)
```

## 2. Code Contracts (`app.py` & `requirements.txt`)
- `requirements.txt` chứa danh sách thư viện cố định: `streamlit`, `numpy`, `agno`, `google-genai`, `mcp`, `rich`, `pytest`, `matplotlib`.
- `app.py` chứa mã nguồn giao diện chính của Streamlit, quản lý `st.session_state` cho luồng hội thoại chat.

## 3. Tasks
### Wave 1 (Streamlit Layout & Integration)
- [x] **Task 4.1**: Tạo `requirements.txt` với đầy đủ các package cần thiết và phiên bản phù hợp.
  - *Verify*: Thử nghiệm cài đặt cục bộ qua lệnh `pip install -r requirements.txt`.
- [x] **Task 4.2**: Tạo `app.py`. Thiết kế giao diện premium:
  - Sidebar: Nhập điểm Band Score hiện tại và mục tiêu cho 4 kỹ năng, số ngày học mong muốn.
  - Vùng chính: Gồm 2 tab: "Chat Coach" (Chatbot tương tác với `CoachAgent`) và "Study Schedule" (Lịch học chi tiết + Biểu đồ tăng trưởng điểm số sử dụng `matplotlib`).
  - *Verify*: Chạy lệnh `streamlit run app.py` và kiểm tra giao diện hiển thị chính xác.

### Wave 2 (Trace Viewer & Deploy)
- [x] **Task 4.3**: Triển khai trình đọc log thời gian thực trên Web UI: tạo một `st.expander("Agent Trace Logging & Reasoning")` đọc liên tục từ tệp `logs/agent.log` để hiển thị quá trình suy nghĩ và gọi tool của Agent cho người dùng/giám khảo quan sát.
  - *depends_on*: Task 4.2
  - *Verify*: Khi Agent chạy lập lịch học, expander log cập nhật đúng tiến trình gọi.
- [x] **Task 4.4**: Deploy ứng dụng lên Streamlit Community Cloud. Cấu hình biến môi trường `GEMINI_API_KEY` trong Streamlit Settings.
  - *Verify*: Truy cập thành công vào link ứng dụng web công khai không cần đăng nhập.

## 4. Failure Scenarios
| When (Sự kiện lỗi) | Then (Hành vi mong muốn) | Error Format / Code |
| :--- | :--- | :--- |
| File logs/agent.log bị trống | Hiển thị thông báo "Chưa có log trace nào được ghi nhận..." | st.info("Waiting for agent execution...") |
| Streamlit Server bị quá tải bộ nhớ khi chạy GA | Giới hạn số thế hệ GA chạy tối đa 50 trên môi trường web | Tự động hạ tham số `generations` trên giao diện web |

## 5. Rejection Criteria
- **DO NOT** để lộ API key trong mã nguồn public trên GitHub.
- **DO NOT** sử dụng màu sắc Streamlit mặc định nhàm chán. Phải định cấu hình `.streamlit/config.toml` với theme Dark Mode hiện đại (curated palette).

## 6. Cross-Phase Context
- **Assumes:** Thư viện Agent và file log hoạt động từ Phase 2.
- **Exports:** Link web app hoạt động công khai để nộp cho Kaggle Capstone.

## 7. Acceptance Criteria
- Ứng dụng web Streamlit hoạt động chính xác trên cloud.
- Người dùng có thể chat và tạo lịch học cùng lúc, xem biểu đồ tăng điểm rõ ràng và xem log trace suy luận của AI trực quan.

## 8. Traceability Matrix
- **Kaggle Concept 5 (Deployability):** Thực hiện tại Task 4.4.
- **Kaggle Concept 4 (Security):** Thực hiện tại Task 4.2 (kiểm thực dữ liệu đầu vào trên UI).

---
## Outcome Block

### What Was Planned
Thiết lập kế hoạch chi tiết cho Phase 4 tập trung vào xây dựng và deploy giao diện Web Streamlit hoàn thiện với đầy đủ biểu đồ trực quan và bộ đọc trace log.

### Immediate Next Action
Chuẩn bị viết mã nguồn Streamlit cho `app.py` và deploy ứng dụng sau khi hoàn thành các Phase trước.

### How to Measure
| Metric | Measurement Command | Expected Result |
| :--- | :--- | :--- |
| File existence | `ls -la .rune/plan-ielts-coach-phase4.md` | Tệp kế hoạch Phase 4 tồn tại ở đúng đường dẫn. |
