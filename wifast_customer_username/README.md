# WiFast Customer Username

Adds a WiFi/customer account username to Odoo contacts and exposes secured
endpoints for a future WiFi or billing system integration.

## Contact Field

The module adds `wifi_username` on `res.partner` with the label **Username**.
It appears on the contact form under **Sales & Purchase**, in the Misc section,
and is searchable from the Contacts list search bar.

Non-empty usernames must be unique within the same Odoo company.

## API Key

Set the API key from **Settings > General Settings > WiFast Customer Username**.
The value is stored in:

```text
wifast_customer_username.api_key
```

API requests can authenticate with either header:

```text
X-API-Key: your_api_key
Authorization: Bearer your_api_key
```

## GET Contact

```text
GET /wifast_customer_username/api/contact
```

Supported query parameters:

- `partner_id`
- `username`
- `email`
- `phone`

Example Postman setup:

- Method: `GET`
- URL: `https://example.odoo.com/wifast_customer_username/api/contact?username=john_wifi_123`
- Header: `X-API-Key: your_api_key`

Example curl:

```bash
curl -X GET "https://example.odoo.com/wifast_customer_username/api/contact?username=john_wifi_123" \
  -H "X-API-Key: your_api_key"
```

Example response:

```json
{
  "success": true,
  "contact": {
    "id": 45,
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "+971...",
    "mobile": "+971...",
    "username": "john_wifi_123",
    "company_id": 1
  }
}
```

## POST Username Update

```text
POST /wifast_customer_username/api/contact/username
```

The endpoint updates only the `wifi_username` field on an existing contact. It
does not create contacts.

Example Postman setup:

- Method: `POST`
- URL: `https://example.odoo.com/wifast_customer_username/api/contact/username`
- Header: `X-API-Key: your_api_key`
- Header: `Content-Type: application/json`
- Body:

```json
{
  "partner_id": 45,
  "username": "john_wifi_123"
}
```

Example curl:

```bash
curl -X POST "https://example.odoo.com/wifast_customer_username/api/contact/username" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"partner_id": 45, "username": "john_wifi_123"}'
```

When `partner_id` is not provided, the contact can be identified by `email` or
`phone`.

Example success response:

```json
{
  "success": true,
  "contact": {
    "id": 45,
    "name": "John Smith",
    "username": "john_wifi_123"
  }
}
```

Common error response:

```json
{
  "success": false,
  "error": "contact_not_found"
}
```
