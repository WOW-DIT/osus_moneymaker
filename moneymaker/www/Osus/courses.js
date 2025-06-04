document.addEventListener("DOMContentLoaded", function () {
    // Get the search input element

    const searchInput = document.getElementById("big-search-input");
    const searchForm = document.getElementById("advanced-search-form");
    const searchBtn = document.getElementById("advanced-search-btn");
    const categorySelect = document.querySelectorAll(".category-check");
    const orderSelect = document.getElementById("order-select");
    const coursesCount = document.getElementById("courses-count");
    const pagination = document.querySelector(".pagination");
    console.log(pagination)
    const preLoader = document.getElementById("preloader");
    hideLoader();

    let orderBy = null;
    let instructor = null;
    let page = 1;

    const selectedCategories = [];

    // Function to get URL parameters
    
    // Set the search input value if "q" exists in the URL
    let searchQuery = getQueryParam("q");
    if (searchQuery) {
      searchInput.value = searchQuery;
      filterCourses();
    }

    categorySelect.forEach((e) => {
      e.addEventListener("change", function (event) {

        const categoryName = event.target.value
        if(event.target.checked) {
          selectedCategories.push(categoryName)
        } else {
          selectedCategories.pop(categoryName)
        }
      });
    })

    $(orderSelect).on("change", (e) => {
      const orderValue = e.target.value;
      
      orderBy = orderValue? orderValue : null
    })


    // newestRad.addEventListener("change", function (event) {
    //   if(event.target.checked) {
    //     order = "DESC"
    //   }
    // });

    // oldestRad.addEventListener("change", function (event) {
    //   if(event.target.checked) {
    //     order = "ASC"
    //   }
    // });

    // instructorInput.addEventListener("input", function (event) {
    //   if(event.target.value === "") {
    //       instructor = null
    //   } else {
    //       instructor = event.target.value
    //   }
    // });
    
    // Prevent form submission from redirecting
    searchForm.addEventListener("submit", function (event) {
      event.preventDefault();

      filterCourses();
      if(searchInput.value !== "") {
      }
    });

    searchBtn.onclick = (event) => {
      searchForm.requestSubmit();
    }

    function getQueryParam(param) {
        let urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    function filterCourses(resetPage=true) {
      if (resetPage) {
        page = 1
      }
      
      showLoader();

      const body = document.body;
      const institution = body.getAttribute("data-inst");

      fetch(
          `/api/method/moneymaker.www.api.courses.getCourses`,
          {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
              "institution": institution,
              "name": searchInput.value,
              "categories": selectedCategories,
              "instructor": instructor,
              "order_by": orderBy,
              "page": page,
            }),
          }
        )
          .then(response => response.json())
          .then(r => {

            if (r.message) {
              const courses = r.message.courses;
              const numberOfPages = r.message.number_of_pages;
              const coursesLength = r.message.number_of_courses;

              const courses_box = document.getElementById("courses-box")
              courses_box.innerHTML = ""

              var row=document.createElement("DIV");
              row.className="row"

              row.innerHTML = courses.map(item => `
                <div class="col-lg-4">
                    <a href="course_detail?id=${item.course_name}">
                        <div class="course_card">
                            <div class="img_box">
                                <img src="${item.hero_image}" class="secImg" alt="" />
                                <img src="${item.hero_image}" class="secImg" alt="" />
                                <div class="overlay"></div>
                            </div>
                            <div class="card-body">
                                <p class="categ">${item.category}</p>
                                <h4 class="title"> ${item.course_name} </h4>
                                <div class="p">
                                  ${item.description}
                                </div>

                                <div class="price_row">
                                    <div class="price">
                                        <span>
                                        ${item.price}
                                          <small>
                                            <img src="/files/riyal_symbol.svg" class="riyal_symbol"/>
                                          </small>
                                        </span>
                                        <span class="old_prc">
                                          ${item.priceold}
                                          <small>
                                            <img src="/files/riyal_symbol.svg" class="riyal_symbol"/>
                                          </small>
                                        </span>
                                    </div>
                                    <div class="stars">
                                        <span class="star"> <i class="fas fa-star me-1"></i> </span>
                                        <span> ${item.average_rating} </span>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </a>
                </div>
                  
              `).join('');
              courses_box.appendChild(row);
              coursesCount.textContent = `(${coursesLength})`
              getPages(numberOfPages);
            }
            hideLoader();
          })
          .catch(error => {
              console.log(error);
              hideLoader();
          });
    }

    function getPages(numberOfPages) {
      pagination.innerHTML = "";

      let pagesString = `
        <li class="page-item">
            <a class="page-link" href="#" aria-label="Previous">
                <span aria-hidden="true">«</span>
            </a>
        </li>
        <li class="page-item"><button type="button" class="page-link page-number-btn">1</button></li>
      `;
      for (let i = 2; i <= numberOfPages; i++) {
        pagesString += `<li class="page-item"><button type="button" class="page-link page-number-btn">${i}</button></li>`;
      }
      pagesString += `
        <li class="page-item">
            <a class="page-link" href="#" aria-label="Next">
                <span aria-hidden="true">»</span>
            </a>
        </li>
      `;

      pagination.innerHTML = pagesString

      const pageNumbers = pagination.querySelectorAll(".page-number-btn");

      pageNumbers.forEach((e) => {
        if (e.textContent.trim() == page.toString()) {
          e.classList.add("active")
        } else {
          e.classList.remove("active")
        }
        e.addEventListener("click", (btn) => {
          page = parseInt(btn.target.textContent.trim())
          filterCourses(false)
        });
      });

    }

    function hideLoader() {
      preLoader.style.display = "none";
    }
  
    function showLoader() {
      preLoader.style.display = "inline";
    }
});