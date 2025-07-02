document.addEventListener('DOMContentLoaded', () => {
  const teamSel   = document.getElementById('id_potm_team');
  const playerSel = document.getElementById('id_potm');

  if (!teamSel || !playerSel) return;

  // cache all original options
  const allOptions = Array.from(playerSel.options).map(opt => ({
    value: opt.value,
    text:  opt.text,
    team:  opt.getAttribute('data-team')  // we’ll add this attribute below
  }));

  // add data-team attributes to each <option>
  allOptions.forEach((o, i) => {
    if (playerSel.options[i]) {
      playerSel.options[i].setAttribute('data-team', o.team);
    }
  });

  function filterPlayers() {
    const selectedTeam = teamSel.value;
    // rebuild the player select
    playerSel.innerHTML = '';
    // add a blank placeholder
    const blank = document.createElement('option');
    blank.value = '';
    blank.text  = 'Select a Player';
    playerSel.appendChild(blank);

    allOptions.forEach(o => {
      if (!selectedTeam || o.team === selectedTeam) {
        const opt = document.createElement('option');
        opt.value = o.value;
        opt.text  = o.text;
        playerSel.appendChild(opt);
      }
    });
  }

  // on change, re-filter and reset
  teamSel.addEventListener('change', filterPlayers);

  // initial filter (in case form is re-rendered with data)
  filterPlayers();
});
