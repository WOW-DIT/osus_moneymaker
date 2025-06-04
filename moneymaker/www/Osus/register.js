document.addEventListener("DOMContentLoaded", (e) => {
  const preLoader = document.getElementById("preloader");
  hideLoader();
    const firstName = document.getElementById("first-name");
    const lastName = document.getElementById("last-name");
    const phoneNumber = document.getElementById("phone-number");
    const email = document.getElementById("email");
    const pass = document.getElementById("pass");
    const conf_pass = document.getElementById("cpass");
    const form = document.getElementById("register-form");
    const registerBtn = document.getElementById("register-btn")

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      register()
    })
    const baseUrl = "https://osus.wowdigital.sa"
    function register() {
      if(pass.value!=conf_pass.value)
        {
            conf_pass.style="border-color: red;"
            alert("كلمة السر غير متطابقة");
            return;
        }else{
            conf_pass.style="border-color: none;"
            
        }
        showLoader();

        fetch(
            baseUrl+`/api/method/education.third_party_api.register`,
            {
              method: "POST",
              headers: {"Content-Type": "application/json"},
              body: JSON.stringify({
                "first_name": firstName.value,
                "last_name": lastName.value,
                "phone_number": phoneNumber.value,
                "email": email.value,
                "password": pass.value,
              }),
            }
          )
            .then(response => response.json())
            .then(res => {
              if(res.message.passed == true) {
                hideLoader();
                window.location.href = "login"
              } else {
                hideLoader();
                alert(res.message.message)
              }
            })
            .catch(error => {
                
            });
    }
    function hideLoader() {
      preLoader.style.display = "none";
  }
  
  function showLoader() {
      preLoader.style.display = "inline";
  }
    $("#conf_pass").on("change", async function(event) {
      event.preventDefault();
      console.log(this.value);
      if(pass.value!=this.value)
      {
          this.style="border-color: red;"
      }else{
          this.style="border-color: none;"
          console.log("ok");
      }
  });
})