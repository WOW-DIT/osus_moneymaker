import frappe
import math
from frappe import _
from datetime import datetime

def get_context(context):
    content = getWebContent()
    categories = getCategories(content.institution)
    context = {
        "content":content,
        "category":categories,
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
        "lang": getLang(),
        "year": datetime.today().year,
    }
    
    return context

def getLang():
    if frappe.session.user != "Guest":
        user = frappe.get_doc("User", frappe.session.user)
        return user.language
    
    return "en"

def getInstitutionName():
    brand_name = getBrandName()
    with open(f"/home/frappe/frappe-bench/apps/moneymaker/moneymaker/www/{brand_name}/name.txt", "r") as f:
        institution = f.read()
    return institution

def getSelectedCategory():
    return str(frappe.local.request.args.get('category'))

@frappe.whitelist(allow_guest=True)
def isLoggedIn():
    return frappe.session.user != "Guest"

@frappe.whitelist()
def getBrandName():
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    brand_name = dir_path.split("/")[len(dir_path.split("/")) - 1]
    return brand_name

@frappe.whitelist(allow_guest=True)
def getWebContent():
    brand_name = getBrandName()
    content_id = frappe.get_value("Educational Institution Website Content", {"brand_name": brand_name})
    if content_id is not None:
        content = frappe.get_doc('Educational Institution Website Content',content_id)
        return content

@frappe.whitelist(allow_guest=True)
def getCategories(institution):
    categories = frappe.db.sql(f"""
        SELECT a.name, a.category, a.category_ar, a.image
        FROM `tabCourse Category` AS a
        JOIN 
        `tabCourse` AS c ON a.category = c.category AND c.activee = 1
        where c.institution = %s
        GROUP BY c.category
        ORDER BY a.name """,
        (institution),as_dict=True,)

    return categories

@frappe.whitelist(allow_guest=True)
def getCourses():
    try:
        institution = frappe.form_dict.get("institution")
        name = frappe.form_dict.get("name", None)
        categories = frappe.form_dict.get("categories", [])
        instructor = frappe.form_dict.get("instructor", None)
        order_by = frappe.form_dict.get("order_by", None)
        page = frappe.form_dict.get("page", 1)

        if not institution:
            frappe.throw("Missing institution name")

        page_size = 6
        page = int(page)
        page_offset = int((page - 1) * page_size)

        order_by_line = ""
        # Ensure only valid values for ORDER BY direction
        if order_by:
            if order_by == "new":
                order_by_line = f"ORDER BY c.creation DESC"
            elif order_by == "purchased":
                order_by_line = f"ORDER BY purchase_count DESC"
            elif order_by == "price":
                order_by_line = f"ORDER BY price ASC"


        # Construct conditions safely with placeholders
        conditions = ["c.standalone = 1", "c.activee = 1"]
        values = []

        if name:
            conditions.append("c.course_name LIKE %s")
            values.append(f"%{name}%")

        if frappe.db.exists("Institution", institution):
            conditions.append("c.institution = %s")
            values.append(institution)

        if categories:
            conditions.append("c.category IN %s")
            values.append(tuple(categories))

        if instructor is not None:
            conditions.append("c.created_by LIKE %s")
            values.append(f"%{instructor}%")

        where_clause = " AND ".join(conditions)

        query = f""" 
            SELECT c.name, c.course_name, c.hero_image, c.description, c.created_by, 
                   c.price AS priceold, c.category,
                   COALESCE(AVG(r.rating), 0) AS average_rating, COUNT(r.rating) AS rate_count,
                   COALESCE(FLOOR(AVG(r.rating)), 0) AS full_stars, 
                   ROUND(c.price * (1 - c.discount / 100), 2) AS price,
                   CASE WHEN AVG(r.rating) - FLOOR(AVG(r.rating)) >= 0.5 THEN 1 ELSE 0 END AS half_star, 
                   5 AS total_stars,
                   COUNT(DISTINCT cp.user) AS purchase_count
            FROM `tabCourse` AS c
            LEFT JOIN `tabCourse Ratings` AS r ON c.name = r.course
            LEFT JOIN `tabCourse Purchase` AS cp ON cp.course = c.name AND cp.is_refunded = 0
            WHERE {where_clause}
            GROUP BY c.name
            {order_by_line}
        """

        # Execute the query safely
        courses = frappe.db.sql(query, tuple(values), as_dict=True)
        page_courses = courses[page_offset: (page_offset + page_size)]

        number_of_pages = int(math.ceil(len(courses) / page_size))
        
        return {"courses": page_courses, "number_of_courses": len(courses), "number_of_pages": number_of_pages}
    except Exception as e:
        return str(e)
