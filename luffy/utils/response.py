
from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, status=None, headers=None, **kwargs):
        data = {'code': 100, 'msg': '成功'}
        if kwargs:
            data.update(kwargs)

        super(APIResponse, self).__init__(data=data, status=status, headers=headers)
