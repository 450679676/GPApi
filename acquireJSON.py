import jsonpath

def get_jaon(res,key):
    """
    :param res: 返回数据
    :param key: 要提取字段的key
    """
    try:
        if res is not None:
            """如果返回数据不为空 """
            text = res.json()
            value = jsonpath.jsonpath(text,f'$..{key}')
            # print(value)
            if value:
                if len(value) == 1:
                    return value[0]
            else:
                return value
    except Exception as e:
        return e
    else:
        return None


