let termButtons = document.querySelectorAll(".term-button:not(.toggle-all-button)")
let toggleAllButtons = document.querySelectorAll(".term-button.toggle-all-button")

for (let button of termButtons) {
    button.addEventListener("click", () => {
        button.classList.toggle("active")

        let domElement = document.getElementById(button.dataset.target)
        domElement.classList.toggle("active");
    })
}

for (let button of toggleAllButtons) {
    button.addEventListener("click", () => {
        button.classList.toggle("active")

        let definitionElement = document.getElementById(`definition-${button.dataset.target}`)
        let contextElement = document.getElementById(`context-${button.dataset.target}`)
        let commentElement = document.getElementById(`comment-${button.dataset.target}`)
        let synonymElement = document.getElementById(`connected-${button.dataset.target}`)
        definitionElement.classList.toggle("active");
        contextElement.classList.toggle("active");
        commentElement.classList.toggle("active");
        synonymElement.classList.toggle("active");
    })
}
