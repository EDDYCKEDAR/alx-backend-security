INSTALLED_APPS += [
    "ip_tracking",
    "ratelimit",
    "django_celery_beat",
]

MIDDLEWARE = [
    "ip_tracking.middleware.IPBlacklistMiddleware",
    "ip_tracking.middleware.IPLoggingMiddleware",
    # ...
]

CELERY_BEAT_SCHEDULE = {
    "detect_anomalies_hourly": {
        "task": "ip_tracking.tasks.detect_anomalies",
        "schedule": 3600.0,
    },
}
