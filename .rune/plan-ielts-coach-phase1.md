# Phase 1 Plan: Core Mathematical Engine & Optimization GA

## 1. Data Flow
```
Inputs (initial, target, days) ──► run_ga()
                                     │
    ┌────────────────────────────────┴────────────────────────┐
    ▼                                                         ▼
[Initialize Pop] ──► [Evaluate Fitness] ◄── [Learning Curve & Fatigue Calc]
                           │
                           ▼
                    [GA Operations] (Selection, Crossover, Mutation, Elitism)
                           │
                           ▼
                    [Best Schedule JSON]
```

## 2. Code Contracts (`ga_engine.py`)
```python
def calculate_learning_gain(p0: float, t: float, k: float, p_inf: float = 9.0) -> float: ...
def calculate_fatigue(schedule: list, alpha: float = 1.3, beta: float = 0.2) -> float: ...
def calculate_fitness(schedule: list, initial_bands: dict, target_bands: dict) -> float: ...
def run_ga(initial_bands: dict, target_bands: dict, total_days: int, pop_size: int = 300, generations: int = 100) -> dict: ...
```

## 3. Tasks
### Wave 1 (Engine Core)
- [x] **Task 1.1**: Tạo `ga_engine.py`. Viết các hàm tính toán `calculate_learning_gain`, `calculate_fatigue` và `calculate_fitness` theo công thức toán học trong `Specs-5565918f-f1cf-5191-bbb5-e43fc8cbf30d.md`.
  - *Verify*: Chạy thủ công với đầu vào đơn giản để kiểm tra tính chính xác.
- [x] **Task 1.2**: Tạo `tests/test_ga.py`. Viết các unit tests cơ bản sử dụng `pytest` cho các hàm toán học trên (kiểm tra các giá trị biên như $t=0$, $t=\infty$, band score $= 9.0$).
  - *Verify*: Chạy lệnh `pytest tests/test_ga.py` và tất cả các test pass.

### Wave 2 (GA Loop)
- [x] **Task 1.3**: Triển khai logic vòng lặp GA chính trong `ga_engine.py`: khởi tạo quần thể (300 cá thể), toán tử Selection (Tournament), Crossover (Single-point/Uniform), Mutation và Elitism (giữ lại 10% tốt nhất). Áp dụng các ràng buộc (block size >= 45 phút, max blocks/ngày = 4, min blocks/kỹ năng = 4/chu kỳ).
  - *depends_on*: Task 1.1
  - *Verify*: Gọi hàm `run_ga` trả về một lịch học 7 ngày hợp lệ.
- [x] **Task 1.4**: Bổ sung unit tests cho thuật toán GA trong `tests/test_ga.py`: kiểm tra xem lịch học đầu ra có vi phạm các ràng buộc (constraints) hay không, kiểm tra tính hội tụ của thuật toán.
  - *depends_on*: Task 1.2, Task 1.3
  - *Verify*: Chạy lệnh `pytest tests/test_ga.py` kiểm tra toàn bộ thuật toán.

## 4. Failure Scenarios
| When (Sự kiện lỗi) | Then (Hành vi mong muốn) | Error Format / Code |
| :--- | :--- | :--- |
| Band Score đầu vào $< 0.0$ hoặc $> 9.0$ | Trả về thông báo lỗi kiểm thực dữ liệu (ValueError) | `ValueError: Band score must be between 0.0 and 9.0` |
| Tổng số ngày học (total_days) $< 7$ | Ném ngoại lệ lỗi tham số | `ValueError: total_days must be at least 7` |
| GA không tìm thấy lịch hợp lệ sau 100 gen | Trả về lịch tốt nhất hiện tại kèm cảnh báo | `{"status": "warning", "message": "Constraints not fully met", "schedule": [...]}` |

## 5. Rejection Criteria
- **DO NOT** sử dụng thư viện GA ngoài (ví dụ: DEAP) để đảm bảo kiểm soát tốt các ràng buộc phức tạp của IELTS. Phải tự viết vòng lặp GA bằng Python/NumPy.
- **DO NOT** bỏ qua quy tắc làm tròn điểm IELTS (0.25, 0.5, 0.75, 1.0) khi tính Fitness.
- **DO NOT** để xảy ra lỗi chia cho 0 khi tính toán fatigue cho các ngày không có block học.

## 6. Cross-Phase Context
- **Assumes:** Dữ liệu đầu vào từ cấu hình toán học `Specs-5565918f-f1cf-5191-bbb5-e43fc8cbf30d.md`.
- **Exports:** Hàm `run_ga` trong `ga_engine.py` để các Phase sau sử dụng làm công cụ tối ưu lịch học.

## 7. Acceptance Criteria
- 100% unit tests trong `tests/test_ga.py` chạy thành công.
- Thuật toán GA tìm ra lịch tối ưu cho 10 trường hợp test định sẵn trong dưới 2 giây/lần chạy.
- Đầu ra của `run_ga` là JSON chứa lịch học 7 ngày và điểm dự đoán của từng kỹ năng đúng định dạng.

## 8. Traceability Matrix
- **Spec Section 2, 3 (Toán học GA):** Thực hiện tại Task 1.1, 1.3 và kiểm thử tại Task 1.2, 1.4.
- **Spec Section 8 (Quy tắc làm tròn):** Thực hiện tại Task 1.1 và kiểm thử tại Task 1.2.

---
## Outcome Block

### What Was Planned
Thiết lập kế hoạch chi tiết cho Phase 1 tập trung vào xây dựng bộ máy GA tối ưu hóa và hệ thống unit test tự động đi kèm.

### Immediate Next Action
Thực hiện viết mã nguồn thuật toán core GA trong `ga_engine.py` và các unit tests cơ bản trong `tests/test_ga.py`.

### How to Measure
| Metric | Measurement Command | Expected Result |
| :--- | :--- | :--- |
| File existence | `ls -la .rune/plan-ielts-coach-phase1.md` | Tệp kế hoạch Phase 1 tồn tại ở đúng đường dẫn. |
