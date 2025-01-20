const dialogs = document.querySelectorAll('dialog')
 const filterModal = document.querySelector('#filter-content-backdrop')
const showButton = document.querySelector('#filter-modal-open-button')
const closeButton = document.querySelector('#filter-modal-close-button')

function toggleFilterModal() {
  filterModal.classList.toggle('open')
}

// "Show the dialog" button opens the dialog modally
showButton?.addEventListener('click', toggleFilterModal)

// "Close" button closes the dialog
closeButton?.addEventListener('click', toggleFilterModal)

filterModal?.addEventListener('mousedown', (e) => {
  if (e.target === filterModal) {
    toggleFilterModal()
  }
})

dialogs.forEach((dialog) =>
  dialog.addEventListener('mousedown', (event) => {
    if (event.target === dialog) {
      dialog.close()
    }
  })
)

const contactForm = document.querySelector('#contact-form')
const successDialogContact = document.querySelector('#success-modal-contact')
const errorDialogContact = document.querySelector('#error-modal-contact')
const errorDialogCloseButtonContact = document.querySelector('#error-modal-close-button-contact')
let didSubmitContact = false

contactForm?.addEventListener('submit', (e) => {
  e.preventDefault();
  didSubmitContact = true

  const formData = new FormData(document.getElementById("contact-form"));
  fetch('/send_email', { method: 'POST', body: formData })
      .then(response => {
          if (response.status === 200) {
              successDialogContact.showModal()
          }
          else
          {
              errorDialogContact.showModal();
          }
      })
})

// const contactButton = contactForm?.querySelector('button')
// contactButton?.addEventListener('mousedown', () => {
//   didSubmitContact = false
//   setTimeout(() => {
//     if (didSubmitContact) {
//       successDialogContact.showModal()
//     } else {
//       errorDialogContact.showModal()
//     }
//   }, 200)
// })

errorDialogCloseButtonContact?.addEventListener('click', () => {
  errorDialogContact.close()
})
