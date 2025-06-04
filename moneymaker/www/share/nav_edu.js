document.addEventListener("DOMContentLoaded", ()=>{
    const search = document.getElementById("search-input");
    const form = document.getElementById("search-form");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        let query = search.value;
        
        location.href = `./search?q=${query}`
    })
})