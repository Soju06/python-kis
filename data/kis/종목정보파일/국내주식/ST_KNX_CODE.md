# ST_KNX_CODE

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%BD%94%EB%84%A5%EC%8A%A4%29.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%BD%94%EB%84%A5%EC%8A%A4%29.h)
- 레코드 길이: `245`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `mksc_shrn_iscd` | `char` | 9 | 단축코드 |
| `stnd_iscd` | `char` | 12 | 표준코드 |
| `hts_kor_isnm` | `char` | 40 | 한글종목명 |
| `scrt_grp_cls_code` | `char` | 2 | 증권그룹구분코드<br>KN:코넥스 |
| `stck_sdpr` | `char` | 9 | 주식 기준가 |
| `frml_mrkt_deal_qty_unit` | `char` | 5 | 정규 시장 매매 수량 단위 |
| `ovtm_mrkt_deal_qty_unit` | `char` | 5 | 시간외 시장 매매 수량 단위 |
| `trht_yn` | `char` | 1 | 거래정지 여부 |
| `sltr_yn` | `char` | 1 | 정리매매 여부 |
| `mang_issu_yn` | `char` | 1 | 관리 종목 여부 |
| `mrkt_alrm_cls_code` | `char` | 2 | 시장 경고 구분 코드 (00:해당없음 01:투자주의<br>02:투자경고 03:투자위험 |
| `mrkt_alrm_risk_adnt_yn` | `char` | 1 | 시장 경고위험 예고 여부 |
| `insn_pbnt_yn` | `char` | 1 | 불성실 공시 여부 |
| `byps_lstn_yn` | `char` | 1 | 우회 상장 여부 |
| `flng_cls_code` | `char` | 2 | 락구분 코드<br>00:해당사항없음 01:권리락<br>02:배당락 03:분배락 04:권배락 05:중간배당락<br>06:권리중간배당락 99:기타<br>SW,SR,EW는 미해당(미해당의경우 SPACE) |
| `fcam_mod_cls_code` | `char` | 2 | 액면가 변경 구분 코드 (00:해당없음<br>01:액면분할 02:액면병합 99:기타) |
| `icic_cls_code` | `char` | 2 | 증자 구분 코드 (00:해당없음 01:유상증자<br>02:무상증자 03:유무상증자 99:기타) |
| `marg_rate` | `char` | 3 | 증거금 비율 |
| `crdt_able` | `char` | 1 | 신용주문 가능 여부 |
| `crdt_days` | `char` | 3 | 신용기간 |
| `prdy_vol` | `char` | 12 | 전일 거래량 |
| `stck_fcam` | `char` | 12 | 주식 액면가 |
| `stck_lstn_date` | `char` | 8 | 주식 상장 일자 |
| `lstn_stcn` | `char` | 15 | 상장 주수(천) |
| `cpfn` | `char` | 21 | 자본금 |
| `stac_month` | `char` | 2 | 결산 월 |
| `po_prc` | `char` | 7 | 공모 가격 |
| `prst_cls_code` | `char` | 1 | 우선주 구분 코드 (0:해당없음(보통주)<br>1:구형우선주 2:신형우선주) |
| `ssts_hot_yn` | `char` | 1 | 공매도과열종목여부 |
| `stange_runup_yn` | `char` | 1 | 이상급등종목여부 |
| `krx300_issu_yn` | `char` | 1 | KRX300 종목 여부 (Y/N) (실제적으로 필러) |
| `sale_account` | `char` | 9 | 매출액 |
| `bsop_prfi` | `char` | 9 | 영업이익 |
| `op_prfi` | `char` | 9 | 경상이익 |
| `thtr_ntin` | `char` | 5 | 단기순이익 |
| `roe` | `char` | 9 | ROE(자기자본이익률) |
| `base_date` | `char` | 8 | 기준년월 |
| `prdy_avls_scal` | `char` | 9 | 전일기준 시가총액 (억) |
| `co_crdt_limt_over_yn` | `char` | 1 | 회사신용한도초과여부 |
| `secu_lend_able_yn` | `char` | 1 | 담보대출가능여부 |
| `stln_able_yn` | `char` | 1 | 대주가능여부 |
