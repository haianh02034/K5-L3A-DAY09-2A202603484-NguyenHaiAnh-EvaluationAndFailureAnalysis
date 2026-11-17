# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: single
- Commit hash: f9966e2
- Run id dẫn chứng: R-single-C-001-s11
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000 - 1.000 / 0.000000
- Cost per success (mô phỏng, VND): 39.53 VND
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 / 0

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Vì sao shape này

Nhóm chọn Shape B (`single`) vì đây là điểm cân bằng tối ưu giữa tính tự chủ của Agent và độ tin cậy vận hành. Single ReAct Agent tự chủ quyết định việc tra cứu tuần tự các công cụ đọc (`lookup_order`, `lookup_refund_history`, `compute_compensation`) trong phạm vi giới hạn nghiêm ngặt (tối đa 8 bước). Trên bộ dữ liệu 14 claim qua 5 seed (70 trial), Shape B đạt pass rate tuyệt đối 1.000, pass^5 đạt 1.000, phương sai hạt giống (seed variance) bằng 0.000000, và chi phí mô phỏng là 39.53 VND/success (rẻ hơn 30% so với Orchestrator 56.52 VND và rẻ hơn 20% so với Swarm 49.57 VND), đồng thời hoàn toàn loại bỏ được rủi ro dao động thất bại của Swarm (Swarm fail tại T02 seed 55).

## Có đáng đổi lấy multi-agent không

Không đáng đổi lấy Multi-agent (Swarm hay Orchestrator) cho tác vụ xử lý khiếu nại LogiX-VN này. Kết quả benchmark thực tế chứng minh quy trình claim là luồng nghiệp vụ phụ thuộc tuần tự (order $\rightarrow$ policy $\rightarrow$ compensation $\rightarrow$ refund). Việc đưa thêm các agent giao tiếp ngang hàng như Swarm làm chi phí tăng thêm 25.4% (từ 39.53 lên 49.57 VND), số bước tăng từ 1.93 lên 2.80, và làm giảm pass rate xuống 0.986 với phương sai 0.000816. Nhóm sẽ chỉ cân nhắc đổi sang Multi-agent khi bài toán xuất hiện các luồng điều tra song song độc lập trên quy mô lớn (ví dụ nhiều kho hàng cần xác minh cùng lúc) hoặc khi các domain chuyên môn hóa yêu cầu ranh giới ủy quyền phân cấp bảo mật chặt chẽ.

## Trace và bằng chứng

Trace của Shape B ghi nhận các sự kiện: `react_init` (chỉ `claim_id`, `order_id`), `quote`, `decision`, `error` (claim không tồn tại) và `crash`. Các trường cố ý **không ghi** bao gồm: `parent_secret`, `raw_headers`, số điện thoại khách hàng, địa chỉ giao hàng, tên hàng hóa chi tiết và ghi chú nội bộ. Các trường này được loại bỏ chủ động qua allowlist của tool adapter và trace contract. Nếu trace nằm ngoài vùng scanner tự động quét, đội an ninh chứng minh bằng tính bất biến của code (code invariants): hàm `get_claim_view` và `lookup_order` chỉ chọn các trường trong danh sách cho phép, và mọi luồng chuyển tiếp dữ liệu đều thông qua cấu trúc dữ liệu đã được sanitize cứng trong mã nguồn trước khi ghi ra đĩa.

## Giới hạn

MockLLM không phải model sản xuất thực tế; latency được ghi nhận là `unavailable`. Các số liệu chi phí dựa trên bảng giá mô phỏng trong `config/pricing.yaml`. Toàn bộ số liệu được trích xuất tự động từ `src/reports/benchmark.json` và `src/reports/crash.json`, nhóm không chỉnh sửa thủ công để đạt chỉ số.
