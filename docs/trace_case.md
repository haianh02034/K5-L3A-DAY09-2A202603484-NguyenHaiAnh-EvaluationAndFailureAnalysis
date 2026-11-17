# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi nhóm 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, run ID: `E-seeded_regression-20261117-ea77` |
| Triệu chứng | Grader `pass_rate` và `refund_amount_correct` FAIL (status resolved != denied, refund 20000 != 0). Reply nói "Dạ, LogiX đã hoàn 20.000đ cho đơn O-202." |
| Bước sai đầu tiên | Event 3: `model_override` `{"delay_days": 5}` |
| Vì sao là bước *đầu tiên* | Event 1 (`handoff`) và Event 2 (`investigator`) thực hiện hoàn toàn đúng, tra cứu DB ra thực tế trễ 2 ngày (`delay_days: 2`). Đến Event 3, agent mới bắt đầu sai khi lấy số ngày trễ 5 ngày do khách tự khai trong ticket đè lên dữ liệu DB. |
| Failure mode | FM-03 (ticket_trust — tin ticket hơn DB) |
| Đối chứng | Trên shape `fixed` (`C-002@11`): Không có event `model_override`. Event 3 sinh `quote` trực tiếp từ DB với `amount_vnd: 0`, từ chối bồi hoàn (`status: denied`, `refund_vnd: 0`), khớp 100% với nhãn. |
| Regression test | `DbFactKept` kiểm tra không có event `model_override` trong trace; test `test_override_event_breaks_db_fact` trong `test_lab9_graders.py`. Đã xác nhận FAIL trên `seeded_regression` và PASS trên `fixed`. |
| Chưa chắc chắn | Chưa kiểm chứng được hành vi của model khi ticket chứa prompt injection phức tạp nhiều tầng (multi-turn jailbreak) thay vì chỉ khai gian số ngày trễ. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
