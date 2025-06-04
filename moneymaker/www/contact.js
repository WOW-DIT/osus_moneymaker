document.addEventListener("DOMContentLoaded", ()=> {
    const contactForm = document.getElementById("contact-form");
    const fields = document.querySelectorAll(".form-control")

    contactForm.addEventListener("submit", (event) => {
        event.preventDefault();
        
        console.log(fields.length)
        const fullName = fields[0].value
        const email = fields[1].value
        const phone = fields[2].value
        const subject = fields[3].value
        const message = fields[4].value

        sendMessage(fullName, phone, email, subject, message);
    })

    function sendMessage(fullName, phone, email, subject, message) {
        $.ajax({
            url: "/api/method/moneymaker.www.contact.sendIssue",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "full_name": fullName,
                "phone_number": phone,
                "email": email.toLowerCase(),
                "subject": subject,
                "message": message,
            }),
            success: function (response) {
                location.reload();
            },
            error: function (xhr, status, error) {
                alert("فشل تسجيل الدخول! يرجى التحقق من بياناتك.");
            }
        });
    }


})