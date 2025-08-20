{
    "name": "Monstar Report",
    "version": "1.0",
    "category": "Accounting",
    "summary": "Custom invoice/bill PDF layout",
    "description": "Module to change invoice and vendor bill PDF layout programmatically",
    "author": "MLES/Pranto",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "views/invoice_layout_views.xml",
        "views/report_templates.xml",
    ],
    "installable": True,
    "application": False,
}
