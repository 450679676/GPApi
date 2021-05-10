## 熟悉项目

项目名称： TodoList
项目地址：Todo list - Vue.js
接口文档：三木的接口自动化测试练习v2 - Swagger UI
接口协议 ：Restful API （OpenAPI3.0）
接口地址1：http://127.0.0.1:8000/login/access_token
接口地址2：http://127.0.0.1:8000/login/sign_up
接口地址3: http://127.0.0.1:8000/todo
其他信息：
接口的BaseURL ： http://127.0.0.1:8000
 登录后才可用使用系统
部分接口会返回204 （例如 DELETE http://127.0.0.1:8000/todo/3）

## 搭建环境

创建Python项目，并编写自动化测试代码

## 选择工具：

HTTPClient ： requests
测试框架： pytest
框架插件：
创建项目：
创建PyCharm项目
创建虚拟环境
列出第三方包依赖 (pip管理 requirements.txt ）
pytest
requests

# 测试用例

测试登录接口

```python
from log import LoggerSession
import pytest
session = LoggerSession()
base_url = "https://api.tttt.one/rest-v2"
def test_login_sign_up():
    data = {
        "email":"enling@qq.com",
        "password":"enling@qq.com"
    }
    res = session.post(url=f"{base_url}/login/access_token",json=data)
    assert res.status_code == 200
```

## 全局性管理接口数据

1. 查看所有的接口信息
   1. 用途
   2. 地址、参数、鉴权
2. 接口的分组
   1. 相关性
   2. 依赖性
3.  结果依赖分析
4.  设计测试用例
   1. 正向用例
   2. 反向用例



### 封装请求参数

吧注册接口所用到的所有请求体 和断言 封装在一个容器中

```python
from collections import namedtuple
api_info_temp= namedtuple("api_info", ['method','url','body',"params",'code','res_body'])

api_info = dict(
    注册 = api_info_temp(
        method="POST",
        url="/login/sign_up",
        body={},
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
    )
    
)

#print(api_info["注册"].method)  打印下看看能不能获取
>>>POST
```

### 用例调用参数

```python
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
```

### 传递依赖参数

测试验证token的接口

需要从登录接口获取token后再进行验证  但是不要在测试登录接口的用例中获取  因为用例与用例之间是相互独立的  

可以在 请求验证token之前 但是发送一次登录请求 获取token  

```python
def test_token_user(self):
    """验证token
    请求登录接口 把token加入请求头中 
    """
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
```



