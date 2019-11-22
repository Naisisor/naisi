import re


def is_contain_zh(p):
    """ 判断参数是否包含中文 """
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zh_pattern.search(str(p))
    return True if match else False
