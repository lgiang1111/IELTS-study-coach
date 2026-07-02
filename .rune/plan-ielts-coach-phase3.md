# Phase 3 Plan: CLI Interface & Agent Skills

## 1. Data Flow
```
Terminal Commands ──► cli.py ──► [CoachAgent]
                         │
                         ▼
        Console Layout (Rich) ◄── [Output & logs/agent.log]
```

## 2. Code Contracts (`cli.py`)
- CLI hỗ trợ 2 chế độ:
  1. Chế độ Chat tương tác (`python cli.py`)
  2. Chế độ Tham số nhanh (`python cli.py --initial "6.0,6.5,5.5,6.0" --target "7.0,7.0,6.5,6.5" --days 30`)

## 3. Tasks
### Wave 1 (CLI Core & Layout)
- [x] **Task 3.1**: Tạo `cli.py`. Thiết lập parser tham số (`argparse`) và cấu trúc vòng lặp chat (while-loop) giao tiếp với `CoachAgent` từ `agents.py`.
  - *Verify*: Chạy `python cli.py --help` hiển thị các cờ lệnh hướng dẫn đầy đủ.
- [x] **Task 3.2**: Tích hợp thư viện `rich` để định dạng giao diện terminal:
  - In lịch học dạng Bảng (Table) trực quan.
  - Hiển thị logs/trace suy luận của Agent trong một Panel phụ bên dưới để người dùng theo dõi suy luận của AI theo thời gian thực.
  - *Verify*: Chạy lịch học thử qua CLI và xem giao diện hiển thị lịch học và log suy luận có đẹp mắt không.

### Wave 2 (CLI Integration Tests)
- [x] **Task 3.3**: Tạo `tests/test_cli.py`. Kiểm thử tự động giao diện CLI bằng cách mock input và kiểm tra CLI kết thúc thành công (exit code 0).
  - *depends_on*: Task 3.1, Task 3.2
  - *Verify*: Chạy lệnh `pytest tests/test_cli.py` pass.

## 4. Failure Scenarios
| When (Sự kiện lỗi) | Then (Hành vi mong muốn) | Error Format / Code |
| :--- | :--- | :--- |
| Nhập sai định dạng tham số CLI | Hiển thị hướng dẫn định dạng đúng và thoát | In ra màn hình cảnh báo có màu đỏ (Rich Console) |
| File logs/agent.log không tồn tại | Tạo mới file log trống, không gây lỗi hệ thống CLI | Tự động tạo tệp `logs/agent.log` |

## 5. Rejection Criteria
- **DO NOT** in dữ liệu thô JSON của lịch học trực tiếp lên terminal mà không định dạng qua bảng của `rich`.
- **DO NOT** để chương trình rơi vào vòng lặp vô hạn khi gọi LLM không phản hồi (phải thiết lập timeout cho tiến trình gọi).

## 6. Cross-Phase Context
- **Assumes:** Agent và hệ thống logging từ `agents.py` (Phase 2).
- **Exports:** Giao diện CLI hoàn thiện đóng vai trò chứng minh tiêu chí "Agent CLI Skills" của Kaggle.

## 7. Acceptance Criteria
- Chạy `python cli.py` cho phép nhập liệu bằng lệnh CLI thành công, sinh ra lịch học hoàn thiện dạng bảng trong vòng dưới 5 giây.
- Trace logs suy luận của agent hiển thị rõ ràng trên màn hình CLI.

## 8. Traceability Matrix
- **Kaggle Concept 6 (Agent skills CLI):** Thực hiện tại Task 3.1, 3.2 và kiểm thử tại Task 3.3.

---
## Outcome Block

### What Was Planned
Thiết lập kế hoạch chi tiết cho Phase 3 tập trung xây dựng giao diện tương tác CLI chuyên nghiệp có tích hợp hiển thị Trace logs của Agent.

### Immediate Next Action
Chuẩn bị viết mã nguồn CLI cho `cli.py` sau khi hoàn thành Phase 2.

### How to Measure
| Metric | Measurement Command | Expected Result |
| :--- | :--- | :--- |
| File existence | `ls -la .rune/plan-ielts-coach-phase3.md` | Tệp kế hoạch Phase 3 tồn tại ở đúng đường dẫn. |
