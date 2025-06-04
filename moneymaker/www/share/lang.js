document.addEventListener("DOMContentLoaded", function(e) {
    const brand = document.body.getAttribute("data-brand")
    const curr_lang = document.documentElement.lang
    const langBtn = document.getElementById("lang-btn")

    const webUrl = "https://osus.wowdigital.sa"
    langBtn.onclick = changeLange

    function changeLange() {
        fetch(
            `${webUrl}/api/method/moneymaker.www.share.lang.changeLanguage`,
            {
              method: "POST",
              headers: {"Content-Type": "application/json"},
              body: JSON.stringify({
                "lang": curr_lang == "en"? "ar" : "en",
              }),
            }
          )
            .then(response => response.json())
            .then(res => {
              location.reload()
            })
            .catch(error => {
                
            });
    }
})