# ST_ELW_CODE

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28ELW%29.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28ELW%29.h)
- 레코드 길이: `270`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `mksc_shrn_iscd` | `char` | 9 | 단축코드 |
| `stnd_iscd` | `char` | 12 | 표준코드 |
| `hts_kor_isnm` | `char` | 40 | 한글종목명 |
| `elw_nvlt_optn_cls_code` | `char` | 1 | ELW권리형태<br>0 : 표준옵션<br>1 : 디지털옵현<br>2: 조기종료 옵션 |
| `elw_ko_barrier` | `char` | 13 | ELW조기종료발생기준가격 |
| `bskt_yn` | `char` | 1 | 바스켓 여부 (Y/N) |
| `unas_iscd1` | `char` | 9 | 기초자산코드 |
| `unas_iscd2` | `char` | 9 | 기초자산코드 |
| `unas_iscd3` | `char` | 9 | 기초자산코드 |
| `unas_iscd4` | `char` | 9 | 기초자산코드 |
| `unas_iscd5` | `char` | 9 | 기초자산코드 |
| `elw_pblc_istu_name` | `char` | 40 | 발행사 한글 종목명 |
| `elw_pblc_mrkt_prtt_no` | `char` | 5 | 발행사코드 |
| `acpr` | `char` | 9 | 행사가 |
| `stck_last_tr_month` | `char` | 8 | 최종거래일 |
| `rmnn_dynu` | `char` | 4 | 잔존 일수 |
| `rght_type_cls_code` | `char` | 1 | 권리 유형 구분 코드<br>'C':콜 'E':기타 'P':풋 |
| `paym_date` | `char` | 8 | 지급일 |
| `prdy_avls` | `char` | 9 | 전일시가총액(억) |
| `lstn_stcn` | `char` | 15 | 상장주수(천) |
| `mrkt_prtt_no1` | `char` | 5 | 시장 참가자 번호1 |
| `mrkt_prtt_no2` | `char` | 5 | 시장 참가자 번호2 |
| `mrkt_prtt_no3` | `char` | 5 | 시장 참가자 번호3 |
| `mrkt_prtt_no4` | `char` | 5 | 시장 참가자 번호4 |
| `mrkt_prtt_no5` | `char` | 5 | 시장 참가자 번호5 |
| `mrkt_prtt_no6` | `char` | 5 | 시장 참가자 번호6 |
| `mrkt_prtt_no7` | `char` | 5 | 시장 참가자 번호7 |
| `mrkt_prtt_no8` | `char` | 5 | 시장 참가자 번호8 |
| `mrkt_prtt_no9` | `char` | 5 | 시장 참가자 번호9 |
| `mrkt_prtt_no10` | `char` | 5 | 시장 참가자 번호10 |
