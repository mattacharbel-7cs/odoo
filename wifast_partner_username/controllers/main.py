# -*- coding: utf-8 -*-
import hmac
import json
import logging

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)

# Route prefix and API-key parameter are kept as-is so existing external
# integrations (Postman, WiFast/Fast2Serv) keep working unchanged.
API_KEY_PARAM = 'wifast_customer_username.api_key'

# The username lives on the client's Studio field.
USERNAME_FIELD = 'x_studio_username'


class WifiCustomerUsernameController(http.Controller):

    def _json(self, data, status=200):
        return request.make_response(
            json.dumps(data, default=str),
            headers=[('Content-Type', 'application/json')],
            status=status,
        )

    def _error(self, error, status=400):
        return self._json({'success': False, 'error': error}, status=status)

    def _parse_json_body(self):
        try:
            raw = request.httprequest.data.decode('utf-8')
            return (json.loads(raw) if raw else {}), None
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None, 'invalid_json'

    def _get_request_api_key(self):
        header_key = request.httprequest.headers.get('X-API-Key', '')
        if header_key:
            return header_key

        auth_header = request.httprequest.headers.get('Authorization', '')
        prefix = 'Bearer '
        if auth_header.lower().startswith(prefix.lower()):
            return auth_header[len(prefix):].strip()
        return ''

    def _is_authorized(self):
        configured = request.env['ir.config_parameter'].sudo().get_param(
            API_KEY_PARAM, default=''
        )
        provided = self._get_request_api_key()
        if not configured or not provided:
            return False
        try:
            return hmac.compare_digest(
                str(configured).encode('utf-8'),
                str(provided).encode('utf-8'),
            )
        except Exception:
            return False

    def _contact_payload(self, partner):
        data = {
            'id': partner.id,
            'name': partner.name,
            'username': partner[USERNAME_FIELD],
            'company_id': partner.company_id.id or False,
        }
        for field_name in ('email', 'phone', 'mobile'):
            if field_name in partner._fields:
                data[field_name] = partner[field_name]
        return data

    def _compact_contact_payload(self, partner):
        return {
            'id': partner.id,
            'name': partner.name,
            'username': partner[USERNAME_FIELD],
        }

    def _find_partner(self, values):
        Partner = request.env['res.partner'].sudo().with_context(active_test=False)

        partner_id = values.get('partner_id')
        if partner_id:
            try:
                if isinstance(partner_id, bool):
                    return Partner.browse(), None
                partner_id = int(partner_id)
            except (TypeError, ValueError):
                return Partner.browse(), 'invalid_partner_id'
            return Partner.browse(partner_id).exists(), None

        username = (values.get('username') or '').strip()
        if username:
            return self._search_single(Partner, [(USERNAME_FIELD, '=', username)])

        email = (values.get('email') or '').strip()
        if email:
            return self._search_single(Partner, [('email', '=ilike', email)])

        phone = (values.get('phone') or '').strip()
        if phone:
            phone_domain = []
            if 'phone' in Partner._fields:
                phone_domain.append(('phone', '=', phone))
            if 'mobile' in Partner._fields:
                phone_domain.append(('mobile', '=', phone))
            if not phone_domain:
                return Partner.browse(), 'phone_lookup_unavailable'
            return self._search_single(Partner, self._or_domain(phone_domain))

        return Partner.browse(), 'missing_identifier'

    def _or_domain(self, expressions):
        if len(expressions) == 1:
            return expressions
        return ['|'] * (len(expressions) - 1) + expressions

    def _search_single(self, Partner, domain):
        partners = Partner.search(domain, limit=2)
        if len(partners) > 1:
            return Partner.browse(), 'multiple_contacts_found'
        return partners, None

    @http.route(
        '/wifast_customer_username/api/contact',
        type='http',
        auth='none',
        methods=['GET'],
        csrf=False,
    )
    def get_contact(self, **kwargs):
        if not self._is_authorized():
            return self._error('unauthorized', status=401)

        partner, error = self._find_partner(kwargs)
        if error:
            return self._error(error)
        if not partner:
            return self._error('contact_not_found', status=404)

        return self._json({
            'success': True,
            'contact': self._contact_payload(partner),
        })

    @http.route(
        '/wifast_customer_username/api/contact/username',
        type='http',
        auth='none',
        methods=['POST'],
        csrf=False,
        readonly=False,
    )
    def update_username(self, **kwargs):
        if not self._is_authorized():
            return self._error('unauthorized', status=401)

        payload, error = self._parse_json_body()
        if error:
            return self._error(error)
        if not isinstance(payload, dict):
            return self._error('invalid_json')

        username = (payload.get('username') or '').strip()
        if not username:
            return self._error('missing_username')

        lookup = {
            'partner_id': payload.get('partner_id'),
            'email': payload.get('email'),
            'phone': payload.get('phone'),
        }
        partner, error = self._find_partner(lookup)
        if error:
            return self._error(error)
        if not partner:
            return self._error('contact_not_found', status=404)

        try:
            partner.write({USERNAME_FIELD: username})
        except ValidationError:
            return self._error('username_already_exists')
        except Exception:
            _logger.exception("Failed to update username for partner %s", partner.id)
            return self._error('update_failed', status=500)

        return self._json({
            'success': True,
            'contact': self._compact_contact_payload(partner),
        })
