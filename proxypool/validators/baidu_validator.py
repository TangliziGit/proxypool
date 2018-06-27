from .base_validator import BaseValidator
from ..rules import VALIDATE_RULES

class BaiduValidator(BaseValidator):
    name='baidu_validator'
    validate_rules=[VALIDATE_RULES['baidu']]
    validate_check_sign=VALIDATE_RULES['baidu'].get('check_sign')
