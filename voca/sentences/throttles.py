from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

    def allow_request(self, request, view):
        if request.user.is_superuser:
            return True
        return super().allow_request(request, view)


