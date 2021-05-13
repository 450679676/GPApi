from log import *
import jsonpath
import pytest
base_url = "https://api.tttt.one/rest-v2"
session = LoggerSession()

# @pytest.fixture()
# def get_jaon(res,key):
#     """
#     :param res: 返回数据
#     :param key: 要提取字段的key
#     """
#     try:
#         if res is not None:
#             """如果返回数据不为空 """
#             text = res.json()
#             value = jsonpath.jsonpath(text,f'$..{key}')
#             # print(value)
#             if value:
#                 if len(value) == 1:
#                     return value[0]
#             else:
#                 return value
#     except Exception as e:
#         return e
#     else:
#         return None




@pytest.fixture(scope="session")
def user_token():
    """测试登录成功功能
           请求登录 判断账号是否存在 如果 存在就正常断言
           如果不存在就 先注册 然后再登录断言
           因为测试环境的数据 有可能会被删除  所以需要判断一下
          """

    res = session.request(
            "POST",
        f"{base_url}/login/access_token",
        json={
            "email":"senling@163.com",
            "password":"senling@163.com"}
    )
    if res.json().get("detail") != "Incorrect email or password":
        assert res.status_code == 200
        token = res.json()['access_token']
        return token
    else:
        res = session.request("POST",
                              f"{base_url}/login/sign_up",
                              json={
                                "email":"senling@163.com",
                                "password":"senling@163.com"
                              }
                              )
        assert res.status_code == 200
        res = session.request(
            "POST",
            f"{base_url}/login/access_token",
            json={
                "email": "senling@163.com",
                "password": "senling@163.com"}
        )
        token = res.json()['access_token']
        return token



@pytest.fixture(scope="session")
def user_session(user_token):
    """把 user_token获取到的鉴权信息 添加到请求头 返回
    使用过后pop 销毁
    """
    session.headers['Authorization'] = "Bearer "+user_token
    yield session
    session.headers.pop("Authorization")



