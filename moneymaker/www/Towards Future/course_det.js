document.addEventListener("DOMContentLoaded", function(e){
    const purchaseBtn = document.getElementById("purchase-btn")
    if(purchaseBtn) {
        purchaseBtn.onclick = intent
    }
})

function intent() {
    debugger

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const course_id = urlParams.get("id")

    const priceEle = document.getElementById("price-tag")
    const companyName = document.body.getAttribute("data-company")
    let total_amount = 0
    
    if (priceEle != null) {
        total_amount = parseFloat(priceEle.innerText)
    }
    const items = [
        {
            name: course_id,
            amount: total_amount,
            description: "",
            quantity: 1
        }
    ]

    fetch('/api/method/paymob_integration.pay_api_live.intention', {
        method: 'POST',
        body: JSON.stringify({data: {
            amount: total_amount,
            items: items,
            extras: {
                action: "buy_course",
                course: course_id,
                company_name: companyName
            },
            company_name: companyName,
        }}),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      }).then((response) => response.json())
        .then((json) => {
            console.log(json)
            if(json.message && json.message.success)
            {
                location.href = json.message.url
            }
        });
}

function validateTime(frm) {
	const now = new Date();
	const startTime = new Date(`${frm.doc.schedule_date} ${frm.doc.from_time}`);
	const endTime = new Date(`${frm.doc.schedule_date} ${frm.doc.to_time}`);
	
	return now >= startTime && now <= endTime
}

async function joinMeeting(doc) {
	const domain = "https://osus.wowdigital.sa"
	const apiToken = "";
    try {
        var meeting_room = await frappe.db.get_doc("Meeting Room", doc.meeting)
        var response = await login(doc)
        if(response.message) {
            var data = response.message.data;
            
            if(data.success == 200) {
				let params = [
                    data.userName,
                    data.Email,
                    data.userimg,
                    data.Account,
                    // apiToken,
                ];
                var pram_string = params.join("Qva5rm");
                // var pram_string=data.userName + "Qva5rm"+data.Email + "Qva5rm"+data.userimg + "Qva5rm"+data.Account;
                var pram=encodeURIComponent(pram_string);
                return `https://meeting.wowdigital.sa/meet/${meeting_room.room_id}?docname=${doc.name}&doctype=${doc.doctype}&domain=${domain}` + "?q=" + pram, "_blank"
            } else {
                return `https://meeting.wowdigital.sa/?room=${meeting_room.room_code}&doctype=${doc.doctype}&docname=${doc.name}&domain=${domain}`
            }
        } else {
			return `https://meeting.wowdigital.sa/?room=${meeting_room.room_code}&doctype=${doc.doctype}&docname=${doc.name}&domain=${domain}`
        }
    } catch(e) {
        frappe.throw(e.toString())
    }
}

async function login(doc) {
    // var meeting_room = await frappe.db.get_doc("Meeting Room", doc.meeting)
    var r = await frappe.call({
        method: 'meeting.wow_meeting.doctype.meeting_room.meeting_room.meetingLogin',
        args: {
            // Pass any arguments required by the method
            user: frappe.session.user
        },
    });
    return r
}