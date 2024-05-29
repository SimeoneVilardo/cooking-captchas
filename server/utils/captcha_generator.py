from abc import ABC
import abc
from io import BytesIO
import secrets
import string
from typing import TypedDict
from captcha.image import ImageCaptcha


class BaseSecureStringGenerator(ABC):
    @abc.abstractmethod
    def get_secure_string(self) -> str: ...


class SecureStringGenerator(BaseSecureStringGenerator):
    def __init__(self, alphabet: str = string.ascii_uppercase + string.digits, length: int = 6):
        if not alphabet:
            raise ValueError("Alphabet cannot be an empty string")
        if length < 1:
            raise ValueError("Length must be at least 1")
        self.alphabet = alphabet
        self.length = length

    def get_secure_string(self) -> str:
        secure_string: str = "".join(secrets.choice(self.alphabet) for _ in range(self.length))
        return secure_string


class FakeSecureStringGenerator(BaseSecureStringGenerator):
    def __init__(self, secure_string: str):
        self.secure_string = secure_string

    def get_secure_string(self) -> str:
        return self.secure_string


class CaptchaDict(TypedDict):
    image: BytesIO
    value: str


class CaptchaGenerator:
    def __init__(self, secure_string_generator: BaseSecureStringGenerator = SecureStringGenerator()):
        self.image_generator = ImageCaptcha()
        self.secure_string_generator = secure_string_generator

    def get_captcha(self) -> CaptchaDict:
        secure_string = self.secure_string_generator.get_secure_string()
        image = self.image_generator.generate(secure_string)
        return {"image": image, "value": secure_string}


def get_captcha_generator() -> CaptchaGenerator:
    return CaptchaGenerator()
