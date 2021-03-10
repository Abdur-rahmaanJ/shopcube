import pytest
from shopyo.api import validators


class TestValidators:
    """Tests validator methods"""

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("google", False),
            ("www.google.com", True), ("https://www.google.com", True),
            ("localhost:3000", True), ("192.168.0.250", True),
            ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", True)
        ]
    )
    def test_is_valid_url(self, url, expected):
        result = validators.is_valid_url(url)
        assert result == expected
