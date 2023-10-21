function deleteExpense(expenseId) {
  fetch("/delete_expense", {
    method: "POST",
    body: JSON.stringify({ expenseId: expenseId }),
  }).then((_res) => {
    window.location.href = "/expenses";
  });
}

function editExpense(expenseId) {
    window.location.href = `/edit_expense/${expenseId}`;
}