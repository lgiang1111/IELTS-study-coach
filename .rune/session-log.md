# Session Log

## 2026-06-30
- **Hoạt động**: Đánh giá kiến trúc thiết kế dự án Capstone và thiết lập cấu hình dự án với `rune onboard`.
- **Mục tiêu đạt được**:
  - Viết tài liệu phân tích và so sánh 3 phương án thiết kế (`system_design_evaluation.md`).
  - Đưa ra khuyến nghị thiết kế lai: Lean Multi-Agent bọc bởi một custom MCP Server.
  - Tạo `CLAUDE.md`, `.rune/conventions.md`, `.rune/decisions.md`, `.rune/progress.md`, và `.rune/instincts.md`.
- **Người thực hiện**: Antigravity (AI Coding Assistant).

## 2026-06-30 (Session 2)
- **Hoạt động**: Triển khai toàn bộ kế hoạch từ Phase 1 đến Phase 5 của Master Plan.
- **Mục tiêu đạt được**:
  - Hoàn thành lõi GA toán học (`ga_engine.py`) và bộ unit tests.
  - Xây dựng 2 Agent Agno (`CoachAgent`, `ReviewerAgent`), log tracing (`logs/agent.log`) và stdio MCP server (`mcp_server.py`).
  - Xây dựng CLI phong phú và Streamlit Web UI premium vẽ đồ thị dự phóng và xem log trực quan.
  - Thực hiện mô phỏng định lượng (simulation) 100 users, đạt tỷ lệ thành công 72%, tăng trung bình +1.04 bands.
  - Viết tài liệu báo cáo Kaggle Capstone (`KAGGLE_SUBMISSION.md`) và khởi tạo toàn bộ tài liệu hệ thống (`README.md`, `ARCHITECTURE.md`, `docs/API.md`, `CHANGELOG.md`).
  - Kiểm thử 16/16 testcases All-Green kết nối trực tiếp đến mô hình Gemini 2.5 Flash thông qua API Key của người dùng.
- **Người thực hiện**: Antigravity (AI Coding Assistant).

## 2026-06-30 (Session 3)
- **Hoạt động**: Đồng bộ cấu hình Onboarding và gia cố độ tin cậy kết nối mô hình.
- **Mục tiêu đạt được**:
  - Hoàn thiện và cập nhật `CLAUDE.md` với các câu lệnh chạy thực tế và thông tin tech stack chính xác.
  - Sửa lỗi bắt và hiển thị lỗi API quá tải (HTTP 503) bằng cách bọc các hàm gọi LLM trong cơ chế tự động thử lại (Retry) với độ trễ số mũ.
  - Thiết lập định dạng thông báo lỗi Markdown thân thiện cho người dùng cuối trên Streamlit khi API quá tải.
  - Kiểm tra 16/16 testcases và xác thực khả năng hiển thị biểu đồ tối ưu hóa trên trình duyệt thực tế.
- **Người thực hiện**: Antigravity (AI Coding Assistant).

## 2026-07-01 (Session 4)
- **Hoạt động**: Chạy kiểm thử xác thực toàn diện, tạo cấu hình mẫu `.env.example` và đóng gói nén mã nguồn dự án.
- **Mục tiêu đạt được**:
  - Chạy thành công toàn bộ test suite (16/16 tests passed).
  - Khởi tạo tệp `.env.example` loại bỏ API Key thật để bảo mật.
  - Đóng gói nén mã nguồn thành tệp `ielts-study-coach.zip` loại bỏ triệt để các thư mục rác, cache, virtualenv, và các thư mục/tập tin không liên quan.
- **Người thực hiện**: Antigravity (AI Coding Assistant).

## 2026-07-01 (Session 5)
- **Hoạt động**: Tái cấu trúc sang package modular, tích hợp SearXNG, bộ lọc bảo mật 2 lớp, nâng cấp Agent Execution Timeline UI/UX, và cập nhật tài liệu Kaggle.
- **Mục tiêu đạt được**:
  - Tách codebase sang package `ielts_coach/` chuyên nghiệp, chia nhỏ các agents thành các file độc lập.
  - Tích hợp công cụ tìm kiếm web SearXNG cho Coach Agent để tra cứu tài liệu ôn thi.
  - Xây dựng bộ lọc bảo mật 2 lớp (Regex + LLM Guardrail Agent) chống prompt injection và lọc nội dung ngoài luồng.
  - Tích hợp giao diện hiển thị dòng thời gian Agent Execution Timeline trên Streamlit UI.
  - Đồng bộ hóa toàn bộ tài liệu hệ thống (`README.md`, `ARCHITECTURE.md`, `docs/API.md`, `CLAUDE.md`, `KAGGLE_SUBMISSION.md`).
  - Ghi nhận định hướng xử lý vòng lặp sửa lịch học bị Reject (Auto-Refinement vs. Human-in-the-Loop) trong file thảo luận tương lai.
- **Người thực hiện**: Antigravity (AI Coding Assistant).

## 2026-07-01 (Session 6)
- **Activity**: 100% English localization audit, Streamlit LAN sharing configuration, and trace log viewer UI/UX design updates.
- **Key Achievements**:
  - Localized 100% of codebase strings, system outputs, log formats, mock data scenarios, and test assertions in `tests/test_integration.py` to English.
  - Fully translated all user-facing documentation: `KAGGLE_SUBMISSION.md`, `system_design_v3.md`, `CLAUDE.md`, and `README.md`.
  - Quarantined deprecated or mixed-language files into `docs/quarantine/`.
  - Configured Streamlit server to bind to network interfaces (`0.0.0.0`) enabling accessibility across the LAN.
  - Revamped Streamlit trace log visualizer to reverse line order (newest first) and parse `\n` to `<br/>` for correct wrapping and styled highlight coloring.
- **Performed by**: Antigravity (AI Coding Assistant).

## 2026-07-02 (Session 7)
- **Activity**: Fixed CLI unit testing and successfully initialized Git repository with remote push to GitHub.
- **Key Achievements**:
  - Resolved blocking pytest execution issue in `tests/test_cli.py` by mocking the Rich console inputs, making the test suite completely green and fast (< 1s).
  - Initialized Git workspace, created a clean `.gitignore` (excluding caches, venv, and logs), staged all project resources, and created the initial semantic commit.
  - Successfully connected local codebase to the remote GitHub repository at `git@github.com:lgiang1111/IELTS-study-coach.git` and pushed to the `main` branch.
- **Performed by**: Antigravity (AI Coding Assistant).


