
  document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('.toggle-button');

    toggleButtons.forEach(button => {
      button.addEventListener('click', () => {
        const targetId = button.getAttribute('data-target');
        const targetElement = document.getElementById(targetId);
        const downArrowUrl = button.getAttribute('data-down-arrow-url');

        if (targetElement) {
          targetElement.classList.toggle('hidden');
          
          // Toggle arrow direction
          const img = button.querySelector('img');
          if (targetElement.classList.contains('hidden')) {
            img.src = downArrowUrl;
          } else {
            img.src = downArrowUrl;
          }
        }
      });
    });
  });




