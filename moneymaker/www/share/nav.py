import frappe

from frappe import _

def get_context(context):
    #frappe.local.cookie_manager.set_cookie("sss", "sss")
    frappe.throw("ADSADASDASDAS")
    company  = initCompanyCookies()
    context = {
        "content":getWebContent(company),
    }
    return context


@frappe.whitelist(allow_guest=True)
def initCompanyCookies():
    path = frappe.local.request.path
    brandName = path.split('/')[1]
    company = frappe.db.sql(""" select company from `tabWebsite Basic Template Content Management` where brand_name=%s """,(brandName) , as_dict=True)[0].company
    frappe.local.cookie_manager.set_cookie("company", company)
    frappe.local.cookie_manager.set_cookie("brand", brandName)

    return company

@frappe.whitelist(allow_guest=True)
def getWebContent(company):
    #company = frappe.request.cookies.get('company')
    temps = frappe.db.sql(f""" select name from `tabWebsite Basic Template Content Management` where publish=1 and company=%s """,(company),as_dict=True)[0]
    p = frappe.get_doc("Website Basic Template Content Management" , temps.name)

    return p