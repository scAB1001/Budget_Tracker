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

function editIncome(incomeId) {
    window.location.href = `/edit_income/${incomeId}`;
}
function editExpense(expenseId) {
    window.location.href = `/edit_expense/${expenseId}`;
}