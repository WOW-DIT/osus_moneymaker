import frappe
from frappe import _
from datetime import datetime

def get_context(context):
    content = getWebContent()
    context = {
        "content":content,
        "category":getCategories(content.institution),
        "course":singleCourse(),
        "finishedSurvey": finishedSurvey(),
        # "course_items": courseItems(),
        # "course_langs": courseLangs(),
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
        # "number_of_students": numberOfStudents()
        # "blogger":getBlogger(),
        # "news":getNews(),
        # "plans":getplans()
    }
    return context

def getInstitutionName():
    with open("/Osus/name.txt", "r") as f:
        institution = f.read()
    return institution

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
    

@frappe.whitelist()
def finishedSurvey():
    course_id=frappe.local.request.args.get('id')
    user = frappe.session.user

    if frappe.db.exists("User Survey Answer", {"user": user, "course": course_id}):
        return True
    
    return False


@frappe.whitelist(allow_guest=True)
def getCategories(institution="Osus"):
        # SELECT name, hero_image, description, created_by, price
        # FROM `tabCourse`
    categories = frappe.db.sql(f"""
        SELECT a.category, a.image
        FROM `tabCourse Category` AS a
        JOIN 
        `tabCourse` AS c ON a.category = c.category AND c.activee = 1
        where c.institution = %s
        GROUP BY c.category
        ORDER BY a.name """,
        (institution),as_dict=True,)
    
    return categories


@frappe.whitelist(allow_guest=True)
def courseLangs():
    lang = ""
    course_id=frappe.local.request.args.get('id')
    langs = frappe.db.sql(f"""
        SELECT cl.language
        FROM `tabCourse Languages` AS cl
        WHERE cl.parent=%s
        ORDER BY cl.idx """,(course_id),as_dict=True,)
    
    for i, l in enumerate(langs):
        lang += l.language
        if i < len(langs)-1:
            lang += "/"

    return lang


@frappe.whitelist(allow_guest=True)
def singleCourse():
    id=frappe.local.request.args.get('id')
    course = frappe.db.sql(f"""
        SELECT c.name, c.description, c.category,c.survey_template
        FROM `tabCourse` AS c
        WHERE c.name= %s AND c.activee = 1
         """,
        (id,),as_dict=True,)
    
    questions = frappe.db.sql("""
        SELECT sq.name, sq.question, sq.type
        FROM `tabSurvey Questions Table` AS q
        LEFT JOIN `tabSurvey Question` AS sq ON sq.name = q.question
        WHERE q.parent = %s
        ORDER BY q.idx
        """, (course[0].survey_template), as_dict=True)

    for question in questions:
        if question.type != "Text":
            options = frappe.db.sql("""
                SELECT o.option
                FROM `tabSurvey Options Table` AS o
                WHERE o.parent = %s
                ORDER BY o.parent AND o.idx
            """, (question.name), as_dict=True)
        else:
            options = None

        question["options"] = options

    return {"course": course[0], "survey": questions}


@frappe.whitelist()
def submitSurvey(data):
    try:
        id=frappe.local.request.args.get('id')

        course = frappe.get_doc("Course", id)
        user = frappe.get_doc("User", frappe.session.user)

        questions = data["questions"]
        # survey_template = data["survey"]
        # course = data["course"]

        for q in questions:
            answers = questions[q]
            if len(answers) > 0:
                answer = frappe.new_doc("User Survey Answer")
                answer.user = user
                # answer.survey = survey_template
                answer.question = q
                answer.answer = "\n,\n".join(answers)
                answer.course = course.name
                answer.insert(ignore_permissions=True)

        certificate_url = newCertificate(course, user)

        return {"message": "Survey has been submitted successfully", "successful": True, "certificate_url": certificate_url}

    except Exception as e:
        return {"message": e, "successful": False}


@frappe.whitelist()
def newCertificate(course, user):
    try:
        cert = frappe.new_doc("Certificate")
        cert.user = user.name
        cert.date = datetime.now()
        cert.type = "Course"
        cert.course = course.name
        cert.instructor = course.created_by
        cert.institution = course.institution

        cert.insert(ignore_permissions=True)

        return cert.get_url()
    
    except:
        return None