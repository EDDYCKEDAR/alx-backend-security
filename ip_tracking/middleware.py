from django.utils.timezone import now
from django.http import HttpResponseForbidden
from django.core.cache import cache
from ipgeolocation import GeoIP
from .models import RequestLog, BlockedIP

geo = GeoIP()

class IPBlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked.")
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        return x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        ip = self.get_client_ip(request)

        # Cache geolocation for 24h
        cache_key = f"geo_{ip}"
        location = cache.get(cache_key)

        if not location:
            try:
                location = geo.city(ip)
                cache.set(cache_key, location, 60 * 60 * 24)
            except Exception:
                location = {}

        RequestLog.objects.create(
            ip_address=ip,
            timestamp=now(),
            path=request.path,
            country=location.get("country_name"),
            city=location.get("city")
        )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        return x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
