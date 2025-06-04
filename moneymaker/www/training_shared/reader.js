document.addEventListener("DOMContentLoaded", (e) => {
    let readables = document.querySelectorAll(".readable");
    function defineBtns() {
        startReader.onclick = start
        closeReader. onclick = close
        prevReader.onclick = goPrev
        nextReader.onclick = goNext
        pauseReader.onclick = pause
    }
    
    function start() {
        stopped = false;
        paused = false;
        resetBtns(startReader);

        readables = document.querySelectorAll(".readable");

        function readNext() {
            if (paused || readIndex >= readables.length) return;

            const textEl = readables[readIndex];
            textEl.classList.add("current-reading");
            textEl.scrollIntoView({ behavior: "smooth", block: "center" });

            const text = textEl.textContent;
            const speech = new SpeechSynthesisUtterance(text);
            speech.pitch = 1.0;
            speech.rate = 1.0;
            speech.volume = 1;
            speech.lang = curr_lang == "en" ? "en-US" : "ar-SA";

            speech.onend = () => {
                textEl.classList.remove("current-reading");
                readIndex++;
                readNext();
            };

            window.speechSynthesis.speak(speech);
        }

        readNext();
    }

    function pause() {
        resetBtns(pauseReader);

        window.speechSynthesis.cancel();
        stopped = false;
        paused = true;
    }

    function goPrev() {
        if(stopped) return;

        const prevState = (paused == false);
        pause();

        const textEl = readables[readIndex];
        textEl.classList.remove("current-reading");

        if(readIndex > 0) {
            readIndex--;
        } else {
            readIndex = 0;
        }

        if(prevState) {
            start();
        }
    }

    function goNext() {
        if(stopped) return;

        const prevState = (paused == false);
        pause();

        const textEl = readables[readIndex];
        textEl.classList.remove("current-reading");

        if(readIndex < readables.length - 1) {
            readIndex++;
        } else {
            readIndex = readables.length - 1;
        }
        if(prevState) {
            start();
        }
    }

    function close() {
        pause();

        resetBtns();
        const textEl = readables[readIndex];
        textEl.classList.remove("current-reading");

        readIndex = 0;
    }

    function resetBtns(activeBtn=null) {
        readerBtns.forEach(btn => {
            btn.classList.remove("aud_butn_selected");
        });
        if(activeBtn){
            activeBtn.classList.add("aud_butn_selected");
        }
    }
    
    const readerBtns = document.querySelectorAll(".aud_butn");
    const closeReader = document.getElementById("close-reader");
    const prevReader = document.getElementById("prev-reader");
    const startReader = document.getElementById("start-reader");
    const pauseReader = document.getElementById("pause-reader");
    const nextReader = document.getElementById("next-reader");

    let readIndex = 0;
    let paused = true;
    let stopped = true;

    const curr_lang = document.documentElement.lang
    defineBtns();
});

window.addEventListener("beforeunload", (e) => {
    window.speechSynthesis.cancel();
});