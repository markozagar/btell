"""Index - BTell front page."""
from typing import Dict, Any

from django import http, shortcuts

from btell_main.views import context as btell_context


def index(request: http.HttpRequest) -> http.HttpResponse:
    """Index view."""
    ctx: Dict[str, Any] = {}
    btell_context.context_add_user_info(request, ctx)
    return shortcuts.render(request, 'btell_main/index.html', ctx)

