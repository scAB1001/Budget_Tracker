/* Delete all entries by sending a POST req, nav to entry type */
function deleteAllEntries(entry_type) {
  fetch(`/delete_all_${entry_type}s`, {
    method: "POST",
  }).then((_res) => {
    window.location.href = `/${entry_type}s`;
  });
}

/* Delete an entry by sending a POST req of the id, nav to entry type */
function deleteEntry(entry_type, entryId) {
  fetch(`/delete_${entry_type}`, {
    method: "POST",
    body: JSON.stringify({ entryId: entryId }),
  }).then((_res) => {
    window.location.href = `/${entry_type}s`;
  });
}

/* Edit an entry, nav to specific entryId */
function editEntry(entry_type, entryId) {
  window.location.href = `/edit_${entry_type}/${entryId}`;
}

/* Toggle show/hide elements */
function show(eId) {
  var x = document.getElementById(eId);
  x.style.display = "block";
}

function hide(eId) {
  var x = document.getElementById(eId);
  x.style.display = "none";
}

// Swipe functionality
function initializeSwipe() {
    let startX;

    document.querySelectorAll('.swiper-card').forEach(card => {
        card.addEventListener('mousedown', (e) => {
            startX = e.clientX;
            e.preventDefault();
        });

        card.addEventListener('mouseup', (e) => {
            if (startX - e.clientX > 150) { // Swiped left
                card.style.transform = 'translateX(-100%)';
            } else if (startX - e.clientX < -150) { // Swiped right
                card.style.transform = 'translateX(100%)';
            }
            e.preventDefault();
        });
    });
}

// Initialize the swipe functionality
initializeSwipe();

