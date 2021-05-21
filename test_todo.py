from collections import namedtuple
from re import A, M
import time
import pytest
base_url = "https://api.tttt.one/rest-v2"

api_info_temp= namedtuple("api_info", ['method','url','body',"params",'code','res_body'])

api_info = dict(
    任务列表 = api_info_temp(
        method='GET',
        url= "/todo",
        body= {},
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


@pytest.mark.parametrize(
     "data",[
      {
        "body":{},
        "result":{"code":200,"total":10}
      },
      {"body":{"page":1,"size":50},
        "result":{"code":200,"total":10}
      },
      {
        "body":{"page":0,"size":100},
        "result":{"code":200,"total":10}
      },
      {
        "body":{"page":"sggss","size":"fesdfsd"},
        "result":{"code":422,"msg":"value is not a valid integer"}
      }
      ]
)
def test_todo_list(user_session,data):
    api_name = "任务列表"
    res = user_session.request(
        api_info[api_name].method,
        f"{base_url}{api_info[api_name].url}",
        params=data['body']

    )
    assert res.status_code == data['result']['code']
    
    if res.json().get('total')  is not None: 
        assert res.json().get('total') == 10
    else:
        assert res.json()['detail'][0]['msg'] == data['result']['msg']                          
    

@pytest.mark.parametrize(
    'params',[{'result':{"code":200,"res_body":{
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
              {"page":1,"size":50,"result":{"code":200,"res_body":{
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
              {"page":"sfaf","size":"24rqwdf","result":{"code":422,"res_body":{
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
def test_todo_list_data(user_session,params):
    api_name = "任务列表"
    res = user_session.request(
        api_info[api_name].method,
        f"{base_url}{api_info[api_name].url}",
        params=params
    )
    assert res.status_code == params["result"]['code']
    assert res.json().keys() == params["result"]['res_body'].keys()
   

    

  
@pytest.mark.parametrize(
    "data",[
      {
        "body":{},
        "result":{"code":200,"title":"null"}
      },
      {"body":{"title":"senling","is_done":True},
        "result":{"code":200,"title":"senling"}
      },
      {
        "body":{"title":"senling"},
        "result":{"code":200,"title":"senling"}
      },
      {
        "body":{"is_done":False},
        "result":{"code":200,"title":"null"}
      }
      ]
)
def test_todo_establish(user_session,data):
  api_name = "创建任务"
  res = user_session.request(
      api_info[api_name].method,
      f"{base_url}{api_info[api_name].url}",
      json = data['body']
  )

  assert res.status_code == data["result"]['code']
  assert res.json()['title'] == data['result']['title']
  
