import json
import logging
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings

logger = logging.getLogger(__name__)

VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def verify_recaptcha(request):
    """Verify a reCAPTCHA v2 ("I'm not a robot" checkbox) response.

    The widget posts its token as ``g-recaptcha-response``. Returns True when
    Google confirms the token is valid.
    """
    secret = getattr(settings, 'RECAPTCHA_SECRET_KEY', '')
    if not secret:
        logger.warning('RECAPTCHA_SECRET_KEY is not set; skipping reCAPTCHA verification.')
        return True

    token = request.POST.get('g-recaptcha-response', '')
    if not token:
        return False

    data = urlencode({
        'secret': secret,
        'response': token,
        'remoteip': _client_ip(request),
    }).encode()

    try:
        with urlopen(Request(VERIFY_URL, data=data), timeout=5) as response:
            result = json.loads(response.read().decode())
    except (URLError, ValueError, TimeoutError) as exc:
        logger.error('reCAPTCHA verification request failed: %s', exc)
        return False

    if not result.get('success'):
        logger.info('reCAPTCHA failed: %s', result.get('error-codes'))
        return False

    return True
