from re import compile
from rest_framework.status import is_client_error, is_success


class APIResponseMiddleware:
    ALLOWED_METHOD = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE',)
    API_URLS = [compile(r'^api/')]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        response = self.get_response(request)

        if not request.method in self.ALLOWED_METHOD or not any(m.match(path) for m in self.API_URLS):
            return response

        success = is_success(response.status_code)

        response_format = {
            'result': None,
            'success': success,
            'message': "OK" if success else None
        }

        if not hasattr(response, 'data') or getattr(response, 'data') is None:
            try:
                response.data = response_format
                response.content = response.render().rendered_content
            except AttributeError:
                pass
            return response

        data = response.data

        if is_client_error(response.status_code):
            response_format.update({
                'message': data.get('message')
            })
        elif success:
            response_format.update({
                'result': data
            })

        response.data = response_format
        response.content = response.render().rendered_content

        return response
