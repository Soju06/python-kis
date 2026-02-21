# IDX_CODE

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%97%85%EC%A2%85%EC%BD%94%EB%93%9C%EC%A0%95%EB%B3%B4.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%97%85%EC%A2%85%EC%BD%94%EB%93%9C%EC%A0%95%EB%B3%B4.h)
- 레코드 길이: `45`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `idx_div` | `char` | 1 | 시장구분값 ex) 00002(대형주)일 경우 맨 앞자리 0 |
| `idx_code` | `char` | 4 | 업종코드 ex) 00002(대형주)일 경우 맨 앞자리를 제외한 0002 |
| `idx_name` | `char` | 40 | 업종명 |
