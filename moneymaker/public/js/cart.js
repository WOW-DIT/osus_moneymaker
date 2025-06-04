
let removeBtns = document.querySelectorAll(".remove-cart");
const container = document.getElementById("container");
const cart_form = document.getElementById("cart-form");
const cart_container = document.getElementById("cart-container");
const empty_container = document.getElementById("cart-empty");
const amount_el = document.getElementById("amount");
const vat_el = document.getElementById("vat");
const grand_total_el = document.getElementById("grand-total");

let amount = 0.0
let vat = 0.0
let grand_total = 0.0

document.addEventListener("DOMContentLoaded", ()=>{
    console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    listenToRemove()

    const payment_btn = document.getElementById("payment-button");
    payment_btn.addEventListener("click", (e)=>{
        paymentIntent();
    })
})

function paymentIntent() {
    amount = parseFloat(amount_el.innerText.split(" ")[0])
    vat = parseFloat(vat_el.innerText.split("+")[1].split(" ")[0])
    grand_total = parseFloat(grand_total_el.innerText.split(" ")[0])
    console.log(amount)
    console.log(vat)
    console.log(grand_total)

    const item = {
        name: "Course 1",
        amount: grand_total,
        description: "AAAAA",
        quantity: 1,
    }
    
    frappe.call({
        "type": "POST",
        "method": "paymob_integration.pay_api_live.intention",
        // "headers": {
        //     "Content-Type": "application/json",
        // },
        args:{
            "data": {
                "amount": grand_total,
                "item": item,
                "extras": {
                    "action": "subscribe",
                    "package_name": "B-E-M",
                    "payment_cycle": "Annual",
                }
            }
        }
    });

    // try{$.ajax(settings).done(function (response) {
    //     console.log(response)
    //     if(response.message) {
    //     }
    // });}
    // catch(e) {
    //     console.log(e)
    // }
}


function listenToRemove() {
    removeBtns.forEach((btn)=>{
        btn.addEventListener("click", removeItem)
    })
}

function removeItem(e) {
    const btn = e.target;
    const item_id = btn.getAttribute("data-item")
    console.log(item_id)
    var settings = {
        "url": `https://Osus.wowdigital.sa/api/method/moneymaker.www.user.cart.deleteItem?item_id=${item_id}`,
        "method": "GET",
        // "headers": {
        //     "Content-Type": "application/json",
        // },
        // "data": JSON.stringify({
        //     item_id: item_id
        // }),
    };

    try{$.ajax(settings).done(function (response) {
        if(response.message) {
            updateCart(response.message);
        }
    });}
    catch(e) {
        console.log(e)
    }
    
}

function updateCart(cart) {
    const items = cart.items;
    console.log(items)
    if(items.length == 0) {
        cart_form.style.display = "none";
        empty_container.style.display = "inline";
    } else {
        let cart_html = `
            <div class="cart-count-text wow bounceInUp faster" style="visibility: visible; animation-name: bounceInUp;"><b>${items.length}</b> عناصر
                في السلة
            </div>            
        `;

        for(let item of items) {
            cart_html += `
                <div class="cart-item wow bounceInUp faster" style="visibility: visible; animation-name: bounceInUp;">
                    <div class="cart-item-img">
                        <a href="">
                            <img src="${item.image}">
                        </a>
                    </div>
                    <div class="cart-item-details">
                        <a href="">
                            <h3>
                                ${item.item_name}
                                <div class="price">
                                    <span>${item.price} ر.س  (${item.qty})</span>
                                </div>
                            </h3>
                        </a>
                    </div>
                    <button type="button" class="remove-cart delete" data-item="${item.item}" data-text="هل أنت متأكد من انك تريد إزالة باقة عصارة بلس من سلة المشتريات ؟">
                        <svg id="Combined_Shape" data-name="Combined Shape" xmlns="//www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 10 10">
                            <path id="Combined_Shape-2" data-name="Combined Shape" d="M8.781,9.791,5,6.01,1.219,9.791A.714.714,0,0,1,.209,8.781L3.99,5,.209,1.219A.715.715,0,0,1,1.219.209L5,3.99,8.781.209a.714.714,0,0,1,1.01,1.011L6.01,5,9.791,8.781a.714.714,0,1,1-1.01,1.01Z"></path>
                        </svg>
                    </button>
                </div>
            `;
        }


        cart_container.innerHTML = cart_html;

        amount_el.innerText = `${cart.total_amount} ر.س`
        vat_el.innerText = `+${Math.ceil(cart.vat * 10) / 10} ر.س`
        grand_total_el.innerText = `${cart.grand_total} ر.س`
    }
}