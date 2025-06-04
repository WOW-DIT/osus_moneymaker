document.addEventListener("DOMContentLoaded", ()=> {
    const contactForm = document.getElementById("ticket-form");
    const preLoader = document.getElementById("preloader");
  
    hideLoader();
  
    contactForm.addEventListener("submit", (event) => {
        event.preventDefault();
        
        const fields = event.target.querySelectorAll(".form-control")

        const subject = fields[0].value
        const message = fields[1].value

        sendMessage(subject, message);
    })
  
    function sendMessage(subject, message) {
      showLoader();
      fetch(
        `/api/method/moneymaker.www.api.new_ticket.sendTicket`,
        {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            "subject": subject,
            "message": message,
            "institution": getCookie("institution"),
          }),
        }
      )
        .then(response => response.json())
        .then(res => {
          hideLoader();
          if(res.message.passed === true) {
            location.href = "support"
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