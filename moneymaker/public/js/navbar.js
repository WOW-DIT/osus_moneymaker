frappe.ready(() => {
   //let img = document.createElement("i");
    //img.classList.add('fa','fa-map-marker-alt' , 'me-3');
    footerInfo();
    footerNews();

 })
 
 function footerInfo(){
    frappe.call({
       method: "moneymaker.www.index.getWebContent",
       callback: function (r) {
               if (r.message) {
                document.getElementById('navbar-img').setAttribute("src",r.message.logo_image);
                   document.getElementById('footer-address').innerHTML = r.message.address;
                   document.getElementById('footer-phone').innerHTML = r.message.tel;
                   document.getElementById('website_name').innerHTML = r.message.website_name;
                   document.getElementById('website_name2').innerHTML = r.message.website_name;
                   document.getElementById('footer-envelope').innerHTML = r.message.email;
                   document.getElementById('footer-twitter').setAttribute("href",r.message.twitter);
                   document.getElementById('footer-facebook').setAttribute("href",r.message.facebook);
                   document.getElementById('footer-youtube').setAttribute("href",r.message.youtube);
                   document.getElementById('footer-instagram').setAttribute("href",r.message.instgram);
                   document.getElementById('footer-linkedin').setAttribute("href",r.message.linkedin);
                   document.getElementById('years').innerHTML=new Date().getFullYear();
               }
       },
    });
 }
 function footerNews(){
   frappe.call({
      method: "moneymaker.www.index.getNews",
      callback: function (r) {
              if (r.message) {
                  let news = document.getElementById('footer-news');
                  for(const _new of r.message){
                     const li = document.createElement('li');
                     li.innerHTML = _new.message
                     news.appendChild(li);
                  }
              }
      },
   });
}