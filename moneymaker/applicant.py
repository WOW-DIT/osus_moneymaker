import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_context(context):
    context = {
        "Programs": getAllPrograms(),
        "acadmicYear" :getAllAcadmicYear(),
        "countries" : getAllcountries(),
        "genders" : getAllGender(),
    }
    return context

@frappe.whitelist(allow_guest=True)
def getAllPrograms():
    return frappe.db.sql(f"""SELECT program_name FROM `tabProgram` """, as_dict=True)

@frappe.whitelist(allow_guest=True)
def getAllAcadmicYear():
    return frappe.db.sql(f"""SELECT academic_year_name FROM `tabAcademic Year` """, as_dict=True)

@frappe.whitelist(allow_guest=True)
def getAllcountries():
    return frappe.db.sql(f"""SELECT country_name FROM `tabCountry` """, as_dict=True)

@frappe.whitelist(allow_guest=True)
def getAllGender():
    return frappe.db.sql(f"""SELECT gender FROM `tabGender` """, as_dict=True)


@frappe.whitelist(allow_guest=True)
def applyStudent(data):
    # newGender = frappe.new_doc("Gender")
    # newGender.gender = gender
    # newGender.save(ignore_permissions=True)

    applicant = frappe.new_doc("Student Applicant")
    applicant.first_name = data["first_name"]
    applicant.middle_name = data["middle_name"]
    applicant.last_name = data["last_name"]
    applicant.gender = data["gender"]
    applicant.academic_year = "academic_year"
    applicant.nationality = data["nationality"]
    applicant.studnet_mobile_number = data["mobile"]
    applicant.application_date = data["date"]
    applicant.program = data["program"]
    applicant.student_email_id = data["email"]
    applicant.date_of_birth = data["dob"] or ""
    applicant.city = data["city"]
    applicant.country = data["country"]
    applicant.state = data["state"]
    applicant.address_line_1 = data["address_line_1"] or ""
    applicant.address_line_2 = data["address_line_2"] or ""
    applicant.pincode = data["pincode"] or ""
    
    applicant.save(ignore_permissions=True)
    
    return "Applied Successfully"
    