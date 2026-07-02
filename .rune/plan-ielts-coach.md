# Master Plan: IELTS Study Coach Agent (Option A)

## 1. Overview
AI Agent lập lịch học IELTS tối ưu hóa bằng Genetic Algorithm (GA) không mệt mỏi nhận thức, tích hợp Logging/Tracing và Unit Tests để đảm bảo độ tin cậy và đạt điểm tuyệt đối.

## 2. Kế hoạch các giai đoạn (Phases)
| Phase | Goal / Output | Files | Status |
| :--- | :--- | :--- | :---: |
| **Phase 1** | Viết thuật toán GA thuần (`ga_engine.py`) & Unit Tests (`tests/test_ga.py`). | `ga_engine.py`, `tests/test_ga.py` | ✅ Completed |
| **Phase 2** | Triển khai 2 Agno Agents + Custom Logging/Tracing & local MCP Server. | `agents.py`, `mcp_server.py` | ✅ Completed |
| **Phase 3** | Viết giao diện CLI tích hợp Trace Logs (đạt tiêu chí CLI Agent Skills). | `cli.py` | ✅ Completed |
| **Phase 4** | Xây dựng Web UI Streamlit hiển thị Trace Logs & Deploy Streamlit Cloud. | `app.py`, `requirements.txt` | ✅ Completed |
| **Phase 5** | Chạy simulation 1000 users lấy biểu đồ tối ưu & Soạn tài liệu Kaggle. | `simulation.py`, `KAGGLE_SUBMISSION.md` | ✅ Completed |

## 3. Kiến trúc & Quyết định kỹ thuật
- **Unit Testing (pytest):** Viết kiểm thử cho Learning curve, Fatigue, Fitness và GA constraints.
- **Agent Logging & Tracing:** Sử dụng Python `logging` + Agno Agent logger để ghi lại chi tiết các bước suy luận, gọi tool và phản hồi của Reviewer làm minh chứng "LLM-as-Judge".
- **MCP & Decoupled GA:** GA Engine độc lập, được kiểm thử kỹ lưỡng trước khi bọc thành MCP.

## 4. Rủi ro & Phòng ngừa
- **Rủi ro:** Rate limit của Gemini API khi chạy test hoặc simulation.
- **Phòng ngừa:** Mock API trong unit tests, tích hợp cơ chế Retry & Exponential Backoff ở Phase 2.

---
## Outcome Block

### What Was Planned
Cập nhật Kế hoạch tổng thể (Master Plan) theo yêu cầu của người dùng: loại bỏ Greedy Baseline để tinh giản hệ thống, bổ sung kiểm thử tự động (Unit Tests) vào Phase 1 và cơ chế ghi log (Logging/Tracing) cho Agent vào Phase 2.

### Immediate Next Action
Đợi người dùng phê duyệt bản kế hoạch tổng thể đã cập nhật để bắt đầu viết mã nguồn GA Engine và bộ unit tests đi kèm trong Phase 1.

### How to Measure
| Metric | Measurement Command | Expected Result |
| :--- | :--- | :--- |
| File existence | `ls -la .rune/plan-ielts-coach.md` | Tệp kế hoạch tổng thể tồn tại ở đúng đường dẫn. |
| Verification of changes | `grep -i "test" .rune/plan-ielts-coach.md` | Có sự xuất hiện của các tác vụ kiểm thử (unit tests) và ghi log (logging). |
