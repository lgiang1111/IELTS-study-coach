# Phase 2 Plan: Agno Agent System & Logging/Tracing

## 1. Data Flow
```
User Prompt ──► [Main Coach Agent] ──(Gọi GA Tool)──► [ga_engine.py]
                       │                                    │
                       ▼                                    ▼
           [Reviewer Agent (LLM-as-Judge)] ◄─── Lịch học & Điểm dự báo JSON
                       │
                       ▼
            [Response + Logs/Trace]
```

## 2. Code Contracts (`agents.py` & `mcp_server.py`)
```python
# agents.py
def get_coach_agent(session_id: str = None) -> Agent: ...
def get_reviewer_agent() -> Agent: ...

# mcp_server.py
# Khởi tạo MCP Server sử dụng thư viện mcp (stdio transport)
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("IELTS Study Planner")
@mcp.tool()
def optimize_schedule(initial_bands: str, target_bands: str, total_days: int) -> str: ...
```

## 3. Tasks
### Wave 1 (Agno Agents & Logging)
- [x] **Task 2.1**: Tạo `agents.py`. Định nghĩa `CoachAgent` (suy luận và gọi GA tool) và `ReviewerAgent` (LLM-as-Judge đánh giá tính khả thi sư phạm). Ràng buộc Prompt của mỗi Agent cực kỳ ngắn (< 10 dòng) theo triết lý Agno.
  - *Verify*: Chạy thử prompt xem các Agent phân biệt được vai trò hay không.
- [x] **Task 2.2**: Cấu hình logging hệ thống ghi dấu vết Agent (Tracing). Ghi nhận toàn bộ thông tin: thời điểm bắt đầu gọi LLM, tool được chọn, đầu ra của GA engine, và quyết định của Reviewer vào tệp tin `logs/agent.log`.
  - *Verify*: Chạy Agent và kiểm tra xem file `logs/agent.log` có sinh ra log dạng structured hay không.

### Wave 2 (MCP Server & Tests)
- [x] **Task 2.3**: Tạo `mcp_server.py`. Sử dụng `mcp` SDK của Python để dựng stdio MCP Server. Đăng ký tool `optimize_schedule` gọi hàm `run_ga` từ Phase 1.
  - *depends_on*: Task 2.1
  - *Verify*: Chạy `python mcp_server.py` không gặp lỗi cú pháp.
- [x] **Task 2.4**: Tạo `tests/test_agents.py`. Viết unit tests kiểm tra: Agent nhận dạng đúng tool, ghi nhận log và Reviewer phê duyệt lịch học thành công.
  - *depends_on*: Task 2.2
  - *Verify*: Lệnh `pytest tests/test_agents.py` hoạt động tốt.

## 4. Failure Scenarios
| When (Sự kiện lỗi) | Then (Hành vi mong muốn) | Error Format / Code |
| :--- | :--- | :--- |
| Gemini API lỗi kết nối / Rate limit | Bắt ngoại lệ, thử lại (Retry) với cơ chế Backoff trong Agent | Ghi log WARNING vào file log, trả về thông báo lịch sự cho user |
| Reviewer từ chối lịch học của GA | Ghi log REJECT, gửi lại yêu cầu GA điều chỉnh tham số nhẹ và lập lại | Lịch trình học được tinh chỉnh tự động |

## 5. Rejection Criteria
- **DO NOT** viết prompt dài hơn 15 dòng cho mỗi Agent. Phải phân tách vai trò rõ ràng giữa Planner (Coach) và Judge (Reviewer).
- **DO NOT** để rò rỉ API Key ra file log (`logs/agent.log`). Phải ẩn hoặc lọc bỏ các chuỗi nhạy cảm trước khi lưu.

## 6. Cross-Phase Context
- **Assumes:** Thư viện tính toán GA từ `ga_engine.py` (Phase 1).
- **Exports:** 2 Agent và file ghi log để Phase 3 (CLI) và Phase 4 (UI Streamlit) gọi và đọc dữ liệu trace.

## 7. Acceptance Criteria
- Cả 2 Agent có thể trao đổi dữ liệu lịch học thành công dưới dạng JSON.
- Toàn bộ hành trình suy luận (suy nghĩ, gọi tool, đánh giá lịch) được lưu đầy đủ vào `logs/agent.log` và testable bằng unit test.
- MCP Server phản hồi tool call đúng định dạng khi giao tiếp qua stdio.

## 8. Traceability Matrix
- **Kaggle Concept 1 (Multi-agent):** Thực hiện tại Task 2.1, 2.4.
- **Kaggle Concept 2 (MCP Server):** Thực hiện tại Task 2.3.

---
## Outcome Block

### What Was Planned
Thiết lập kế hoạch chi tiết cho Phase 2 xây dựng hệ thống 2 Agent thông minh bằng Agno, tích hợp ghi vết log chi tiết và xây dựng local MCP server.

### Immediate Next Action
Chuẩn bị triển khai code của `agents.py` và `mcp_server.py` sau khi hoàn thành Phase 1.

### How to Measure
| Metric | Measurement Command | Expected Result |
| :--- | :--- | :--- |
| File existence | `ls -la .rune/plan-ielts-coach-phase2.md` | Tệp kế hoạch Phase 2 tồn tại ở đúng đường dẫn. |
