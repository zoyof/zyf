from rest_framework.throttling import SimpleRateThrottle


class SMSThrottle(SimpleRateThrottle):
    scope = 'sms'

    def get_cache_key(self, request, view):
        mobile = request.query_params.get('mobile')
        return mobile
