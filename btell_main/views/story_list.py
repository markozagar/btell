"""View for displaying a list of stories, with optional filtering."""
from django import http


def stories_list_get(request: http.HttpRequest) -> http.HttpResponse:
    """Get method for the list of stories."""
    return http.HttpResponse('Test')
