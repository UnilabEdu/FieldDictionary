let termButtons = document.querySelectorAll(".term-button:not(.toggle-all-button)")
let toggleAllButtons = document.querySelectorAll(".term-button.toggle-all-button")

for (let button of termButtons) {
    button.addEventListener("click", () => {
        button.classList.toggle("active")

        let domElement = document.getElementById(button.dataset.target)
        domElement.classList.toggle("active");

        let allButton = document.querySelector(`.term-button[data-target="${button.dataset.target.split("-")[1]}"]`)
        if (allButton.classList.contains("active")) {
            allButton.classList.remove("active")
        }
    })
}

for (let button of toggleAllButtons) {
    button.addEventListener("click", () => {
        let definitionElement = document.getElementById(`definition-${button.dataset.target}`)
        let contextElement = document.getElementById(`context-${button.dataset.target}`)
        let commentElement = document.getElementById(`comment-${button.dataset.target}`)
        let synonymElement = document.getElementById(`connected-${button.dataset.target}`)

        let definitionBtn = document.querySelector(`.term-button[data-target="definition-${button.dataset.target}"]`)
        let contextBtn = document.querySelector(`.term-button[data-target="context-${button.dataset.target}"]`)
        let commentBtn = document.querySelector(`.term-button[data-target="comment-${button.dataset.target}"]`)
        let synonymBtn = document.querySelector(`.term-button[data-target="connected-${button.dataset.target}"]`)

        if (button.classList.contains("active")) {
            definitionElement?.classList.remove("active");
            contextElement?.classList.remove("active");
            commentElement?.classList.remove("active");
            synonymElement?.classList.remove("active");

            definitionBtn.classList.remove("active");
            contextBtn.classList.remove("active");
            commentBtn.classList.remove("active");
            synonymBtn.classList.remove("active");

            button.classList.remove("active")
        }
        else
        {
            definitionElement?.classList.add("active");
            contextElement?.classList.add("active");
            commentElement?.classList.add("active");
            synonymElement?.classList.add("active");

            definitionBtn.classList.add("active");
            contextBtn.classList.add("active");
            commentBtn.classList.add("active");
            synonymBtn.classList.add("active");

            button.classList.add("active")
        }
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
