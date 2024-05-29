import pytest
from server.utils.captcha_generator import CaptchaGenerator, FakeSecureStringGenerator


@pytest.mark.parametrize(
    "value",
    [
        ("COOKING"),
        ("HELLO"),
        ("WORLD"),
    ],
)
def test_captcha_generator(value) -> None:
    generator = FakeSecureStringGenerator(value)
    captcha_generator = CaptchaGenerator(generator)
    captcha = captcha_generator.get_captcha()
    assert captcha["value"] == value
    assert captcha["image"].getvalue()[:8] == b"\x89PNG\r\n\x1a\n"
