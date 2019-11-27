import re


def is_contain_zh(val):
    """ 判断参数是否包含中文 """
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zh_pattern.search(str(val))
    return True if match else False


def contain_zh(val):
    """ 为 webargs 校验提供的函数 """
    if is_contain_zh(val):
        from webargs import ValidationError
        raise ValidationError('不能包含中文')
