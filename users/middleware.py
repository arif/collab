from django.conf import settings
from django.utils import translation


class SetUserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = getattr(request.user, 'language', settings.LANGUAGE_CODE)
        if language:
            translation.activate(language)
            request.LANGUAGE_CODE = language

        response = self.get_response(request)

        return response
