# ST_KSP_CODE

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%BD%94%EC%8A%A4%ED%94%BC%29.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%BD%94%EC%8A%A4%ED%94%BC%29.h)
- 레코드 길이: `288`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `mksc_shrn_iscd` | `char` | 9 | 단축코드 |
| `stnd_iscd` | `char` | 12 | 표준코드 |
| `hts_kor_isnm` | `char` | 40 | 한글종목명 |
| `scrt_grp_cls_code` | `char` | 2 | 증권그룹구분코드<br>ST:주권 MF:증권투자회사 RT:부동산투자회사<br>SC:선박투자회사 IF:사회간접자본투융자회사<br>DR:주식예탁증서 EW:ELW EF:ETF<br>SW:신주인수권증권 SR:신주인수권증서<br>BC:수익증권 FE:해외ETF FS:외국주권 |
| `avls_scal_cls_code` | `char` | 1 | 시가총액 규모 구분 코드 유가<br>(0:제외 1:대 2:중 3:소) |
| `bstp_larg_div_code` | `char` | 4 | 지수 업종 대분류 코드 |
| `bstp_medm_div_code` | `char` | 4 | 지수 업종 중분류 코드 |
| `bstp_smal_div_code` | `char` | 4 | 지수 업종 소분류 코드 |
| `mnin_cls_code_yn` | `char` | 1 | 제조업 구분 코드 (Y/N) |
| `low_current_yn` | `char` | 1 | 저유동성종목 여부 |
| `sprn_strr_nmix_issu_yn` | `char` | 1 | 지배 구조 지수 종목 여부 (Y/N) |
| `kospi200_apnt_cls_code` | `char` | 1 | KOSPI200 섹터업종(20110401 변경됨)<br>0:미분류 1:건설기계 2:조선운송 3:철강소재<br>4:에너지화학 5:정보통신 6:금융 7:필수소비재<br>8: 자유소비재 |
| `kospi100_issu_yn` | `char` | 1 | KOSPI100여부 |
| `kospi50_issu_yn` | `char` | 1 | KOSPI50 종목 여부 |
| `krx_issu_yn` | `char` | 1 | KRX 종목 여부 |
| `etp_prod_cls_code` | `char` | 1 | ETP 상품구분코드<br>0:해당없음 1:투자회사형 2:수익증권형<br>3:ETN 4:손실제한ETN |
| `elw_pblc_yn` | `char` | 1 | ELW 발행여부 (Y/N) |
| `krx100_issu_yn` | `char` | 1 | KRX100 종목 여부 (Y/N) |
| `krx_car_yn` | `char` | 1 | KRX 자동차 여부 |
| `krx_smcn_yn` | `char` | 1 | KRX 반도체 여부 |
| `krx_bio_yn` | `char` | 1 | KRX 바이오 여부 |
| `krx_bank_yn` | `char` | 1 | KRX 은행 여부 |
| `etpr_undt_objt_co_yn` | `char` | 1 | 기업인수목적회사여부 |
| `krx_enrg_chms_yn` | `char` | 1 | KRX 에너지 화학 여부 |
| `krx_stel_yn` | `char` | 1 | KRX 철강 여부 |
| `short_over_cls_code` | `char` | 1 | 단기과열종목구분코드 0:해당없음<br>1:지정예고 2:지정 3:지정연장(해제연기) |
| `krx_medi_cmnc_yn` | `char` | 1 | KRX 미디어 통신 여부 |
| `krx_cnst_yn` | `char` | 1 | KRX 건설 여부 |
| `krx_fnnc_svc_yn` | `char` | 1 | 삭제됨(20151218) |
| `krx_scrt_yn` | `char` | 1 | KRX 증권 구분 |
| `krx_ship_yn` | `char` | 1 | KRX 선박 구분 |
| `krx_insu_yn` | `char` | 1 | KRX섹터지수 보험여부 |
| `krx_trnp_yn` | `char` | 1 | KRX섹터지수 운송여부 |
| `sri_nmix_yn` | `char` | 1 | SRI 지수여부 (Y,N) |
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
| `flng_cls_code` | `char` | 2 | 락구분 코드 (00:해당사항없음 01:권리락<br>02:배당락 03:분배락 04:권배락 05:중간배당락<br>06:권리중간배당락 99:기타<br>S?W,SR,EW는 미해당(SPACE) |
| `fcam_mod_cls_code` | `char` | 2 | 액면가 변경 구분 코드 (00:해당없음<br>01:액면분할 02:액면병합 99:기타 |
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
| `prst_cls_code` | `char` | 1 | 우선주 구분 코드 (0:해당없음(보통주)<br>1:구형우선주 2:신형우선주 |
| `ssts_hot_yn` | `char` | 1 | 공매도과열종목여부 |
| `stange_runup_yn` | `char` | 1 | 이상급등종목여부 |
| `krx300_issu_yn` | `char` | 1 | KRX300 종목 여부 (Y/N) |
| `kospi_issu_yn` | `char` | 1 | KOSPI여부 |
| `sale_account` | `char` | 9 | 매출액 |
| `bsop_prfi` | `char` | 9 | 영업이익 |
| `op_prfi` | `char` | 9 | 경상이익 |
| `thtr_ntin` | `char` | 5 | 당기순이익 |
| `roe` | `char` | 9 | ROE(자기자본이익률) |
| `base_date` | `char` | 8 | 기준년월 |
| `prdy_avls_scal` | `char` | 9 | 전일기준 시가총액 (억) |
| `grp_code` | `char` | 3 | 그룹사 코드 |
| `co_crdt_limt_over_yn` | `char` | 1 | 회사신용한도초과여부 |
| `secu_lend_able_yn` | `char` | 1 | 담보대출가능여부 |
| `stln_able_yn` | `char` | 1 | 대주가능여부 |
