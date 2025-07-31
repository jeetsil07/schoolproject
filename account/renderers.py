from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {}
        # If errors exist, wrap them under 'errors'
        if 'ErrorDetail' in str(data):
            response['status'] = 'error'
            response['errors'] = data
        else:
            response['status'] = 'success'
            response['data'] = data
        return super().render(response, accepted_media_type, renderer_context)