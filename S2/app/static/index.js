function deleteIncome(incomeId) {
  fetch("/delete_income", {
    method: "POST",
    body: JSON.stringify({ incomeId: incomeId }),
  }).then((_res) => {
    window.location.href = "/incomes";
  });
}
function deleteExpense(expenseId) {
  fetch("/delete_expense", {
    method: "POST",
    body: JSON.stringify({ expenseId: expenseId }),
  }).then((_res) => {
    window.location.href = "/expenses";
  });
}
function deleteGoal(goalId) {
  fetch("/delete_goal", {
    method: "POST",
    body: JSON.stringify({ goalId: goalId }),
  }).then((_res) => {
    window.location.href = "/goal";
  });
}

/* Edit an entry, nav to specific entryId */
function editIncome(incomeId) {
  window.location.href = `/edit_income/${incomeId}`;
}
function editExpense(expenseId) {
  window.location.href = `/edit_expense/${expenseId}`;
}
function editGoal(goalId) {
  window.location.href = `/edit_goal/${goalId}`;
}

function show(eId) {
  var x = document.getElementById(eId);
  x.style.display = "block";
}

function hide(eId) {
  var x = document.getElementById(eId);
  x.style.display = "none";
}

/* W3 schools progress bar animation */
function updateProgress(eId, value) {
  var i = 0;
  if (i == 0) {
    i = 1;
    var elem = document.getElementById(eId);
    var width = 0;
    var id = setInterval(frame, 12);
    
    function frame() {
      if (width >= value) {
        clearInterval(id);
        i = 0;
      } else {
        width++;
        elem.style.width = width + "%";
        elem.innerHTML = "You're " + width + "% of the way there!";
      }
    }

  }
}

/* W3 schools scroll indicator animation */
function indicateScroll(eId) {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;
  document.getElementById(eId).style.width = scrolled + "%";
}

