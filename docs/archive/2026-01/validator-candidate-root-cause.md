# Validator Candidate Root Cause Review

- Source: tmp/docs/reports/validation_hints_candidates.json
- Evidence: tmp/docs/augment/<endpoint-id>/success.json, error.json, request_*_params.json

## 89e1ffde-0cda-4426-8277-72710c193cf2

- rule_type: output_required
- output: output1
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## ca2e71e1-5ef4-4489-b4c4-118e10588690

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 264533d3-00eb-4794-984a-fecb84350f39

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=100)
- sentinel fields: 2/43 (ratio=0.05)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## ebf1dc17-7b48-4192-841d-0ccb6ce3f016

- rule_type: output_required
- output: output1
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 3871dd9b-e9a5-471b-a0ce-d9ceb207ac5b

- rule_type: any_field_sentinel
- output: output1
- reason: sentinel_ratio=0.69
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=16)
- sentinel fields: 11/16 (ratio=0.69)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## e27baf2f-6ec0-4029-b4fd-4c873f340478

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## dd867a76-745d-4268-8ff8-b3e7f71e6e83

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 7bdbff93-1334-496f-a9b8-7da6032f7407

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 0c2760ca-7fc9-4f41-9abd-33b2f5ff3b3b

- rule_type: output_required
- output: output1
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 05a719af-aa3c-46c7-a670-55f2f11654c2

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## dfd2502e-0d5c-4999-8a24-84ff15a74696

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 72e63cb2-2ab1-41a0-8ab9-62cbeaa5eea0

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 3ed0247e-d717-43ed-85e9-51f952844687

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=21)
- sentinel fields: 3/11 (ratio=0.27)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 4a077f43-7053-47be-b811-8e35be4ea745

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 50775574-8832-4db8-aeb5-51a32c8250ed

- rule_type: any_field_sentinel
- output: output
- reason: sentinel_ratio=0.67
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=1)
- sentinel fields: 9/9 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## b664e9df-7ab6-4b89-89a0-5537ae380caf

- rule_type: output_required
- output: output1
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## fc52daa5-9919-4f80-b926-ee35ef298c54

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 7d1b2345-32f8-463b-9f41-8b4602387d52

- rule_type: any_field_sentinel
- output: output1
- reason: sentinel_ratio=0.64
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=7)
- sentinel fields: 7/7 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## f54caf9c-65db-42ee-aa7e-a337c5a41778

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## f77aedcb-b46f-4aa0-b062-f03b9a444405

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 43c17205-d112-4f9f-83f9-1704af8e4f79

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 26c5165d-1910-4467-aed9-7213524b7546

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## e7a0d02d-2aec-4358-8738-65c7c6da3b1b

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## c5933de1-4016-485a-a9ff-729818881d28

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## ca0f8e3e-9f99-4ebd-a81c-c5f8017c4d65

- rule_type: output_required
- output: output1
- reason: output_empty
- success rt_cd/msg1: 0 / 조회가 계속됩니다..다음버튼을 Click 하십시오.                                   
- error rt_cd/msg1: 0 / 조회할 내용이 없습니다                                                          
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 01fd59f1-e7f6-4192-8b02-d52e5dd7c8f3

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=100)
- sentinel fields: 8/8 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## fdb555c9-b958-48ad-a836-fd81f18ad73e

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## e0f9b38e-774a-441e-8dbd-27ab5f5ebb8b

- rule_type: output_required
- output: output
- reason: output_missing
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: missing (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## a4275fc3-384b-4b24-bf3a-38b72786b5ab

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## a27c026a-744f-4ddd-9d35-c35b285af74c

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 8c473311-ecfd-428f-9ec2-0b574d8592b9

- rule_type: all_fields_missing
- output: output1
- reason: missing_ratio=1.09
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=3)
- sentinel fields: 2/3 (ratio=0.67)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 31d46ebe-2a19-4467-9dfb-a2d21adb1e61

- rule_type: output_required
- output: output
- reason: output_missing
- success rt_cd/msg1: 0 / 
- error rt_cd/msg1: 0 / 
- error output state: missing (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## d5dc7247-6f82-4cd7-8133-afabd8f003f7

- rule_type: all_fields_missing
- output: output1
- reason: missing_ratio=1.00
- success rt_cd/msg1: 0 / 정상 조회되었습니다.
- error rt_cd/msg1: 0 / 정상 조회되었습니다.
- error output state: dict (len=1)
- sentinel fields: 1/1 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 3acd4025-6e95-46dc-a90d-b38215912d11

- rule_type: all_fields_sentinel
- output: output
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 조회가 계속됩니다..다음버튼을 Click 하십시오.                                   
- error rt_cd/msg1: 0 / 조회할 내용이 없습니다                                                          
- error output state: list (len=50)
- sentinel fields: 15/15 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 8702dab4-008d-4849-8f24-a91b57872a80

- rule_type: all_fields_missing
- output: output1
- reason: missing_ratio=1.09
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=3)
- sentinel fields: 2/3 (ratio=0.67)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 506cd6e9-97d9-4c4b-82bc-6a6c13586885

- rule_type: output_required
- output: output
- reason: output_missing
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: missing (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## cd2e4d9a-7e3d-44ff-9b68-36d971655c24

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=0.82
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=3)
- sentinel fields: 2/3 (ratio=0.67)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 1394ba1d-e17d-42c8-8e53-6bed5dce7588

- rule_type: output_required
- output: output
- reason: output_empty
- success rt_cd/msg1: 0 / 조회 되었습니다. (마지막 자료)                                                  
- error rt_cd/msg1: 0 / 조회할 자료가 없습니다                                                          
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## e8fcb701-6f36-4ba5-bbc7-84a577beec50

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=5)
- sentinel fields: 5/5 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 65db61e3-49a5-4a95-9cf3-61298c7b8461

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=5)
- sentinel fields: 5/5 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 967e60c7-f1eb-4f23-b893-71747556ad49

- rule_type: output_required
- output: output1
- reason: output_empty
- success rt_cd/msg1: 0 / 조회 되었습니다. (마지막 자료)                                                  
- error rt_cd/msg1: 0 / 조회할 내용이 없습니다                                                          
- error output state: list (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## ae084fcd-7a30-4a14-8483-91a7fc918d23

- rule_type: any_field_sentinel
- output: output1
- reason: sentinel_ratio=0.71
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=7)
- sentinel fields: 7/7 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 4360b745-0b9b-408e-8e0d-178138dbf864

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=3)
- sentinel fields: 3/3 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 9064a50c-0545-4b6c-8eb2-034f5214974b

- rule_type: output_required
- output: output
- reason: output_missing
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: missing (len=0)
- sentinel fields: 0/0 (ratio=0.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 2549b1c6-2c8c-4826-b632-74c0b68c24e9

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=3)
- sentinel fields: 3/3 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 05980ed5-8ab1-471a-975c-3e129841cbb8

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=5)
- sentinel fields: 5/5 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 3cb7e131-7e44-4f34-831f-e6720b4a299a

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=5)
- sentinel fields: 5/5 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 7d30b578-018d-4250-852a-7599211ff988

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=5)
- sentinel fields: 5/5 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## ec944971-3694-4692-8a17-761c2b549cd9

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=5)
- sentinel fields: 5/5 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## bac2f657-36b1-4538-aabc-0bee8ba77229

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=0.80
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=5)
- sentinel fields: 5/5 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.

## 40409c43-9bc7-447a-b09a-171d14b437f9

- rule_type: all_fields_sentinel
- output: output1
- reason: sentinel_ratio=1.00
- success rt_cd/msg1: 0 / 정상처리 되었습니다.
- error rt_cd/msg1: 0 / 정상처리 되었습니다.
- error output state: dict (len=3)
- sentinel fields: 3/3 (ratio=1.00)
- invalid params diff: unavailable
- docs/normalize issues: none
- classification: request_params_issue
- cause: Invalid params yield empty/sentinel/missing output with OK response.
- suggested_fix: Add validator for empty/sentinel/missing output; ensure invalid probe uses bad params.
