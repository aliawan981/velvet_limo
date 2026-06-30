import json
import time
from urllib import error, parse, request

from django.conf import settings


class MicrosoftGraphMailError(RuntimeError):
    pass


class MicrosoftGraphMailer:
    def __init__(self):
        self.tenant_id = getattr(settings, 'MICROSOFT_GRAPH_TENANT_ID', '')
        self.client_id = getattr(settings, 'MICROSOFT_GRAPH_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'MICROSOFT_GRAPH_CLIENT_SECRET', '')
        self.sender = getattr(settings, 'MICROSOFT_GRAPH_SENDER', '')
        self._access_token = None
        self._token_expires_at = 0

    def _require_configuration(self):
        missing = [
            name
            for name, value in (
                ('MICROSOFT_GRAPH_TENANT_ID', self.tenant_id),
                ('MICROSOFT_GRAPH_CLIENT_ID', self.client_id),
                ('MICROSOFT_GRAPH_CLIENT_SECRET', self.client_secret),
                ('MICROSOFT_GRAPH_SENDER', self.sender),
            )
            if not value
        ]
        if missing:
            raise MicrosoftGraphMailError(
                'Microsoft Graph email is not configured. Missing: ' + ', '.join(missing)
            )

    def _request_json(self, url, data, headers=None):
        payload = None if data is None else json.dumps(data).encode('utf-8')
        request_headers = {'Content-Type': 'application/json'}
        if headers:
            request_headers.update(headers)

        req = request.Request(url, data=payload, headers=request_headers, method='POST')
        try:
            with request.urlopen(req, timeout=30) as response:
                content = response.read().decode('utf-8')
                return json.loads(content) if content else {}
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='ignore')
            if exc.code == 401 and '/sendMail' in url:
                raise MicrosoftGraphMailError(
                    'Microsoft Graph denied sendMail. Verify the app registration has Application permission Mail.Send, '
                    'admin consent was granted, and MICROSOFT_GRAPH_SENDER is a real mailbox/UPN that can send mail.'
                ) from exc
            raise MicrosoftGraphMailError(f'Graph request failed with {exc.code}: {detail}') from exc
        except error.URLError as exc:
            raise MicrosoftGraphMailError(f'Graph request failed: {exc.reason}') from exc

    def _get_access_token(self):
        self._require_configuration()
        now = time.time()
        if self._access_token and now < self._token_expires_at - 60:
            return self._access_token

        token_url = f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token'
        form_data = parse.urlencode(
            {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials',
                'scope': 'https://graph.microsoft.com/.default',
            }
        ).encode('utf-8')

        req = request.Request(
            token_url,
            data=form_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            method='POST',
        )

        try:
            with request.urlopen(req, timeout=30) as response:
                token_data = json.loads(response.read().decode('utf-8'))
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='ignore')
            if exc.code == 401 and 'AADSTS7000215' in detail:
                raise MicrosoftGraphMailError(
                    'Microsoft Graph rejected the client secret. Set MICROSOFT_GRAPH_CLIENT_SECRET to the secret value, not the secret ID, in .env.'
                ) from exc
            raise MicrosoftGraphMailError(f'Unable to get Graph token: {exc.code}: {detail}') from exc
        except error.URLError as exc:
            raise MicrosoftGraphMailError(f'Unable to get Graph token: {exc.reason}') from exc

        self._access_token = token_data.get('access_token', '')
        expires_in = int(token_data.get('expires_in', 0) or 0)
        self._token_expires_at = now + expires_in if expires_in else now + 3000

        if not self._access_token:
            raise MicrosoftGraphMailError('Microsoft Graph did not return an access token.')

        return self._access_token

    def send_mail(self, subject, body, recipients, sender=None):
        to_recipients = [recipient for recipient in recipients if recipient]
        if not to_recipients:
            return

        message_sender = sender or self.sender
        token = self._get_access_token()
        payload = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': 'Text',
                    'content': body,
                },
                'toRecipients': [{'emailAddress': {'address': recipient}} for recipient in to_recipients],
            },
            'saveToSentItems': False,
        }

        self._request_json(
            f'https://graph.microsoft.com/v1.0/users/{parse.quote(message_sender, safe="")}/sendMail',
            payload,
            headers={'Authorization': f'Bearer {token}'},
        )


_graph_mailer = MicrosoftGraphMailer()


def send_graph_mail(subject, body, recipients, sender=None):
    _graph_mailer.send_mail(subject=subject, body=body, recipients=recipients, sender=sender)