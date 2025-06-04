import frappe
from datetime import datetime, timedelta

class SubscriptionModel:
    def get_subscriptions(self, user):
        subs = frappe.db.sql("""
            SELECT
                s.name,
                s.package,
                s.package_title,
                s.active,
                s.status,
                s.auto_renewal,
                s.payment_cycle,
                s.subscription_date,
                s.end_date
            FROM
                `tabInstitution Subscription` AS s
            WHERE
                s.user = %s;
        """, (user,), as_dict=True)

        for s in subs:
            # start_date = datetime.strftime(s.subscription_date, "%Y-%m-%d")
            today = datetime.now().date()

            if s.end_date < today and s.active == 1:
                sub = frappe.get_doc("Institution Subscription", s.name)
                sub.active = 0
                sub.save(ignore_permissions=True)

                s.active = 0
                
        frappe.db.commit()

        return subs


    def get_packages(self):
        packages = frappe.db.sql("""
            SELECT
                p.name,
                p.title,
                p.image,
                p.description,
                p.free,
                p.price,
                p.pay_type,
                p.discount,
                p.benefits_template
            FROM
                `tabOsus Packages` AS p
            WHERE
                p.active = 1 AND p.pay_type = 'Monthly';
        """, as_dict=True)

        for p in packages:

            services = frappe.db.sql("""
                SELECT
                    s.service,
                    s.active
                FROM
                    `tabOsus Services Table` AS s
                WHERE
                    s.parent = %s;
            """, (p.name), as_dict=True)

            p["services"] = services

        return packages


    def package_details(self, package_name):
        p = frappe.get_doc("Osus Packages", package_name)

        monthly_package = {
            "name": p.name,
            "title": p.title,
            "description": p.description,
            "free": p.free,
            "price": p.price + (p.price * (p.discount / 100)),
            "old_price": p.price,
            "pay_type": p.pay_type,
            "discount": p.discount,
        }
        benefits = frappe.db.sql("""
            SELECT
                b.benefit,
                b.title,
                b.binary,
                b.available,
                b.service
            FROM
                `tabPackage Benefits Table` AS b
            WHERE
                b.parent = %s
            ORDER BY b.service;
        """, (p.benefits_template,), as_dict=True)

        for ben in benefits:
            options = frappe.db.sql("""
                SELECT
                    o.option,
                    o.title,
                    o.additional_price,
                    o.image
                FROM
                    `tabBenefit Options` AS o
                WHERE
                    o.parent = %s
                ORDER BY
                    o.additional_price;
            """, (ben.benefit,), as_dict=True)

            ben["options"] = options

        monthly_package["benefits"] = benefits

        ## Get the annual package
        if p.annual_package and p.pay_type == "Monthly":
            p = frappe.get_doc("Osus Packages", p.annual_package)
            annual_package = {
                "name": p.name,
                "title": p.title,
                "description": p.description,
                "free": p.free,
                "price": p.price + (p.price * (p.discount / 100)),
                "old_price": p.price,
                "pay_type": p.pay_type,
                "discount": p.discount,
            }
            benefits = frappe.db.sql("""
                SELECT
                    b.benefit,
                    b.title,
                    b.binary,
                    b.available,
                    b.service
                FROM
                    `tabPackage Benefits Table` AS b
                WHERE
                    b.parent = %s
                ORDER BY b.service;
            """, (p.benefits_template,), as_dict=True)

            for ben in benefits:
                options = frappe.db.sql("""
                    SELECT
                        o.option,
                        o.title,
                        o.additional_price,
                        o.image
                    FROM
                        `tabBenefit Options` AS o
                    WHERE
                        o.parent = %s
                    ORDER BY
                        o.additional_price;
                """, (ben.benefit,), as_dict=True)

                ben["options"] = options

            annual_package["benefits"] = benefits

            return {"monthly": monthly_package, "annual": annual_package}
        
        return {"monthly": monthly_package}
        
    
    def package_init_price(self, package_name, recurring_type="1"):
        p = frappe.get_doc("Osus Packages", package_name)
        if recurring_type == "2" and p.annual_package and p.pay_type == "Monthly":
            p = frappe.get_doc("Osus Packages", p.annual_package)

        package = {
            "price": p.price + (p.price * (p.discount / 100)) if p.free == 0 else 0.00,
            "old_price": p.price,
        }
        return package
    
    
    def saved_order(self, package_name, session_id, recurring_type):
        package = frappe.get_doc("Osus Packages", package_name)
        saved_order_id = frappe.get_value("Saved Temporary Order", {"session_id": session_id, "package": package.name})

        if recurring_type == "2" and package.annual_package and package.pay_type == "Monthly":
            package = frappe.get_doc("Osus Packages", package.annual_package)
            saved_order_id = frappe.get_value("Saved Temporary Order", {"session_id": session_id, "package": package.name})

        price =  package.price - (package.price * (package.discount / 100))
        amount = price

        # if user == "Guest":
        #     return {"status": 201, "benefits": None, "amount": amount, "fixed_amount": price, "discount": package.discount}
        
        try:
            if saved_order_id is not None:
                # saved_order = frappe.get_doc("Saved Temporary Order", saved_order_id)
                benefits = {}
                bens = frappe.db.sql("""
                    SELECT b.benefit, b.option
                    FROM `tabSaved Benefits Table` AS b
                    WHERE b.parent = %s
                    ORDER BY b.idx;
                """, (saved_order_id), as_dict=True)

                for b in bens:
                    option = frappe.db.sql("""
                        SELECT o.title, o.additional_price
                        FROM `tabBenefit Option` AS o
                        WHERE o.name = %s;
                    """, (b.option), as_dict=True)[0]

                    b["price"] = option["additional_price"]
                    
                    benefits[b["benefit"]] = b

                    amount += option.additional_price - (option.additional_price * (package.discount / 100))
                
                return {"status": 200, "package_name": package.title, "benefits": benefits, "amount": amount, "fixed_amount": price, "discount": package.discount, "saved_order": saved_order_id}

            else:
                price =  package.price - (package.price * (package.discount / 100))

                return {"status": 201, "package_name": package.title, "benefits": None, "amount": amount, "fixed_amount": price, "discount": package.discount, "saved_order": saved_order_id}
            
        except Exception as e:
            return {"status": 500, "error": str(e)}


    def apply_coupon(self, code):
        try:
            today = datetime.now().date()
            coupon_id = frappe.get_value(
                "Website Coupon",
                {"coupon_code": code, "enabled": 1, "valid_from": ["<=", today], "valid_upto": [">=", today]},
            )

            if coupon_id:
                coupon = frappe.get_doc("Website Coupon", coupon_id)

                if coupon.used >= coupon.maximum_use:
                    return {"status": 500, "error": "تخطى الحد المسموح لعدد الإستخدامات"}
                
                return {"status": 200, "discount_percent": coupon.pricing, "maximum_discount": coupon.maximum_discount}
            else:
                return {"status": 404, "error": "رمز غير صالح أو منتهي الصلاحية"}
            
        except Exception as e:
            return {"status": 500, "error": str(e)}

    def toggle_auto_renew(self, sub_name):
        try:
            sub = frappe.get_doc("Institution Subscription", sub_name)
            if sub.auto_renewal == 1:
                sub.auto_renewal = 0
            else:
                sub.auto_renewal = 1

            sub.save()

            return {"status": 200}

        except Exception as e:

            return {"status": 500, "error": str(e)}

    def payment_methods(self):
        methods = frappe.db.sql("""
            SELECT
                m.method,
                m.method_ar,
                m.image
            FROM
                `tabPayment Method` AS m
            WHERE
                m.active = 1;
        """, as_dict=True)

        return methods