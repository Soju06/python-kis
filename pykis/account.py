
class KisAccount:
    '''한국투자증권 계좌 정보'''
    number: str
    '''종합계좌번호'''
    code: str
    '''계좌상품코드'''

    def __init__(self, account: str, code: str | None = None):
        '''한국투자증권 계좌 정보를 생성합니다.

        Args:
            account: 계좌번호 8자리 또는 XXXXXXXX-XX 또는 XXXXXXXXXX 형식의 문자 또는 숫자
            code: 계좌코드 2자리. 계좌번호 10자리를 사용할 경우 생략 가능.
        '''
        if '-' in account:
            l, r = account.split('-')
        else:
            l, r = account[:8], account[8:]
        if len(l) != 8 or (code == None and len(r) != 2):
            raise ValueError('계좌번호 형식이 올바르지 않습니다.')

        self.number = l
        if len(r) == 2:
            self.code = r
        else:
            if code == None:
                raise ValueError('계좌코드가 입력되지 않았습니다.')
            self.code = code
            
    def __str__(self):
        return f'{self.number:08d}-{self.code:02d}'

    def build_body(self, body: dict) -> dict:
        '''계좌 정보를 추가합니다.'''      
# CANO	종합계좌번호	String	Y	8	계좌번호 체계(8-2)의 앞 8자리
# ACNT_PRDT_CD	계좌상품코드	String	Y	2	계좌번호 체계(8-2)의 뒤 2자리
        body['CANO'] = self.number
        body['ACNT_PRDT_CD'] = self.code

        return body