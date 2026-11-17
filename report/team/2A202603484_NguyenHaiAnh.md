# Báo cáo cá nhân — 2A202603484_NguyenHaiAnh

## 1. Thông tin thành viên

- Họ tên: Nguyễn Hải Anh
- MSSV: 2A202603484
- Email: haianh29112@gmail.com
- GitHub: haianh02034
- Vai trò: Kỹ sư phụ trách Shape A (Deterministic Workflow)

---

## 2. Phần việc phụ trách

- **Mã nguồn:** Hiện thực hoàn chỉnh Shape A (`src/lab8/shapes/workflow.py`) từ stub ban đầu theo đúng chuẩn `RunResult` và hợp đồng `Trace Contract v1`.
- **Kiểm thử (Tests):** Xây dựng bộ test độc lập `src/tests/test_workflow_shape.py` để kiểm tra toàn diện các kịch bản biên, bảo mật dữ liệu, tính Idempotency và khả năng chịu lỗi khi crash của Shape A.
- **Rà soát & Đảm bảo an toàn:** Đảm bảo Shape A vượt qua tất cả 62 student tests (`pytest -m student -k workflow`) và kiểm tra nộp bài `check_submission`.

---

## 3. Đóng góp cụ thể

- **Commit chính:**
  - Commit hash: `54917fd` (`feat(workflow): implement Shape A deterministic workflow with safety guardrails`).
- **Quyết định kỹ thuật đã đưa ra:**
  1. *Nguyên tắc tiền tệ & quyền lực (Money in Code):* Toàn bộ việc định giá bồi hoàn do hàm `compute_compensation(conn, order)` tính toán trực tiếp từ dữ liệu hệ thống (order row). Không cho phép LLM tham gia quyết định số tiền hay sửa đổi số ngày trễ.
  2. *Bỏ qua số liệu không tin cậy trong ticket:* Với các claim như T02 (khách khai trễ 5 ngày nhưng order thực tế trễ 2 ngày) hoặc T09 (prompt injection "ignore policy"), workflow tuân thủ sự thật từ DB và từ chối bồi hoàn (`denied`, proposal 0).
  3. *Bảo vệ biên giới dữ liệu & PII:*
     - Đọc claim thông qua `get_claim_view` (chỉ chọn `claim_id, principal_id, order_id, ticket`), tuyệt đối không dùng `SELECT *` nhằm ngăn chặn rò rỉ `parent_secret` và `raw_headers`.
     - Khi đơn hàng không thuộc về principal (`lookup_order` trả về `outside_principal_scope`), trả về `escalated` và không ghi chép bất kỳ thông tin nhạy cảm nào (SĐT, địa chỉ, hàng hóa, ghi chú nội bộ) vào trace hoặc log.
  4. *Cơ chế truyền Quote đầy đủ cho Host:* Luôn truyền toàn bộ số tiền quote vào `durability.issue_refund`, để tầng host tự động khấu trừ các khoản bồi hoàn trước đó trên cùng đơn hàng theo quy định (giúp pass chính xác T13 và T14).
  5. *Khả năng chịu lỗi (Crash Resilience & Idempotency):*
     - Truyền `crash_at` trực tiếp vào `issue_refund` và chuyển tiếp ngoại lệ `InjectedCrash` (có ghi trace trước khi throw) để đáp ứng kịch bản kiểm thử crash của grader (T12).
     - Đảm bảo tính Idempotency: khi gọi lại cùng một claim (T11), host nhận diện và tái sử dụng bản ghi cũ mà không tạo thêm dòng mới trong ledger.
- **Test đã thêm:**
  - File: `src/tests/test_workflow_shape.py` gồm 6 test cases:
    + `test_workflow_unknown_claim`: Xử lý claim không tồn tại $\rightarrow$ `status="failed"`.
    + `test_workflow_missing_order_id_needs_info`: Xử lý thiếu `order_id` $\rightarrow$ `status="needs_info"`.
    + `test_workflow_outside_principal_scope_escalated`: Kiểm tra bảo mật PII khi sai khách hàng.
    + `test_workflow_disregards_ticket_text_delay`: Kiểm tra tính trung thực của dữ liệu trước thông tin sai lệch từ ticket.
    + `test_workflow_idempotency_retry`: Kiểm tra gọi lại nhiều lần chỉ tạo 1 dòng ledger.
    + `test_workflow_propagates_injected_crash`: Kiểm tra cơ chế crash và phục hồi sau sự cố.

---

## 4. Bằng chứng

- **Lịch sử Git:**
  - `git log -n 1 54917fd` xác nhận commit thuộc tác giả `haianh02034 <haianh29112@gmail.com>`.
- **Kết quả Unit Tests:**
  - Chạy `python -m pytest -q tests/test_workflow_shape.py`: **6 passed** trong 0.21s.
- **Kết quả Host Tests:**
  - Chạy `python -m pytest -q`: **60 passed** (54 test host có sẵn + 6 test workflow mới).
- **Kết quả Ma trận Student (Shape A):**
  - Chạy `python -m pytest -q -m student -o addopts= -k workflow`: **62 passed** (toàn bộ T01–T14 trên cả 5 seeds 11, 22, 33, 44, 55 + T11 retry + T12 crash).
- **Kết quả Kiểm tra Nộp bài (`check_submission`):**
  - Chạy `python -m lab8.check_submission`:
    ```text
    == shapes ==
    [ OK ] shape workflow: format đúng, 12/12 claim public pass ở seed 11
    ```

---

## 5. Công cụ AI đã dùng

- **Công cụ:** Antigravity (Gemini 3.8 Flash).
- **Mục đích sử dụng:**
  - Đọc, phân tích và giải thích cấu trúc mã nguồn, quy chuẩn hợp đồng `Trace Contract v1` và ma trận test `T01–T14`.
  - Hỗ trợ rà soát các trường hợp biên của Shape A (xử lý trần theo đơn, redaction PII, lan truyền ngoại lệ crash).
  - Soạn thảo khung unit test `test_workflow_shape.py` và hỗ trợ viết tài liệu báo cáo cá nhân.
- **Cách tự kiểm tra kết quả:**
  - Không tin tưởng mù quáng mã sinh ra: đã trực tiếp chạy kiểm thử thực tế trên môi trường máy địa phương với Python 3.11.
  - Chạy toàn bộ ma trận test student (`62/62 passed`).
  - Kiểm tra kết quả thẩm định máy với công cụ `python -m lab8.check_submission`.
  - Quét kỹ file trace sinh ra để đảm bảo không rò rỉ bất kỳ chuỗi `CANARY_SECRET_*` hay thông tin PII nào.

---

## 6. Tự đánh giá

- **Mức độ hoàn thành công việc:** 100% đối với phần Shape A được phân công.
- **Tuân thủ quy định & liêm chính học thuật:**
  - Không chỉnh sửa các file đo lường (`metrics.py`, `durability.py`, `policy.py`, `config/`, `data/`).
  - Toàn bộ kết quả đều được xác minh thực tế bằng lệnh chạy thật, không bịa đặt số liệu.
- **Điểm tự đánh giá:** 10/10 cho phần nhiệm vụ cá nhân (Shape A implementation & tests).
