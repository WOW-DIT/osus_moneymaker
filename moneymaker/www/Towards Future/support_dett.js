document.addEventListener("DOMContentLoaded", ()=> {
    const contactForm = document.getElementById("ticket-form");
    const preLoader = document.getElementById("preloader");
  
    hideLoader();
  
    contactForm.addEventListener("submit", (event) => {
        event.preventDefault();
        
        const fields = event.target.querySelectorAll(".form-control")

        const message = fields[0].value

        sendMessage(message);
    })
  
    function sendMessage(message) {
      showLoader();
      const reference = getQueryParam("id")
      fetch(
        `/api/method/moneymaker.www.api.support_det.sendReply?id=${reference}`,
        {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            "message": message,
            "institution": getCookie("institution"),
          }),
        }
      )
        .then(response => response.json())
        .then(res => {
          console.log(res)
          if(res.message.passed === true) {
            location.reload();
          } else {
            hideLoader();
          }
        })
        .catch(error => {
          hideLoader();
          console.log(error)
        });
    }
    
    function getQueryParam(param) {
      let urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(param);
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