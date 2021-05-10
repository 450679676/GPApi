from collections import namedtuple
import time
from log import LoggerSession
import pytest
session = LoggerSession()
base_url = "https://api.tttt.one/rest-v2"

api_info_temp= namedtuple("api_info", ['method','url','body',"params",'code','res_body'])

api_info = dict(
    注册 = api_info_temp(
        method="POST",
        url="/login/sign_up",
        body={
            "email": "senling@163.com",
            "password": "senling@163.com"
        },
        params = {},
        code =200,
        res_body = {
  "id": 2147483647,
  "email": "user@example.com",
  "create_datetime": "2021-05-09T07:20:06.054Z",
  "update_datetime": "2021-05-09T07:20:06.054Z"
}
    ),
    登录 = api_info_temp(
        method="POST",
        url = "/login/access_token",
        body = {
            "email":"senling@163.com",
            "password":"senling@163.com"
        },
        params = {},
        code = 200,
        res_body={
          "access_token": "string",
          "token_type": "string"
        }
    ),
    验证token = api_info_temp(
        method="POST",
        url="/login/test_token",
        body = {},
        params={},
        code =200,
        res_body={}

    )
)



class Test_Run_user:

    def test_login_sign_up(self):
        """
        测试注册
        """
        email = f"{time.time():.2f}@121"
        password = email

        api_name = "注册"
        res = session.request(api_info[api_name].method,
                           f"{base_url}{api_info[api_name].url}",
                           json={"email":email,"password":password})
        assert res.status_code == api_info[api_name].code
        assert res.json().keys() == api_info[api_name].res_body.keys()


    def test_login_user(self):
        """测试登录成功功能
         请求登录 判断账号是否存在 如果 存在就正常断言
         如果不存在就 先注册 然后再登录断言
         因为测试环境的数据 有可能 会被删除  所以需要判断一下
        """
        api_name = "登录"
        res = session.request(
            api_info[api_name].method,
            f"{base_url}{api_info[api_name].url}",
            json = api_info[api_name].body
        )
        if res.json().get("detail") != "Incorrect email or password":
            assert res.status_code == api_info[api_name].code
            assert res.json().keys() == api_info[api_name].res_body.keys()
        else:
            api_name = "注册"
            res = session.request(api_info[api_name].method,
                                  f"{base_url}{api_info[api_name].url}",
                                  json=api_info[api_name].body
                                  )
            assert res.status_code == api_info[api_name].code
            assert res.json().keys() == api_info[api_name].res_body.keys()

            res = session.request(
                api_info[api_name].method,
                f"{base_url}{api_info[api_name].url}",
                json=api_info[api_name].body
            )
            assert res.status_code == api_info[api_name].code
            assert res.json().keys() == api_info[api_name].res_body.keys()


    def test_token_user(self):
        """验证token"""
        api_name = "登录"

        res = session.request(
            api_info[api_name].method,
            f"{base_url}{api_info[api_name].url}",
            json=api_info[api_name].body
        )
        assert res.status_code == api_info[api_name].code
        token = res.json()["access_token"]
        headers = {
            "authorization": f"Bearer {token}"
        }
        session.headers.update(headers)


        api_name = "验证token"
        res = session.request(api_info[api_name].method,
                        f"{base_url}{api_info[api_name].url}"
                        )
        assert res.status_code == api_info[api_name].code



