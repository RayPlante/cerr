"""Custom context processor
"""
from django.conf import settings


def domain_context_processor(request):
    return {
        "TEAM_NAME": settings.TEAM_NAME
        if hasattr(settings, "TEAM_NAME")
        else "black",
        "TEAM_EMAIL": settings.TEAM_EMAIL
        if hasattr(settings, "TEAM_EMAIL")
        else "",
        "EXPLORE_MENU_NAME": settings.EXPLORE_MENU_NAME
        if hasattr(settings, "EXPLORE_MENU_NAME")
        else "Search",
        "CURATE_MENU_NAME": settings.CURATE_MENU_NAME
        if hasattr(settings, "CURATE_MENU_NAME")
        else "Publish"
    }
