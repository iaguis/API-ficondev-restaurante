import re

REG_NICK = u"\w+$"
REG_EMAIL = u"[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}$"
REG_SHA1 = u"[a-f0-9]{40}$"
REG_TEXT = u"[a-zA-Z ]$"


def checkParam ( param, max_length, reg_exp ):
    if len(param) > max_length:
        return None

    if re.match(reg_exp, param, re.U):
        return param
    else: return None
