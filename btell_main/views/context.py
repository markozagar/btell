# Functions which help build out common parts of the context.
from typing import Dict, Any
from django import http
from django.contrib.auth import models as auth_models

from btell_main.util import user_util
from btell_main import models

def context_add_user_info(request: http.HttpRequest, context: Dict[str, Any]):
    user = user_util.get_user_object(request)
    if user:
        profile = models.Profile.profile_from_user(user)
        full_name = f"{user.first_name} {user.last_name}".strip()
        context['btell_user'] = {
            'username': user.username.strip(),
            'full_name': full_name if full_name else None,
            'email': user.email,
            'profile': {
                'theme': profile.theme
            }
        }
    else:
        # Ensure that the user section of the context does not exist.
        if 'btell_user' in context:
            del context['btell_user']
