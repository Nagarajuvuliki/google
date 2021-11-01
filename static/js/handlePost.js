const questionnaireForm = document.querySelector(
    "main .container #contents section form"
);

questionnaireForm.addEventListener("submit", (e) => {
    e.preventDefault();
    let {
        platform_input,
        category_input,
        region_input,
        product_input,
        brand_input,
        level_satisfaction,
        interested_input,
        email_input,
    } = e.target;
    let bodyData = {
        platform_input: platform_input.value,
        category_input: category_input.value,
        region_input: region_input.value,
        product_input: product_input.value,
        brand_input: brand_input.value,
        level_satisfaction: level_satisfaction.value,
        interested_input: interested_input.value,
        email_input: email_input.value,
    };
    fetch(e.target.action, {
        method: "POST",
        credentials: "include",
        headers: new Headers({
            "content-type": "application/json",
        }),
        body: JSON.stringify(bodyData),
    })
        .then((response) => response.json())
        .then((data) => {
            var h3Tag = document.createElement("h3");
            h3Tag.innerHTML = data.message;
            contents.appendChild(h3Tag);
        })
        .catch((error) => console.log(error));
});
