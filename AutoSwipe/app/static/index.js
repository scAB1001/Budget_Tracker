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
