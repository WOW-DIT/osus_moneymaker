document.addEventListener("DOMContentLoaded", async (e) => {
    const recurringType = getUrlParameter("recurring") ?? "1";
    const sessionId = getSessionID();
    const packageName = getUrlParameter("id");
    let coupon_code = null;
    const discountBlock = document.getElementById("discount-block");
    const discountDisplay = document.getElementById("discount-display");

    const oldDisplay = document.getElementById("old-price-display");
    const oldPriceDisplayLeft = document.getElementById("old-price-display-left");
    const oldPriceDisplayRight = document.getElementById("old-price-display-right");

    const priceDisplayLeft = document.getElementById("price-display-left");
    const priceDisplayRight = document.getElementById("price-display-right");
    const packageNameEl = document.getElementById("package-name");
    // const packageDesc = document.getElementById("package-desc");
    const payMethods = document.querySelectorAll(".pay-method");
    const payCards = document.querySelectorAll(".pay_card");
    const payBtn = document.getElementById("pay-btn");
    const couponField = document.getElementById("coupon-input");
    const couponBtn = document.getElementById("coupon-btn");
    const preLoader = document.getElementById("preloader");

    let selectedPaymentMethod = null;
    let totalAmount = 0;
    let discountAmount = 0;
    let savedOrderName = null;
    
    payCards.forEach((element) => {
        element.addEventListener("click", () => selectPaymentMethod(element));
    });
    couponBtn.onclick = applyCoupon
    
    loadPage();
    

    async function loadPage() {
        const savedOrder = await getSavedOrder(sessionId);
        totalAmount = savedOrder.amount;
        totalAmount *= monthMultiplier()
        savedOrderName = savedOrder.saved_order
        
        displayTotalAmount(totalAmount);
        packageNameEl.textContent = savedOrder.package_name;

        payBtn.onclick = (e) => {
            paymentIntent(totalAmount - discountAmount, savedOrder.package_name);
        }
        hideLoader();
    }

    function displayTotalAmount(amount, oldAmount=null) {
        priceDisplayLeft.textContent = amount.toFixed(2).toString().split(".")[0];
        priceDisplayRight.textContent = amount.toFixed(2).toString().split(".")[1];

        if(oldAmount) {
            oldPriceDisplayLeft.textContent = oldAmount.toFixed(2).toString().split(".")[0];
            oldPriceDisplayRight.textContent = oldAmount.toFixed(2).toString().split(".")[1];
        }
    }

    function selectPaymentMethod(element) {
        // Remove active class from all payment cards
        payCards.forEach((card) => {
            card.querySelector(".form-check-input").checked = false;
        });
        
        // Add active class to the clicked card
        element.querySelector(".form-check-input").checked = true;
        
        selectedPaymentMethod = element.getAttribute("data-method");
    }

    async function getSavedOrder() {
        return await new Promise(function(resolve, reject) {
            
            $.ajax({
                url: `/api/method/moneymaker.www.checkout.saved_order?package_name=${packageName}&session_id=${sessionId}&recurring_type=${recurringType}`,
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

    function monthMultiplier() {
        if(recurringType == "1") {
            return 1
        } else {
            return 12
        }
    }



    function paymentIntent(amount, itemName) {
        const items = [{
            name: itemName,
            amount: amount,
            description: "",
            quantity: 1
        }];
            
        $.ajax({
            url: '/api/method/paymob_integration.pay_api_live.intention',
            type: 'POST',
            contentType: 'application/json; charset=UTF-8',
            data: JSON.stringify({
                data: {
                    amount: amount,
                    items: items,
                    extras: {
                        action: "subscribe",
                        package_name: packageName,
                        payment_cycle: recurringType == "1"? "Monthly" : "Annual",
                        company_name: "Osus",
                        saved_order: savedOrderName,
                        coupon: coupon_code,
                    },
                    company_name: "Osus",
                },
                // notification_url: "https://webhook.site/aa7a88d7-3ecd-4d66-8a86-993f54826da1",
                // redirection_url: "https://www.google.com"
            }),
            success: function(response) {
                console.log(response.message)
                if (response && response.message.success) {
                    location.href = response.message.url;
                }
            },
            error: function(xhr, status, error) {
                alert("طلب الدفع فشل: " + error);
            }
        });
    }

    function applyCoupon() {
        coupon_code = couponField.value.trim()
        if(coupon_code === "") {
            alert("كود الخصم فارغ");
            return;
        }
        showLoader();
        $.ajax({
            url: '/api/method/moneymaker.www.checkout.apply_coupon',
            type: 'POST',
            contentType: 'application/json; charset=UTF-8',
            data: JSON.stringify({
                code: coupon_code,
            }),
            success: function(response) {
                const data = response.message;
                if(data.status == 200) {
                    discountAmount = discountedAmount(totalAmount, data);

                    if (discountAmount > 0) {
                        discountBlock.classList.remove("hidden");
                        oldDisplay.classList.remove("hidden");
                        discountDisplay.textContent = `كود الخصم (${(data.discount_percent)}%): -${discountAmount}`;
                        displayTotalAmount(totalAmount-discountAmount, totalAmount);
                    }
                    hideLoader();

                } else {
                    discountAmount = 0
                    discountBlock.classList.add("hidden");
                    oldDisplay.classList.add("hidden");
                    couponField.value = ""
                    coupon_code = null
                    displayTotalAmount(totalAmount);
                    hideLoader();
                    alert(data.error)
                }
                
            },
            error: function(xhr, status, error) {
                discountAmount = 0
                discountBlock.classList.add("hidden");
                oldDisplay.classList.add("hidden");
                couponField.value = ""
                coupon_code = null
                displayTotalAmount(totalAmount);
                alert("إجراء غير صحيح: " + error);
            }
        });
    }

    function discountedAmount(amount, data) {
        let _discountAmount = amount * (data.discount_percent/100)

        if (_discountAmount > data.maximum_discount) {
            return data.maximum_discount
        } else {
            return _discountAmount
        }
    }


    function getSessionID() {
        let sessionID = getCookie(recurringType == "1"? "order_session_monthly" : "order_session_annual");
        
        if (!sessionID) {
            sessionID = crypto.randomUUID();
            setCookie(recurringType == "1"? "order_session_monthly" : "order_session_annual", sessionID, 2);
        }
    
        return sessionID;
    }

    function getUrlParameter(name) {
        const params = new URLSearchParams(window.location.search);
        const value = params.get(name);
        return value;
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

    function hideLoader() {
        preLoader.style.display = "none";
    }

    function showLoader() {
        preLoader.style.display = "inline";
    }

    payCards.forEach((element) => {
        element.addEventListener("click", () => selectPaymentMethod(element));
    });
})