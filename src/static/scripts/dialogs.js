const dialogs = document.querySelectorAll('dialog')
const filterDialog = document.querySelector('#filter-modal')
const showButton = document.querySelector('#filter-modal-open-button')
const closeButton = document.querySelector('#filter-modal-close-button')

// "Show the dialog" button opens the dialog modally
showButton?.addEventListener('click', () => {
  filterDialog.showModal()
})

// "Close" button closes the dialog
closeButton?.addEventListener('click', () => {
  filterDialog.close()
})

dialogs.forEach((dialog) =>
  dialog.addEventListener('mousedown', (event) => {
    if (event.target === dialog) {
      dialog.close()
    }
  })
)

const subscribeForm = document.querySelector('#subscribe-form')
const emailInput = subscribeForm.querySelector('input')
const successDialog = document.querySelector('#success-modal')
const errorDialog = document.querySelector('#error-modal')
const errorDialogCloseButton = document.querySelector(
  '#error-modal-close-button'
)

let submitStatus = "error"

subscribeForm.addEventListener('submit', (e) => {
  e.preventDefault()
  if(emailInput.value.length === 0){
    submitStatus = "empty"
  }else{
    submitStatus = "sent"
  }
})

const subscribeButton = subscribeForm.querySelector('button')
subscribeButton.addEventListener('click', () => {
  submitStatus = "error"
  setTimeout(() => {
    if (submitStatus === "sent") {
      successDialog.showModal()
    } else if (submitStatus === "error") {
      errorDialog.showModal()
    }else{
      emailInput.focus()
    }
  }, 200)
})

errorDialogCloseButton.addEventListener('click', () => {
  errorDialog.close()
})

const contactForm = document.querySelector('#contact-form')
const successDialogContact = document.querySelector('#success-modal-contact')
const errorDialogContact = document.querySelector('#error-modal-contact')
const errorDialogCloseButtonContact = document.querySelector(
  '#error-modal-close-button-contact'
)

let didSubmitContact = false

contactForm?.addEventListener('submit', (e) => {
  e.preventDefault()
  didSubmitContact = true
})

const contactButton = contactForm?.querySelector('button')
contactButton?.addEventListener('mousedown', () => {
  didSubmitContact = false
  setTimeout(() => {
    if (didSubmitContact) {
      successDialogContact.showModal()
    } else {
      errorDialogContact.showModal()
    }
  }, 200)
})

errorDialogCloseButtonContact?.addEventListener('click', () => {
  errorDialogContact.close()
})

