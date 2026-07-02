# Architecture Decisions

| Date | Decision | Rationale | Status |
| :--- | :--- | :--- | :--- |
| 2026-06-30 | Chọn kiến trúc "Lean Multi-Agent + MCP Server" | Tối đa hóa số lượng tiêu chí Kaggle Capstone đạt được (Multi-agent, MCP, Security, Deployability) trong khi tối thiểu hóa độ phức tạp và độ trễ so với phương án 8-Agent. | APPROVED |
| 2026-06-30 | Sử dụng Agno Framework và Gemini 2.0 Flash | Agno hỗ trợ Multi-agent Orchestration và Workflow Pipeline mạnh mẽ, Gemini 2.0 Flash xử lý Function Calling nhanh chóng và hiệu quả. | APPROVED |
| 2026-07-01 | Nâng cấp mô hình lên Gemini 2.5 Flash & Truyền API Key trực tiếp | Do endpoint của Google đã gỡ bỏ gemini-2.0-flash và yêu cầu truyền khóa API trực tiếp vào constructor của lớp Google Gemini SDK trong Agno để tránh lỗi GOOGLE_API_KEY. | APPROVED |
| 2026-07-01 | Rejection 1-Retry Recovery with HITL Escalation | Implemented automated 1-retry self-healing on ReviewerAgent rejection; if second attempt fails, it escalates to Human-in-the-Loop parameter adjustment. | APPROVED |
| 2026-06-30 | Triển khai cơ chế Retry với Exponential Backoff & Định dạng lỗi cho Agents | Tránh crash luồng chạy và ngăn chặn lỗi 503 hiển thị thô dạng JSON lên giao diện người dùng bằng cách tự động gọi lại mô hình và hiển thị cảnh báo thân thiện. | APPROVED |
| 2026-07-01 | 100% English Localization | Standardized all codebase strings, logs, mock scenarios, tests, and documents to English for public deployment and judging panel evaluation. | APPROVED |
| 2026-07-01 | LAN Binding for Streamlit | Bound Streamlit to 0.0.0.0 instead of 127.0.0.1 to facilitate local network testing on mobile devices and other PCs. | APPROVED |
| 2026-07-01 | Reversed Color-Coded Logs with HTML Breaks | Designed custom HTML div log viewer with newest logs first, component colors, and HTML line break mapping. | APPROVED |


