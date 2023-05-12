from django import http, shortcuts

def stories_list_get(request: http.HttpRequest) -> http.HttpResponse:
    return http.HttpResponse('Test')
