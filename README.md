# WiFast Odoo 19 Enterprise - Custom Addons (dev)

Custom Odoo modules for WiFast ERP system.

## Branch Strategy

| Branch | Environment | URL |
|--------|------------|-----|
| `main` | Production | https://erp.wifast.net |
| `uat` | UAT/Staging | https://uat.erp.wifast.net (Local: http://192.168.99.62:8169/web/login) |
| `dev` | Development | https://dev.erp.wifast.net |

## Workflow

1. Develop on `dev` branch
2. Test on DEV server (`dev.erp.wifast.net`)
3. Merge to `uat` for testing
4. After approval, merge to `main` for production
