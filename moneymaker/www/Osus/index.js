


// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=NEW CODE-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
document.addEventListener("DOMContentLoaded", function () {
    const institution = document.body.getAttribute('data-inst');
    const brand_name = document.body.getAttribute('data-brand');
    const riyalSymbol = "/files/riyal_symbol.svg";
    

    var container=document.getElementById("pills-tabContent");

    const viewElements = document.querySelectorAll('.view-element');

    if(window.top === window.self){
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
        fetch(`/api/method/moneymaker.www.${brand_name}.index.getCategories?institution=${institution}`)
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
                container.appendChild(tab);

                getCourses(element.category)
            } else{
                tab.className="tab-pane fade"
                var courses_box=document.createElement("DIV");
                courses_box.className="courses-box";
                tab.appendChild(courses_box);
                container.appendChild(tab);
            }
            
        } else {
            if(selectedCategory === element.category) {
                tab.className="tab-pane fade show active"
                var courses_box=document.createElement("DIV");
                courses_box.className="courses-box";
                tab.appendChild(courses_box);
                container.appendChild(tab);

                getCourses(element.category)
            } else{
                tab.className="tab-pane fade"
                var courses_box=document.createElement("DIV");
                courses_box.className="courses-box";
                tab.appendChild(courses_box);
                container.appendChild(tab);
            }
        }
        
    }

    function getCourses(category) {
        // const urlParams = new URLSearchParams(window.location.search);
        // const selectedCategory = urlParams.get("category");
        let path = `/api/method/moneymaker.www.${brand_name}.index.getCourses?institution=${institution}&category=${category}`
        console.log(`${path}`)
        fetch(path)
        .then(response => response.json())
        .then(r => {
            if (r.message && r.message.length>0) {
                const courses_box = document.getElementById(category).querySelector(".courses-box")
                courses_box.innerHTML = ""
                var row=document.createElement("DIV");
                row.className="row"
                row.id="row-"+category
                row.setAttribute("data-page",1);
                row.innerHTML = r.message.map(item => itemBlock(item, category)).join('');
                courses_box.appendChild(row);
            }
        })
        .catch(error => {
            // Handle errors
        });
    }

    function itemBlock(item, category) {
        return `
        <div class="col-lg-4">
            <a href="Osus/course_detail?id=${item.course_name}">
                <div class="course_card">
                    <div class="img_box">
                        <img src="${item.hero_image}" class="secImg" alt="" />
                        <img src="${item.hero_image}" class="secImg" alt="" />
                        <div class="overlay"></div>
                    </div>
                    <div class="card-body">
                        <p class="categ readable">${category}</p>
                        <h4 class="title readable"> ${item.course_name_ar} </h4>
                        <div class="p readable">
                            ${item.description_ar}
                        </div>

                        <div class="price_row">
                            <div class="price readable">
                                <span> ${item.price} <small> <img class="riyal_symbol" src="${riyalSymbol}"> </small> </span>
                                ${item.priceold != item.price ? `<span class="old_prc"> ${item.priceold} <small> <img class="riyal_symbol" src="${riyalSymbol}"> </small> </span>` : ''}
                            </div>
                            <div class="stars">
                                <span class="star"> <i class="fas fa-star me-1"></i> </span>
                                <span> ${item.rate_count} </span>
                            </div>
                        </div>

                    </div>
                </div>
            </a>
        </div>
    `
    }

    const btns =document.querySelectorAll(".btn-more-evt");
    const btn_more=document.getElementById('btn_more');
    for (var i = 0; i < btns.length; i++) {
        const currentTab = btns[i];
        currentTab.addEventListener('click', function(e) {
            // Get the data-value attribute of the clicked element
            var curr_category=this.getAttribute('data-bs-target').substring(1);

            
            btn_more.setAttribute('data-category',curr_category);
            
            getCourses(curr_category)
            // console.log(curr_category);
            // debugger
            const targetId = this.getAttribute('data-bs-target').replace('#', '');

            const tabContents = document.querySelectorAll('.tab-pane');

            btns.forEach(tab => {
                tab.classList.remove("active")
            })

            e.currentTarget.classList.add("active")

            // Hide all tab content containers
            tabContents.forEach(content => {
                content.classList.remove('show', 'active');
                content.classList.add('hidden');
            });

            // Show the selected one
            const selectedTab = document.getElementById(targetId);
            if (selectedTab) {
                selectedTab.classList.add('show', 'active');
                selectedTab.classList.remove('hidden');
            }
        });
    }


    btn_more.addEventListener('click', function(e) {
        var _category=this.getAttribute('data-category')
        
        var row=document.getElementById("row-"+_category)

        var page=Math.round(row.getAttribute("data-page"));

        page=page+1;

        fetch(`/api/method/moneymaker.www.${brand_name}.index.getCourses?institution=${institution}&category=${_category}&page=${page}`)
        .then(response => response.json())
        .then(r => {
            if (r.message && r.message.length>0) {
            
                for (let item of r.message) {
                    // debugger
                    row.innerHTML += itemBlock(item, _category);
                }

                row.setAttribute("data-page",page)
            }
        })
        .catch(error => {
            // Handle errors
        });
    });
});