


// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=NEW CODE-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
const institution = document.body.getAttribute('data-inst');
const brand_name = document.body.getAttribute('data-brand');

var continer=document.getElementById("pills-tabContent");
const baseUrl = "https://osus.wowdigital.sa"

const viewElements = document.querySelectorAll('.view-element');

if(window.top === window.self){
    console.log("AAAAAAAAAAAAAAAAAAAAAA");
} else {
    viewElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            const field = element.getAttribute("data-element-field")
            // element.style.padding = '2px';
            element.style.backgroundColor = "rgba(222,222,222,1)";
            element.style.border = '3px solid red';
            window.parent.postMessage({"field": field}, '*');
        });

        element.addEventListener('mouseleave', () => {
            // element.style.padding = '0px';
            element.style.border = 'none';
            element.style.backgroundColor = "transparent";
        });
    });
}




getCategories();

function getCategories() {
    fetch(baseUrl+`/api/method/moneymaker.www.${brand_name}.index.getCategories?institution=${institution}`)
    .then(response => response.json())
    .then(data => {
        let categories = []
        for(let c of data.message) {
            categories.push(c.category);
        }
        data.message.map((element, index) => {
            createCourseBoxes(element, index, categories)

            // getCourses(element, index, categories)
        })
    })
    .catch(error => {
        // Handle errors
    });
}

function createCourseBoxes(element, index, cats) {
    const urlParams = new URLSearchParams(window.location.search);
    const selectedCategory = urlParams.get("category");

    var tab=document.createElement("DIV");
    tab.id=element.category
    
    if(selectedCategory === null || !cats.includes(selectedCategory)) {
        if (index === 0) {
            tab.className="tab-pane fade show active"
            var courses_box=document.createElement("DIV");
            courses_box.className="courses-box";
            tab.appendChild(courses_box);
            continer.appendChild(tab);

            getCourses(element.category)
        } else{
            tab.className="tab-pane fade"
            var courses_box=document.createElement("DIV");
            courses_box.className="courses-box";
            tab.appendChild(courses_box);
            continer.appendChild(tab);
        }
        
    } else {
        if(selectedCategory === element.category) {
            tab.className="tab-pane fade show active"
            var courses_box=document.createElement("DIV");
            courses_box.className="courses-box";
            tab.appendChild(courses_box);
            continer.appendChild(tab);

            getCourses(element.category)
        } else{
            tab.className="tab-pane fade"
            var courses_box=document.createElement("DIV");
            courses_box.className="courses-box";
            tab.appendChild(courses_box);
            continer.appendChild(tab);
        }
    }
    
}

function getCourses(category) {
    // const urlParams = new URLSearchParams(window.location.search);
    // const selectedCategory = urlParams.get("category");
    let path = `/api/method/moneymaker.www.${brand_name}.index.getCourses?institution=${institution}&category=${category}`
    console.log(`${baseUrl}${path}`)
    fetch(`${baseUrl}${path}`)
    .then(response => response.json())
    .then(r => {
        if (r.message && r.message.length>0) {
            const courses_box = document.getElementById(category).querySelector(".courses-box")
            courses_box.innerHTML = ""
            
            var row=document.createElement("DIV");
            row.className="row"
            row.id="row-"+category
            row.setAttribute("data-page",1);
            row.innerHTML = r.message.map(item => `
                <div class="col-lg-4">
                    <a href="Osus/course_det?id=${item.name}" class="item">
                        <div class="img">
                            <img src="${item.hero_image}" alt="" class="img-cover">
                        </div>
                        <div class="info">
                            <h5 class="title"> ${item.name} </h5>
                            <div class="text"> ${item.description} </div>
                            <div class="rate">
                                <div class="stars">
                                    ${Array(item.full_stars).fill('<i class="fas fa-star"></i>').join('')}${item.half_star ? '<i class="fas fa-star-half-alt"></i>' : ''}${Array(item.total_stars - (item.full_stars + (item.half_star ? 1 : 0))).fill('<i class="far fa-star"></i>').join('')}
                                </div>
                                <small class="str-num"> (${item.rate_count}) </small>
                            </div>
                            <div class="price">
                                <h4> <span class="prc"> ${item.price} </span> <small> SAR </small> </h4>
                                ${item.priceold != item.price ? `<h4 class="old-prc"> <span class="prc"> ${item.priceold} </span> <small> SAR </small> </h4>` : ''}
                            </div>
                        </div>
                    </a>
                </div>
            `).join('');
            courses_box.appendChild(row);
        }
    })
    .catch(error => {
        // Handle errors
    });
}

var btns =document.getElementsByClassName("btn-more-evt");
var btn_more=document.getElementById('btn_more');
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener('click', function() {
        // Get the data-value attribute of the clicked element
        var curr_category=this.getAttribute('data-bs-target').substring(1);

        
        btn_more.setAttribute('data-category',curr_category);
        getCourses(curr_category)
        // console.log(curr_category);
    });
}


btn_more.addEventListener('click', function(e) {
    var _category=this.getAttribute('data-category')
    
    var row=document.getElementById("row-"+_category)

    var page=Math.round(row.getAttribute("data-page"));

    page=page+1;

    fetch(baseUrl+`/api/method/moneymaker.www.${brand_name}.index.getCourses?institution=${institution}&category=${_category}&page=${page}`)
    .then(response => response.json())
    .then(r => {
        if (r.message && r.message.length>0) {
        
            for (let item of r.message) {
                // debugger
                row.innerHTML += `<div class="col-lg-4">
                    <a href="Osus/course_det?id=${item.name}" class="item">
                        <div class="img">
                            <img src="${item.hero_image}" alt="" class="img-cover">
                        </div>
                        <div class="info">
                            <h5 class="title"> ${item.name} </h5>
                            <div class="text"> ${item.description} </div>
                            <div class="rate">
                                <div class="stars">
                                    ${Array(item.full_stars).fill('<i class="fas fa-star"></i>').join('')}${item.half_star ? '<i class="fas fa-star-half-alt"></i>' : ''}${Array(item.total_stars - (item.full_stars + (item.half_star ? 1 : 0))).fill('<i class="far fa-star"></i>').join('')}
                                </div>
                                <small class="str-num"> (${item.rate_count}) </small>
                            </div>
                            <div class="price">
                                <h4> <span class="prc"> ${item.price} </span> <small> SAR </small> </h4>
                                ${item.priceold != item.price ? `<h4 class="old-prc"> <span class="prc"> ${item.priceold} </span> <small> SAR </small> </h4>` : ''}
                            </div>
                        </div>
                    </a>
                </div>`;
            }

            row.setAttribute("data-page",page)
        }
    })
    .catch(error => {
        // Handle errors
    });
});

