import frappe
# from ....education.education.subscriptions.subscription import SubscriptionModel
from .models.subscription import SubscriptionModel
from frappe import _

def get_context(context):
    context = {
        "content":getWebContent(),
        "packages": get_packages(),
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
    }

    return context


@frappe.whitelist(allow_guest=True)
def getWebContent():
    content = {}
    main_content = frappe.get_doc("Website Manager", "Website Manager")
    content["main"] = main_content
    return content

@frappe.whitelist(allow_guest=True)
def isLoggedIn():
    return frappe.session.user != "Guest"

## Returns packages for each service type
# @frappe.whitelist(allow_guest=True)
# def get_packages(pay_type: str = "Annual"):
#     tiers = frappe.db.sql("""
#             SELECT t.name
#             FROM `tabSubscription Tier` AS t
#             ORDER BY t.order_no
#         """, as_dict=True)
    
#     services = frappe.db.sql("""
#             SELECT t.name
#             FROM `tabOsus Service` AS t
#         """, as_dict=True)
    

#     all_services = []
#     for s in services:

#         all_packages = []
#                 # ORDER BY
#                 #     CASE p.tier
#                 #         WHEN 'Basic' THEN 1
#                 #         WHEN 'Premium' THEN 2
#                 #         WHEN 'Ultra' THEN 3
#                 #     END;
#         for t in tiers:
#             packages = frappe.db.sql("""
#                 SELECT p.name, p.free, CAST(p.price AS INT) AS price, p.discount, p.benefits_template, p.tier, t.image,
#                     CAST(p.price - (p.price * p.discount / 100) AS INT) AS final_price
#                 FROM `tabOsus Packages` AS p
#                 LEFT JOIN `tabSubscription Tier` AS t on t.name = p.tier
#                 WHERE p.subscription_type = %s AND p.pay_type = %s AND p.tier = %s
#             """, (s.name, pay_type, t.name), as_dict=True)

#             for p in packages:
#                 benefits = frappe.db.sql("""
#                     SELECT b.benefit, b.binary, b.available, b.details, b.section
#                     FROM `tabSubscription Benefits` AS b
#                     WHERE b.parent = %s
#                     ORDER BY b.idx
#                 """, (p.benefits_template), as_dict=True)

#                 p["benefits"] = benefits

#                 all_packages.append(p)
        
#         all_services.append({"service": s.name, "packages": all_packages})

#     return {"tiers_length": len(tiers), "services": all_services}



@frappe.whitelist()
def add_item(data):
    try:
        package_name = data["package_name"]
        payment_cycle = data["payment_cycle"]
        package = frappe.get_doc("Osus Packages", package_name)
        packages = frappe.get_list(
            "Osus Packages",
            filters={
                "pay_type": payment_cycle,
                "tier": package.tier,
                "subscription_type": package.subscription_type,
            },
            fields=["name", "price", "discount"]
        )
        if len(packages) > 0:
            package = packages[0]
            item_id = frappe.get_value("Item", {"reference_type": "Osus Packages", "reference": package_name})
            cart = getCart()
            cart.append("items", {
                "item": item_id,
                "price": package.price - (package.price * (package.discount / 100)),
                "qty": 1,
            })

            cart.save(ignore_permissions=True)

            return {"successful": True, "message": "Item Added successfully"}
        
        else:
            return {"successful": False, "message": "Failed to Add item"}
    
    except:
        return {"successful": False, "message": "Failed to Add item"}



@frappe.whitelist(allow_guest=True)
def getCart():
    user = frappe.session.user
    if user == "Guest":
        return None
    
    cart_id = frappe.get_value("Osus Cart", {"user": user, "workflow_state": "Pending"})

    if cart_id is not None:

        cart = frappe.get_doc("Osus Cart", cart_id)

        return cart
    
    else:
        cart = createCart()

        return cart


def createCart():
    user = frappe.session.user
    cart = frappe.new_doc("Osus Cart")
    cart.user = user
    cart.insert(ignore_permissions=True)

    return cart


@frappe.whitelist(allow_guest=True)
def get_packages():
    packages = SubscriptionModel().get_packages()

    return packages
