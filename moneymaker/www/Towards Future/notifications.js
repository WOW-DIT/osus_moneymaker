function markAsRead(e) {
    const docname = e.getAttribute("data-name");
    console.log(docname)
    $.ajax({
        method: 'POST',
        url: '/api/method/moneymaker.www.api.notifications.mark_as_read',
        data: JSON.stringify({
            docname: docname,
        }),
        success: function(response) {
            if(response.message && response.message.status == 200) {
                e.classList.remove("item_active")
            }
        },
        error: function(xhr) {
            // hideLoader();
        }
    });
}