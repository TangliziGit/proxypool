from .base_validator import BaseValidator
from ..rules import VALIDATE_RULES

class ZhihuValidator(BaseValidator):
    name='zhihu_validator'
    validate_rules=[VALIDATE_RULES['zhihu']]
    validate_check_sign=VALIDATE_RULES['zhihu'].get('check_sign')
