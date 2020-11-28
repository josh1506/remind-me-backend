import json
from rest_framework import renderers


class UserRegisterRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if 'ErrorDetail' in str(data):
            return json.dumps({'errors': data})

        else:
            return json.dumps({'data': data})
