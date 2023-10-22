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

