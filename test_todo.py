from collections import namedtuple
from operationyaml import *
from functools import total_ordering
from re import A
import re
from _pytest.config import main
from _pytest.mark import param
from attr import dataclass
from acquireJSON import get_jaon
import time
import pytest
base_url = "https://api.tttt.one/rest-v2"

api_info_temp = namedtuple(
    "api_info", ['method', 'url', 'body', "params", 'code', 'res_body'])

api_info = dict(
    任务列表=api_info_temp(
        method='GET',
        url="/todo",
        body={},
        params={
            "page": 0,
            "zise": 50
        },
        code=200,
        res_body={
            "items": [
                {
                    "id": 2147483647,
                    "title": "null",
                    "is_done": False,
                    "create_datetime": "2021-05-10T13:06:49.976Z",
                    "done_datetime": "2021-05-10T13:06:49.976Z"
                }
            ],
            "total": 0,
            "page": 0,
            "size": 0
        }
    ),
    创建任务=api_info_temp(
        method="POST",
        url="/todo",
        body={"title": None, "is_done": None},
        params={},
        code=200,
        res_body={
            "id": 2147483647,
            "title": "null",
            "is_done": False,
            "create_datetime": "2021-05-10T14:18:14.580Z",
            "done_datetime": "2021-05-10T14:18:14.580Z"
        }

    ),
    清空任务=api_info_temp(
        method="DELETE",
        url="/todo",
        body={},
        params={"all": all},
        code=204,
        res_body={
            "detail": [
                {
                    "loc": [
                        "string"
                    ],
                    "msg": "string",
                    "type": "string"
                }
            ]
        }
    ),
    任务详情=api_info_temp(
        method="GET",
        url="/todo/{todo_id}",
        body={},
        params={},
        code=200,
        res_body={
            "id": 2147483647,
            "title": "null",
            "is_done": False,
            "create_datetime": "2021-05-10T14:23:58.651Z",
            "done_datetime": "2021-05-10T14:23:58.652Z"
        }
    )


)


@pytest.fixture()
def user_todo_total(user_session):
    min_total = 10  # 设置最小值
    api_name = "任务列表"
    res = user_session.request(
        api_info[api_name].method, f"{base_url}{api_info[api_name].url}")
    assert res.status_code == api_info[api_name].code
   # 获取当前的数据 条数
    total = get_jaon(res, 'total')

    if total >= min_total:
        """如果满足最小值 就直接返回 否则创建任务直到满足最小值 然后再返回"""
        return total
    else:
        for i in range(min_total - total):
            api_name = "创建任务"
            res = user_session.request(
                api_info[api_name].method,
                f"{base_url}{api_info[api_name].url}",
                json={}
            )
            assert res.status_code == 200

        return min_total


@pytest.mark.parametrize(
    "data", [
        {
            "body": {},
            "result": {"code": 200, "total": 10}
        },
        {"body": {"page": 1, "size": 50},
            "result": {"code": 200, "total": 10}
         },
        {
            "body": {"page": 0, "size": 100},
            "result": {"code": 200, "total": 10}
        },
        {
            "body": {"page": "sggss", "size": "fesdfsd"},
            "result": {"code": 422, "msg": "value is not a valid integer"}
        }
    ]
)
def test_todo_list(user_session, data, user_todo_total):
    api_name = "任务列表"

    res = user_session.request(
        api_info[api_name].method,
        f"{base_url}{api_info[api_name].url}",
        params=data['body']

    )
    assert res.status_code == data['result']['code']

    if res.json().get('total') is not None:
        assert res.json().get('total') == user_todo_total
    else:
        assert res.json()['detail'][0]['msg'] == data['result']['msg']


@pytest.mark.parametrize(
    'params', [{'result': {"code": 200, "res_body": {
        "items": [
            {
                "id": 2147483647,
                "title": "null",
                "is_done": False,
                "create_datetime": "2021-05-17T13:46:10.332Z",
                "done_datetime": "2021-05-17T13:46:10.332Z"
            }
        ],
        "total": 10,
        "page": 0,
        "size": 0

    }
    }
    },
        {"page": 1, "size": 50, "result": {"code": 200, "res_body": {
            "items": [
                {
                    "id": 2147483647,
                    "title": "null",
                    "is_done": False,
                    "create_datetime": "2021-05-17T13:46:10.332Z",
                    "done_datetime": "2021-05-17T13:46:10.332Z"
                }
            ],
            "total": 10,
            "page": 0,
            "size": 0

        }
        }},
        {"page": "sfaf", "size": "24rqwdf", "result": {"code": 422, "res_body": {
            "detail": [
                {
                    "loc": [
                        "string"
                    ],
                    "msg": "string",
                    "type": "string"
                }
            ]
        }
        }
    }
    ]
)
def test_todo_list_data(user_session, params, read_url):
    api_name = "任务列表"
    res = user_session.request(
        api_info[api_name].method,
        f"{read_url}{api_info[api_name].url}",
        params=params
    )
    assert res.status_code == params["result"]['code']
    assert res.json().keys() == params["result"]['res_body'].keys()


@pytest.mark.parametrize(
    "data", [
        {
            "body": {},
            "result": {"code": 200, "title": "null"}
        },
        {"body": {"title": "senling", "is_done": True},
            "result": {"code": 200, "title": "senling"}
         },
        {
            "body": {"title": "senling"},
            "result": {"code": 200, "title": "senling"}
        },
        {
            "body": {"is_done": False},
            "result": {"code": 200, "title": "null"}
        }
    ]
)
def test_todo_establish(user_session, data, read_url):
    api_name = "创建任务"
    res = user_session.request(
        api_info[api_name].method,
        f"{read_url}{api_info[api_name].url}",
        json=data['body']
    )

    assert res.status_code == data["result"]['code']
    assert res.json()['title'] == data['result']['title']


@pytest.fixture()
def New_todo(user_session, read_url):
    api_name = "任务列表"

    res = user_session.request(
        api_info[api_name].method,
        f"{read_url}{api_info[api_name].url}"
    )
    assert res.status_code == 200
    id = get_jaon(res, 'id')
    if id is not None:

        return id[0]
    else:
        api_name = "创建任务"
        res = user_session.request(
            api_info[api_name].method,
            f"{read_url}{api_info[api_name].url}",
            json={}
        )
        assert res.status_code == 200
        return get_jaon(res, 'id')


@pytest.mark.parametrize(
    "data", [
        {
            "body": {"id": New_todo},
            "result": {"code": 200}
        },
    ]
)
def test_get_todo(user_session, data):
    api_name = "任务详情"
    res = user_session.request(
        api_info[api_name].method,
        #   https://api.tttt.one/rest-v2/todo{todo_id}.format(todo_id=1067)
        f"{read_url}{api_info[api_name].url}".format(
            todo_id=data['body']['id'])
    )
    assert res.status_code == data['result']['code']


@pytest.fixture()
def new_todo():
    page = 11
    size = 500
    data = (page, size)
    return data


list1 = []


@pytest.mark.parametrize(
    "data", read_yaml()
)
def test_todo_list(user_session, data, new_todo):
    datas = data['body']

    if type(datas) is dict:
        if datas['page'] is None:
            data['body']['page'] = new_todo[0]
        if datas['size'] is None:
            data['body']['size'] = new_todo[1]
        print(data)
