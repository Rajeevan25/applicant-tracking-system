

from collections.abc import Callable
from functools import wraps
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def redirect_authenticated_user(view_func: Callable) -> Callable:
    """
    Decorator to redirect authenticated users away from certain views.
    If the user is authenticated, they will be redirected to the home page.
    Otherwise, the original view function will be executed.
    """
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('home')  # Redirect to home page or any other appropriate page
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view