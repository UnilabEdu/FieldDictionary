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

let searchWord = document.getElementById("searchWord")
let searchLetter = document.getElementById("searchLetter")
let searchButton = document.getElementById("searchButton")
let searchButton2 = document.getElementById("searchButton2")
let sortType = document.getElementById("sortType")

function search() {
    let selectedCheckboxes = document.querySelectorAll("input:checked")
    let url = new URL(window.location.origin)
    if (searchWord.value != '') {
        url.searchParams.set("searchWord", searchWord.value)
    }

    if (searchLetter.value != '') {
        url.searchParams.set("searchLetter", searchLetter.value)
    }
    if (sortType.value != '') {
        url.searchParams.set("sortType", sortType.value)
    }

    let categories = ""
    for (let checkbox of selectedCheckboxes)
        categories += `${checkbox.dataset.category},`

    if (categories != '') {
        url.searchParams.set("categories", categories)
    }

    window.location.href = url
}

searchButton.addEventListener("click", search)
searchButton2.addEventListener("click", search)

let categoryRemoveButtons = document.getElementsByClassName("selected-filter-remove-button")
for (let button of categoryRemoveButtons) {
    button.addEventListener("click", () => {
        let url = decodeURIComponent(decodeURIComponent(window.location.href))
        let matchedString = new RegExp(`\\b${button.dataset.category}\\b,`,"g")
        url = url.replace(matchedString, "")
        window.location.href = url
    })
}