# Copyright (C) 2018 DynApps <http://www.dynapps.be>
# Copyright (C) 2022 Yizuo <https://www.yizuo.ltd>
# @author Stefan Rijnhart <stefan@opener.amsterdam>
# @author Robin Conjour <rconjour@demolium.com>
# PengYB(YiZuo) use OWL Rewrite.
# @author PengYB <pengyb@yizuo.ltd>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Show confirmation dialogue before copying records",
    "version": "16.0.1.0.0",
    "author": "Dynapps,YiZuo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/web",
    "license": "AGPL-3",
    "category": "Tools",
    "depends": [
        "web",
    ],
    "assets": {
        "web.assets_backend": [
            "web_copy_confirm/static/src/js/web_copy_confirm.js",
        ],
        "web.qunit_suite_tests": [
            "web_copy_confirm/static/tests/**/*",
        ],
    },
    "installable": True,
}
