import frappe
import requests
import base64

class ClientModel:

    def profile_info(self):
        try:
            p_id = frappe.get_value("Profile", {"user": frappe.session.user})

            if p_id is not None:
                profile = frappe.get_doc("Profile", p_id)
                attachs = frappe.db.sql("""
                    SELECT f.name
                    FROM `tabFile` AS f
                    WHERE f.attached_to_name = %s;
                """, (p_id), as_dict=True)

                is_completed = True

                if profile.user_type == "Individual":
                    if len(attachs) < 3:
                        is_completed = False

                elif profile.user_type == "Institution":
                    if len(attachs) < 4:
                        is_completed = False
                
                return {"profile": profile, "is_completed": is_completed}
            else:
                return None
            
        except Exception as e:
            frappe.throw(str(e))

    
    def register_comp(self, data):
        try:
            institution = str(data.get("institution")).strip()
            email = str(data.get("email")).strip().lower()
            phone = str(data.get("phone")).strip()
            password = str(data.get("pass")).strip()
            domain = str(data.get("domain")).strip()
            account_name = data.get("account_name")
            iban = str(data.get("iban")).strip()
            bank_name = data.get("bank_name")

            validation = self.validateInstitution(institution, phone)
            if validation["status"] == 500:
                return validation
            
            validation = self.validateUser(email)
            if validation["status"] == 500:
                return validation

            inst = frappe.new_doc("Institution")
            inst.institution = institution
            inst.insert(ignore_permissions=True)
            frappe.db.commit()
            
            ## Create new user
            try:
                user = frappe.new_doc("User")
                user.first_name = institution
                user.enabled = 1
                user.email = email
                user.phone = phone
                user.mobile_no = phone
                user.role_profile_name = "Third Party"
                user.module_profile = "Third Party"
                user.institution = inst.name
                user.new_password = password
                user.insert(ignore_permissions=True)

            ## If user creation failed, remove the created insitution
            except Exception as e:
                if frappe.db.exists("Institution", inst.name):
                    inst = frappe.get_doc("Institution", self.institution_name)
                    inst.delete(ignore_permissions=True)

                return {"passed": False, "status": 500, "message": str(e)}
                

            self.institutionPermission(user.name, inst.name)

            profile = self.createProfile({
                "user": user.name,
                "account_name": account_name,
                "bank_name": bank_name,
                "iban": iban,
                "domain": domain,
                "user_type": "Institution",
                "institution": inst.name,
            })

            frappe.db.commit()

            return {"passed": True, "status": 200, "profile_name": profile.name,}

        except Exception as e:
            return {"passed": False, "status": 400, "message": str(e)}
        
        
    def validateInstitution(self, institution_name, contact_number):
        if frappe.db.exists("Institution", institution_name):
            return {"passed": False, "status": 500, "message": "Institution already exists"}

        if frappe.db.exists("Institution", {"contact_number": contact_number}):
            return {"passed": False, "status": 500, "message": "Contact number is taken"}
        
        return {"status": 200}


    def validateUser(self, email):
        if frappe.db.exists("User", email):
            return {"passed": False, "status": 500, "message": "Email is already taken"}
        else:
            return {"status": 200}
        
        
    def institutionPermission(self, user, institution):
        per = frappe.new_doc("User Permission")
        per.user = user
        per.allow = "Institution"
        per.for_value = institution
        per.insert(ignore_permissions=True)


    def register_user(self, data):
        try:
            first_name = str(data.get("firstname")).strip()
            email = str(data.get("email")).strip().lower()
            phone = str(data.get("phone")).strip()
            password = str(data.get("pass")).strip()
            domain = str(data.get("domain")).strip()
            account_name = data.get("account_name")
            iban = str(data.get("iban")).strip()
            bank_name = data.get("bank_name")

            if frappe.get_value("User", email) is not None:
                return {"passed": False, "status": 400, "message": "This email is taken"}
            
            user = frappe.new_doc("User")
            user.first_name = first_name
            user.enabled = 1
            user.email = email
            user.phone = phone
            user.mobile_no = phone
            user.role_profile_name = "Third Party"
            user.module_profile = "Third Party"
            # user.institution = institution
            user.new_password = password
            user.insert(ignore_permissions=True)

            frappe.db.commit()

            profile = frappe.new_doc("Profile")
            profile.user = user.name
            profile.holder_name = account_name
            profile.bank_name = bank_name
            profile.iban = iban
            profile.domain = domain
            profile.user_type = "Individual"
            profile.insert(ignore_permissions=True)

            frappe.db.commit()
            return {"passed": True, "status": 200, "profile_name": profile.name,}

        except Exception as e:
            return {"passed": False, "status": 400, "message": str(e)}
        

    def createProfile(self, data):
        profile = frappe.new_doc("Profile")
        profile.user = data["user"]
        profile.holder_name = data["account_name"]
        profile.bank_name = data["bank_name"]
        profile.iban = data["iban"]
        profile.domain = data["domain"]
        profile.user_type = data["user_type"]

        if data["user_type"] == "Institution":
            profile.institution = data["institution"]
            
        profile.insert(ignore_permissions=True)

        return profile
    
    def edit_profile(self, data: dict):
        try:
            institution = data.get("institution")
            # full_name = data.get("full_name")
            password = data.get("password", None)
            iban = data.get("iban", "")
            holder_name = data.get("holder_name", "")
            bank_name = data.get("bank_name", "")
            domain = data.get("domain", "")
            phone = data.get("phone", "")

            user = frappe.get_doc("User", frappe.session.user)

            profile_id = frappe.get_value("Profile", {"user": user.name})
            if not profile_id:
                return {"passed": False, "status": 404, "error": f"لم يتم العثور على الملف الشخصي للمستخدم: {user.name}"}

            profile = frappe.get_doc("Profile", profile_id)

            profile.domain = domain
            profile.iban = iban
            profile.holder_name = holder_name
            profile.bank_name = bank_name

            if profile.user_type == "Institution" and institution:
                profile.institution = institution
                user.institution = institution

            if password:
                user.new_password = password
                
            user.mobile_no = phone
            user.phone = phone
            user.save()

            profile.save()
            frappe.db.commit()
            return {"passed": True, "status": 200}

        except Exception as e:
            return {"passed": False, "status": 404, "error": str(e)}