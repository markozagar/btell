"""View for displaying a list of stories, with optional filtering."""

from django import http
from django.db.models import query

from btell_main import models


# Dispatcher
def story_list(request: http.HttpRequest) -> http.HttpResponse:
    if request.method == 'GET':
        return story_list_get(request)
    elif request.method == 'POST':
        return story_list_post(request)
    else:
        return http.HttpResponseNotAllowed(['GET', 'POST'])


def story_list_get(request: http.HttpRequest) -> http.HttpResponse:
    """Get method for the list of stories."""
    # Steps:
    # 1. If logged in user, may have some preferences for tags set in profile (future improvements)
    # 2. Grab query string (filter), and construct a `QuerySet`
    filter = request.GET.get('filter')
    # 3. Paging or endless scroll? Implement paging first, add endless scroll function later via REST
    # 4. Fill context with stories (from QuerySet)
    # 5. HTML template
    return http.HttpResponse('Test - GET')


def story_list_post(request: http.HttpRequest) -> http.HttpResponse:
    return http.HttpResponse('Test - POST')