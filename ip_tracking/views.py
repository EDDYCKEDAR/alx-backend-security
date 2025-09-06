from django.http import JsonResponse
from ratelimit.decorators import ratelimit

@ratelimit(key="ip", rate="10/m", method="POST", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def login_view(request):
    if request.method == "POST":
        return JsonResponse({"message": "Login attempt"})
    return JsonResponse({"message": "Only POST allowed"})
