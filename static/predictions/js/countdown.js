document.addEventListener('DOMContentLoaded', () => {
  const el = document.getElementById('countdown');
  if (!el) return;

  const kickoff = new Date(el.dataset.kickoff);
  function update() {
    const now = new Date();
    const diff = kickoff - now;
    if (diff <= 0) {
      el.textContent = "Matchday started";
      clearInterval(timer);
      return;
    }
    const hrs = String(Math.floor(diff/3600000)).padStart(2,'0');
    const mins = String(Math.floor((diff%3600000)/60000)).padStart(2,'0');
    const secs = String(Math.floor((diff%60000)/1000)).padStart(2,'0');
    el.textContent = `Starts in ${hrs}:${mins}:${secs}`;
  }
  update();
  const timer = setInterval(update, 1000);
});
