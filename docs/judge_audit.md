# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Đạt (κ=0.757 ≥ 0.6, P=0.857 ≥ 0.8, R=0.800 ≥ 0.7) | Dùng |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không đạt (Recall 0.300 < 0.7, κ=0.375 < 0.6) | Loại |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 | PASS | FAIL | Người đúng | Câu "Em đã hoàn tiền cho anh rồi nha, anh check giúp em" xưng hô thân mật tự phát, thiếu chuẩn mực CSKH LogiX. Cần bổ sung rule cấm xưng hô suồng sã vào rubric. |
| 2 | H-017 | PASS | FAIL | Người đúng | Câu "Dạ, bạn ơi LogiX đã hoàn 25.000đ cho đơn O-606 rồi nha" dùng từ "bạn ơi", "rồi nha" suồng sã. Rubric cần định nghĩa rõ từ cấm trong giao tiếp CSKH. |
| 3 | H-029 | PASS | FAIL | Người đúng | Câu "Dạ, vui lòng chờ. Hệ thống đang xử lý, không cần nhắn thêm" mang sắc thái cộc cằn, xua đuổi khách hàng. Cần bổ sung tiêu chí lịch sự vào rubric tone. |
| 4 | H-042 | FAIL | PASS | Người đúng | Câu "Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ" đúng mực, lịch sự, có dạ/ạ. Judge bị False Positive do nhầm lẫn câu ngắn gọn với thiếu tôn trọng. Cần thêm few-shot vào prompt judge. |
| 5 | HL-015 | PASS | FAIL | Người đúng | Khách khiếu nại hỏi rõ nguyên nhân đơn trễ, agent chỉ báo hoàn tiền mà lờ đi câu hỏi. Human đánh FAIL (unhelpful) là chính xác. Judge bỏ lọt (FN=21/30). |

## Kết luận
- **Tiêu chí bị loại:** `helpful` bị loại vì Recall quá thấp (0.300) và Cohen's Kappa chỉ đạt 0.375. Ma trận nhầm lẫn `{'tp': 9, 'fp': 0, 'fn': 21, 'tn': 70}` cho thấy Judge bỏ sót đến 21/30 trường hợp vi phạm thực tế (FN=21), không thể bảo vệ trải nghiệm người dùng nếu dùng làm gate release.
- **Tiêu chí được chọn:** `tone_ok` đạt chuẩn FLOORS với Precision 0.857, Recall 0.800, Cohen's Kappa 0.757.
- **Rủi ro còn lại:** Judge chỉ được kiểm trên dữ liệu replay đã công khai (public replay CSV); cần bộ nhãn người mới (held-out data) để kiểm tra chống overfitting định kỳ.
