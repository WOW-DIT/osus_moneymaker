import frappe

from frappe import _

def get_context(context):
    context = {
        "content":getWebContent(),
        "user": frappe.session.user,
        "cart": getCart(),
    }

    return context


@frappe.whitelist(allow_guest=True)
def getWebContent():
    content = {}
    main_content = frappe.get_doc("Website Manager", "Website Manager")
    content["main"] = main_content
    return content


@frappe.whitelist(allow_guest=True)
def getCart(item_id = None):
    user = frappe.session.user
    if user == "Guest":
        return None
    
    cart_id = frappe.get_value("Osus Cart", {"user": user, "workflow_state": "Pending"})

    if cart_id is not None:

        cart = frappe.get_doc("Osus Cart", cart_id)
        # for i in cart.items:
        #     item = frappe.get_doc("Item", i.item)
        #     i.image = item.image

        return cart
    
    else:
        cart = createCart()

        ### get the package item and add it in the cart
        # if item_id is not None:
        #     cart.append("items", {"item": item_id, price})

        return cart


def createCart():
    user = frappe.session.user
    cart = frappe.new_doc("Osus Cart")
    cart.user = user
    cart.insert(ignore_permissions=True)

    return cart

@frappe.whitelist()
def deleteItem(item_id):
    cart = getCart()

    if cart is not None:
        item_value = frappe.get_value("Cart Item Table", filters={"item": item_id, "parent": cart.name})
        if item_value is not None:
            item = frappe.get_doc("Cart Item Table", item_value)
            item.delete(ignore_permissions=True)

            frappe.db.commit()

            cart = getCart()

            total = 0
            vat = 0
            grand_total = 0

            for item in cart.items:
                grand_total += item.price * item.qty

            vat = grand_total * 0.15

            total = grand_total - vat

            cart.total_amount = float(total)
            cart.vat = float(vat)
            cart.grand_total = float(grand_total)

            cart.save(ignore_permissions=True)
            frappe.db.commit()
            
            return cart

    return None
