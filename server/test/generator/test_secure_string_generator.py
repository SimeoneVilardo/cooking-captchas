import string
import pytest
from utils.captcha_generator import SecureStringGenerator


@pytest.mark.parametrize(
    "alphabet,length",
    [
        ("".join(string.ascii_uppercase) + "".join(string.digits), 6),
        ("".join(string.ascii_uppercase) + "".join(string.digits), 2),
        ("A", 6),
    ],
)
def test_secure_string_success(alphabet, length):
    generator = SecureStringGenerator(alphabet=alphabet, length=length)
    secure_string = generator.get_secure_string()
    assert len(secure_string) == length
    assert all(char in alphabet for char in secure_string)


@pytest.mark.parametrize(
    "alphabet,length",
    [
        ("", 6),
        ("ABC", -1),
    ],
)
def test_secure_string_error(alphabet, length):
    with pytest.raises(ValueError):
        generator = SecureStringGenerator(alphabet=alphabet, length=length)
