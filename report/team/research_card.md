# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R1 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Google Research (2026), "Towards a Science of Scaling Agent Systems", arXiv/Google Research technical report, benchmark & ablation analysis |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Multi-agent chỉ mang lại lợi thế về hiệu năng khi bài toán có các nhánh thực thi song song độc lập; với các luồng phụ thuộc tuần tự, overhead giao tiếp và gọi model làm tăng chi phí 35-70% mà không cải thiện pass rate |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Áp dụng trên tập tác vụ xử lý khiếu nại tuần tự (LogiX-VN claims), MockLLM cố định theo seed, bảng giá token mô phỏng pricing.yaml |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Chuyển từ Workflow (A) sang Single ReAct (B) và Swarm (D) sẽ làm tăng cost per success khoảng 35% đến 70%, trong khi pass rate không tăng thêm (giữ 1.000 hoặc giảm ở Swarm do variance) |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Cố định 14 public claims, 5 seeds (11, 22, 33, 44, 55), bộ công cụ DB, bảng giá mô phỏng, evaluator. Biến duy nhất thay đổi: kiến trúc điều phối (Workflow vs Single ReAct vs Orchestrator vs Swarm) |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Đo bằng cost/success (VND), pass rate, seed variance. Điểm yếu dự kiến: Swarm giao tiếp ngang hàng làm đội chi phí và sinh variance (T02 seed 55) |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: `src/reports/benchmark.json (Run id mẫu: R-single-C-001-s11, R-workflow-C-001-s11)`
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: Đúng về hướng, vượt khoảng dự đoán ở hai shape. Workflow đạt 27.86 VND/success, Single ReAct là 39.53 VND (+42%, trong khoảng 35–70%), Swarm là 49.57 VND (+78%) và Orchestrator là 56.52 VND (+103%), hai shape sau vượt khoảng dự đoán. Pass rate của Workflow, Single và Orchestrator đều là 1.000 với variance 0.000000, nên chi phí tăng mà pass rate không tăng; Swarm giảm xuống 0.986 (pass^5 0.929) với variance 0.000816 do lỗi tin ticket ở T02 seed 55.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
