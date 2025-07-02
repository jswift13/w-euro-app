document.addEventListener('DOMContentLoaded', () => {
  const cards  = document.querySelectorAll('.match-card');
  const inputs = Array.from(document.querySelectorAll('.match-card input'));

  // Prevent clicks on the inputs from also triggering the card click listener
  inputs.forEach(input => {
    input.addEventListener('click', e => {
      e.stopPropagation();
    });
  });

  // Click anywhere on a card to focus its first enabled input
  cards.forEach(card => {
    card.addEventListener('click', () => {
      const firstInput = card.querySelector('input:not([disabled])');
      if (firstInput) firstInput.focus();
    });
  });

  // Enter jumps to next input, or blurs at the end
  inputs.forEach((inp, idx) => {
    inp.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const next = inputs[idx + 1];
        if (next) next.focus();
        else inp.blur();
      }
    });
  });

  // Strip non-digits as they type/paste
  document.querySelectorAll('input[inputmode="numeric"]').forEach(input => {
    input.addEventListener('input', () => {
      input.value = input.value.replace(/[^0-9]/g, '');
    });
  });
});
