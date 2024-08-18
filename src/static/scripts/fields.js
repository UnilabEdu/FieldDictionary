const errorableFields = document.querySelectorAll('.errorable-field')

errorableFields.forEach((field) => {
  input = field.querySelector('input') ?? field.querySelector('textarea')

  input.addEventListener('blur', () => field.classList.add('touched'))

  input.addEventListener('keyup', (e) => {
    const error = field.querySelector('.email-error')
    if(!error) return;
    if (e.target.value.length === 0){
      error.textContent = "შეავსეთ ველი"
    }else{
      error.textContent = "მითიტებული ელ.ფოსტა არასწორია"
    }
  })
})

