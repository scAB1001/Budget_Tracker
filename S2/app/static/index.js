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

function editIncome(incomeId) {
    window.location.href = `/edit_income/${incomeId}`;
}
function editExpense(expenseId) {
    window.location.href = `/edit_expense/${expenseId}`;
}
function editGoal(goalId) {
    window.location.href = `/edit_goal/${goalId}`;
}

/*function loadWheel(progress_value) {
    var progress = progress_value; // Get the progress value from Flask

    // Calculate the rotation angle
    var rotationAngle = progress <= 50 ? progress * 3.6 : 180 - ((100 - progress) * 3.6);

    // Set the transform style for animation
    var rightCircle = document.getElementById('rightCircle');
    rightCircle.style.transform = `rotate(${rotationAngle}deg) translate(-100%, 0)`;

    // Add animation class
    rightCircle.classList.add('fill-animation');
}*/