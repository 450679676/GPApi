from collections import namedtuple
import time
from log import LoggerSession
import pytest
session = LoggerSession()
base_url = "https://api.tttt.one/rest-v2"

api_info_temp= namedtuple("api_info", ['method','url','body',"params",'code','res_body'])

api_info = dict(
    任务列表 = api_info_temp(
        method='GET',
        url= "/todo",
        body= {},
        params={
            "page": 10,
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
    创建任务 = api_info_temp(
        method="POST",
        url="/todo",
        body={"title":None,"is_done":None},
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
    清空任务 = api_info_temp(
        method="DELETE",
        url="/todo",
        body={"alli":all},
        params={},
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
    任务详情 = api_info_temp(
        method="GET",
        url ="/todo/{todo_id}",
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