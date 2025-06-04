import frappe
# from ....education.education.subscriptions.subscription import SubscriptionModel
from .models.subscription import SubscriptionModel
from frappe import _

def get_context(context):
    context = {
        "content":getWebContent(),
        "package_details": package_details(),
        "payment_methods": payment_methods(),
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
def package_details(package_name=None, recurring_type=None):
    if package_name is None:
        package_name = frappe.local.request.args.get('id')

    if recurring_type is None:
        recurring_type = frappe.local.request.args.get('recurring')
    
    
    if not recurring_type:
        recurring_type = "1"


    package = SubscriptionModel().package_details(package_name)
    package["recurring_type"] = str(recurring_type)

    return package


@frappe.whitelist(allow_guest=True)
def package_init_price(package_name, recurring_type="2"):
    try:
        package = SubscriptionModel().package_init_price(package_name, recurring_type)

        return {"status": 200, "data": package}
    except Exception as e:
        return {"status": 500, "error": e}
    

@frappe.whitelist(allow_guest=True)
def payment_methods():
    methods = SubscriptionModel().payment_methods()
    return methods


@frappe.whitelist(allow_guest=True)
def save_order(package_name, options, amount, session_id, recurring_type):
    def appendOption(order, option):
        order.append(
            "benefits",
            {
                "benefit": option["benefit"],
                "option": option["option_id"],
                "price": option["price"],
            }
        )

    try:
        package = frappe.get_doc("Osus Packages", package_name)

        if recurring_type == "2" and package.annual_package and package.pay_type == "Monthly":
            package = frappe.get_doc("Osus Packages", package.annual_package)

        saved_order_id = frappe.get_value("Saved Temporary Order", {"session_id": session_id, "package": package.name})


        if saved_order_id is not None:
            sOrder = frappe.get_doc("Saved Temporary Order", saved_order_id)
            sOrder.package = package.name
            sOrder.benefits = []

        else:
            sOrder = frappe.new_doc("Saved Temporary Order")
            sOrder.session_id = session_id
            sOrder.package = package.name

        for o in options:
            appendOption(sOrder, o)

        sOrder.amount = amount
        sOrder.save(ignore_permissions=True)

        return {"status": 200}

    except Exception as e:
        return {"status": 500, "error": str(e)}

@frappe.whitelist(allow_guest=True)
def saved_order(package_name, session_id, recurring_type="1"):
    order = SubscriptionModel().saved_order(package_name, session_id, recurring_type)
    return order