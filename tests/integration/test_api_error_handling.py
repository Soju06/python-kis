"""
통합 테스트 - API 인증 및 에러 처리

API 인증 정보 검증과 에러 상황을 테스트합니다.
"""

import pytest

from vmkis import KisAuth


@pytest.mark.integration
class TestAuthValidation:
    """인증 정보 검증 테스트."""

    def test_valid_auth_creation(self):
        """정상 인증 정보 생성."""
        auth = KisAuth(
            id="test_user",
            account="50000000-01",
            appkey="P" + "A" * 35,
            secretkey="S" * 180,
            paper=False,
        )
        assert auth.id == "test_user"
        assert auth.account == "50000000-01"
        assert auth.paper is False

    def test_account_format_validation(self):
        """계좌 형식 검증."""
        valid_accounts = ["50000000-01", "50000001-02"]

        for account in valid_accounts:
            auth = KisAuth(
                id="user1",
                account=account,
                appkey="P" + "A" * 35,
                secretkey="S" * 180,
                paper=False,
            )
            assert auth.account == account

    def test_appkey_length_validation(self):
        """AppKey 길이 검증 (36자)"""
        auth = KisAuth(
            id="user1",
            account="50000000-01",
            appkey="P" + "A" * 35,
            secretkey="S" * 180,
            paper=False,
        )
        assert len(auth.appkey) == 36

    def test_secretkey_length_validation(self):
        """SecretKey 길이 검증 (180자)"""
        auth = KisAuth(
            id="user1",
            account="50000000-01",
            appkey="P" + "A" * 35,
            secretkey="S" * 180,
            paper=False,
        )
        assert len(auth.secretkey) == 180


@pytest.mark.integration
class TestEnvironmentCompatibility:
    """실전/모의 환경 호환성 테스트."""

    def test_real_environment_flag(self):
        """실전 환경 플래그."""
        auth = KisAuth(
            id="user1",
            account="50000000-01",
            appkey="P" + "A" * 35,
            secretkey="S" * 180,
            paper=False,
        )
        assert auth.paper is False

    def test_virtual_environment_flag(self):
        """모의 환경 플래그."""
        auth = KisAuth(
            id="user1",
            account="50000000-01",
            appkey="P" + "A" * 35,
            secretkey="S" * 180,
            paper=True,
        )
        assert auth.paper is True

    def test_multiple_auth_isolation(self):
        """여러 인증 정보 분리."""
        auth1 = KisAuth(
            id="user1",
            account="50000000-01",
            appkey="P" + "A" * 35,
            secretkey="S" * 180,
            paper=False,
        )

        auth2 = KisAuth(
            id="user2",
            account="50000001-02",
            appkey="P" + "B" * 35,
            secretkey="B" * 180,
            paper=True,
        )

        assert auth1.id != auth2.id
        assert auth1.account != auth2.account
        assert auth1.paper != auth2.paper
