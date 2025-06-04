import frappe
from frappe.utils import nowdate, add_days 
import requests
from datetime import datetime
from education.pay_api_live import auto_charge, deactivate_sub

@frappe.whitelist(allow_guest=True)
def check_sub_expiry():
    today = nowdate()

    subscriptions = frappe.get_all(
        "Institution Subscription",
        filters={"active": 1, "end_date": ["<", today]},
        fields=["name", "user", "auto_renewal", "saved_card_token", "payment_token", "status"],
    )

    for sub in subscriptions:
        if sub.auto_renewal == 1:
            if sub.saved_card_token and sub.payment_token:
                response = auto_charge(
                    sub_id=sub.name,
                    company_name=sub.company,
                    card_token=sub.saved_card_token,
                    payment_token=sub.payment_token,
                )
                return True
            
            ## If the sub is "Trial" change to "Active"
            elif sub.status == "Trial":
                subscription = frappe.get_doc("Institution Subscription", sub.name)
                subscription.status = "Active"
                subscription.active = 0
                subscription.save(ignore_permissions=True)
                frappe.db.commit()
                return False
                
        else:
            deactivate_sub(sub.name)

    frappe.db.commit()

    return len(subscriptions)

