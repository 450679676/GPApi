import requests
from requests import Response, PreparedRequest
import logging
logging.basicConfig(
    level=logging.DEBUG,


)#日志的格式

class LoggerSession(requests.Session):

    logger = logging.getLogger("request.session")



    def send(self, request: PreparedRequest, **kwargs) -> Response:
        """request请求 将接收到的参数 用send发送 现在需要重写send方法
        发生前记录request ， 响应后记录response
        """
        self.logger.info(f"发生请求>>>> 接口地址= {request.method}{request.url}")
        self.logger.debug(f"发生请求>>>> 请求头= {request.headers}")
        self.logger.debug(f"发生请求>>>> 请求正文= {request.body}")

        response = super(LoggerSession,self).send(request,**kwargs)#发送请求

        self.logger.info(f"接收响应>>>> 状态码= {response.status_code}")
        self.logger.debug(f"接收响应>>>> 响应头= {response.headers}")
        self.logger.debug(f"接收响应>>>> 请求正文= {response.text}")
        return response


