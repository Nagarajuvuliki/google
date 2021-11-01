const contents = document.querySelector("main .container #contents");
const section = document.querySelector("main .container #contents section");
const continueButton = document.querySelector(
    "main .container  #contents .navigation button.continue"
);
const backButton = document.querySelector(
    "main .container  #contents .navigation button.back"
);

const handleScroll = (element, scrollWidth) => {
    element.scrollLeft = element.scrollLeft + scrollWidth;
    if (element.scrollLeft + element.clientWidth == element.scrollWidth) {
        continueButton.style.opacity = 0;
    } else if (element.scrollLeft == 0) {
        backButton.style.opacity = 0;
        backButton.style.display = "none";
    } else {
        continueButton.style.opacity = 1;
        backButton.style.opacity = 1;
        backButton.style.display = "inline-flex";
    }
};

continueButton.addEventListener("click", () => {
    handleScroll(section, section.clientWidth);
});

backButton.addEventListener("click", () => {
    handleScroll(section, section.clientWidth * -1);
});
