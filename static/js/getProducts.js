const category_input = document.querySelector(
    "main .container #contents section form .category input[name='category_input'] "
);
const product_datalist = document.querySelector(
    "main .container #contents section form .product datalist#product"
);

category_input.addEventListener("change", (e) => {
    fetch("http://localhost:5000/get-category-products", {
        method: "POST",
        credentials: "same-origin",
        headers: new Headers({
            "content-type": "application/json",
        }),
        body: JSON.stringify({ "category-name": e.target.value }),
    })
        .then((response) => response.json())
        .then((data) => {
            data.map((item) => {
                let option = document.createElement("option");
                option.value = item.name;
                option.innerHTML = item.name;
                product_datalist.appendChild(option);
            });
        });
});
