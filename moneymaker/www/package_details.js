document.addEventListener("DOMContentLoaded", async (e) => {
    const packageName = getUrlParameter("id");
    const recurringType = getUrlParameter("recurring") ?? "1";
    const sessionId = getSessionID();
    const initOptions = [];
    let currentoptions = [];

    const monthlyTab = document.getElementById("pills-monthly-tab");
    const yearlyTab = document.getElementById("pills-yearly-tab");
    const selects = document.querySelectorAll(".price-select");
    const addedPrices = document.querySelectorAll(".added-price");
    const priceDisplayLeft = document.getElementById("price-display-left");
    const oldPriceLeft = document.getElementById("old-price-display-left");
    const oldPriceRight = document.getElementById("old-price-display-right");
    const priceDisplayRight = document.getElementById("price-display-right");
    const saveBtn = document.getElementById("save-btn");
    const subBtn = document.getElementById("sub-btn");
    const preLoader = document.getElementById("preloader");

    const taxPercent = 15;
    const savedOrder = await getSavedOrder(sessionId);
    const discount_percent = savedOrder.discount / 100

    setInitOptions(savedOrder.benefits)
    
    let fixedTotalAmount = savedOrder.fixed_amount;
    let totalAmount = savedOrder.amount;
    totalAmount *= monthMultiplier();
    
    priceDisplayLeft.textContent = totalAmount.toFixed(2).toString().split(".")[0];
    priceDisplayRight.textContent = totalAmount.toFixed(2).toString().split(".")[1];

    displayOldPrice(totalAmount, discount_percent);

    hideLoader();

    monthlyTab.onclick = (e) => {
        showLoader();
        location.href = `/package_detail?id=${packageName}&recurring=1`
    }
    yearlyTab.onclick = (e) => {
        showLoader();
        location.href = `/package_detail?id=${packageName}&recurring=2`
    }
    
    // Attach event listeners to all select elements
    selects.forEach(select => {
        select.addEventListener("change", updateTotalPrice);
    });

    saveBtn.onclick = saveOptions
    subBtn.onclick = checkOut

    async function getSavedOrder() {
        return await new Promise(function(resolve, reject) {
            $.ajax({
                url: `/api/method/moneymaker.www.package_detail.saved_order?package_name=${packageName}&session_id=${sessionId}&recurring_type=${recurringType}`,
                type: "GET",
                success: function (response) {
                    if(response.message.status == 500) {
                        reject(response.message.error)
                    } else {
                        resolve(response.message);
                    }
                },
                error: function (xhr, status, error) {
                    console.log(error);
                    reject(error)
                }
            });
        });
    }

    function setInitOptions(options) {
        if(!options) {
            return;
        }
        for(let i = 0; i < selects.length; i++) {
            const select = selects[i];
            const benefit = select.getAttribute("data-benefit");

            for(let x = 0; x < select.options.length; x++) {
                const currentOption = select.options[x];
                const option = currentOption.value;
                const optionId = currentOption.getAttribute("data-id");
                const price = parseFloat(currentOption.getAttribute("data-price")) || 0;

                if(options[benefit] && options[benefit].option === optionId) {
                    select.options[x].selected = true;
                    const discounted_price = options[benefit].price - (options[benefit].price * discount_percent);

                    addedPrices[i].textContent = discounted_price.toFixed(2).toString();
                    
                    initOptions.push({
                        benefit: benefit,
                        option: option,
                        option_id: optionId,
                        price: price,
                    })

                    break;
                }
            }
        }
        saveBtn.disabled = true;
        saveBtn.classList.add("disable-btn");
    }

    function updateTotalPrice() {
        currentoptions = [];
        totalAmount = 0.0;
        for(let i = 0; i < selects.length; i++) {
            const select = selects[i];
            const selectedOption = select.options[select.selectedIndex];
            const price = parseFloat(selectedOption.getAttribute("data-price")) || 0;
            const benefit = select.getAttribute("data-benefit");
            const option = selectedOption.value;
            const optionId = selectedOption.getAttribute("data-id");

            totalAmount += price;
            // const discounted_price = price - (price * discount_percent);
            addedPrices[i].textContent = price.toFixed(2).toString();
                
            currentoptions.push({
                benefit: benefit,
                option: option,
                option_id: optionId,
                price: price,
            })

        }
        
        totalAmount += fixedTotalAmount

        totalAmount *= monthMultiplier()

        const formattedAmount = totalAmount.toFixed(2).toString().split(".")

        priceDisplayLeft.textContent = formattedAmount[0];
        priceDisplayRight.textContent = formattedAmount[1];
        
        displayOldPrice(totalAmount, discount_percent);

        saveBtn.disabled = noChanges();
        noChanges()? saveBtn.classList.add("disable-btn") : saveBtn.classList.remove("disable-btn");
    }

    function displayOldPrice(newPrice, discount) {
        if (oldPriceLeft == null) {
            return;
        }
        const formattedAmount = (newPrice / (1 - discount)).toFixed(2).toString().split(".")

        oldPriceLeft.textContent = formattedAmount[0];
        oldPriceRight.textContent = formattedAmount[1];
    }

    function noChanges() {
        return JSON.stringify(currentoptions) === JSON.stringify(initOptions);
    }

    function monthMultiplier() {
        if(recurringType == "1") {
            return 1
        } else {
            return 12
        }
    }

    async function saveOptions() {
        showLoader();
        const options = [];

        for(let i = 0; i < selects.length; i++) {
            const select = selects[i];
            const selectedOption = select.options[select.selectedIndex];
            const benefit = select.getAttribute("data-benefit");
            const option = selectedOption.value;
            const price = parseFloat(selectedOption.getAttribute("data-price")) || 0;
            const optionId = selectedOption.getAttribute("data-id");
                
            options.push({
                benefit: benefit,
                option: option,
                option_id: optionId,
                price: price,
            })
        }

        const body = {
            package_name: getUrlParameter("id"),
            options: options,
            amount: totalAmount,
            session_id: sessionId,
            recurring_type: recurringType,
        }

        try {
            const response = await $.ajax({
                url: `/api/method/moneymaker.www.package_detail.save_order`,
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(body),
                success: function (response) {

                    if (response.message.status === 200) {
                        saveBtn.disabled = true;
                        saveBtn.classList.add("disable-btn");
                        hideLoader();
                    } else {
                        throw new Error(response.message.error);
                    }
                },
                error: function (xhr, status, error) {
                    alert("فشل تسجيل الدخول! يرجى التحقق من بياناتك.");
                }
            });
    
            if (response.message.status === 200) {
                saveBtn.disabled = true;
                saveBtn.classList.add("disable-btn");
                hideLoader();
            } else {
                throw new Error(response.message.error);
            }
        } catch (error) {
            hideLoader();
            alert(error.message);
        }
    }

    async function checkOut() {
        if(!noChanges()) {
            await saveOptions();
        }

        const packageName = getUrlParameter("id");
        location.href = `/checkout?id=${packageName}&recurring=${recurringType}`
    }

    function getSessionID() {
        let sessionID = getCookie(recurringType == "1"? "order_session_monthly" : "order_session_annual");
        
        if (!sessionID) {
            sessionID = crypto.randomUUID();
            setCookie(recurringType == "1"? "order_session_monthly" : "order_session_annual", sessionID, 2);
        }
    
        return sessionID;
    }
    
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + value + "; path=/" + expires;
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

    function totalAmountWithVat() {
        return totalAmount * (taxPercent / 100)
    }

    function taxTotal() {
        return totalAmount - (totalAmount * (taxPercent / 100))
    }

    function getUrlParameter(name) {
        const params = new URLSearchParams(window.location.search);
        const value = params.get(name);
        return value;
    }
    

    function hideLoader() {
        preLoader.style.display = "none";
    }

    function showLoader() {
        preLoader.style.display = "inline";
    }
})