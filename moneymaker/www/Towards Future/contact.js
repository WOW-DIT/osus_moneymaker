document.addEventListener("DOMContentLoaded", ()=> {
  const contactForm = document.getElementById("contact-form");
  const preLoader = document.getElementById("preloader");

  hideLoader();

  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    
    const fields = event.target.querySelectorAll(".form-control")

    const fullName = fields[0].value
    const phoneNumber = fields[1].value
    const email = fields[2].value
    const subject = fields[3].value
    const message = fields[4].value

    sendMessage(fullName, phoneNumber, email, subject, message);
  })

  function sendMessage(fullName, phoneNumber, email, subject, message) {
    showLoader();
    fetch(
      `/api/method/moneymaker.www.api.contact.sendIssue`,
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          "full_name": fullName,
          "phone_number": phoneNumber,
          "email": email,
          "subject": subject,
          "message": message,
          "institution": getCookie("institution"),
        }),
      }
    )
      .then(response => response.json())
      .then(res => {
        hideLoader();
        console.log(res.message)
        if(res.message.passed === true) {
          
        }
      })
      .catch(error => {
        hideLoader();
        console.log(error)
      });
  }

  function getCookie(name) {
    const nameEQ = name + "=";
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim();
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }

  function hideLoader() {
    preLoader.style.display = "none";
  }

  function showLoader() {
    preLoader.style.display = "inline";
  }
})