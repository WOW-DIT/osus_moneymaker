document.addEventListener("DOMContentLoaded", function(e) {
    window.speechSynthesis.cancel();
    // const brand = document.body.getAttribute("data-brand")
    const curr_lang = document.documentElement.lang
    const texts = document.querySelectorAll(".readable")

    texts.forEach((el) => {
        el.addEventListener("click", function() {
            const text = el.innerHTML
            read(text)
        });
    })

    function read(text) {
        window.speechSynthesis.cancel();

        const speech = new SpeechSynthesisUtterance(text)
        speech.pitch = 1.0
        speech.rate = 0.7
        speech.volume = 1
        speech.lang = curr_lang == "en"? "en-US" : "ar-SA"

        window.speechSynthesis.speak(speech);
    }
})