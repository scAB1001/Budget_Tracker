function deleteExpense(expenseId) {
        fetch("/delete-expense", {
          method: "POST",
          body: JSON.stringify({ expenseId: expenseId }),
        }).then((_res) => {
          window.location.href = "/expenses"; // Redirect to wherever you want after deletion
        });
      }

function editExpense(expenseId) {
    window.location.href = `/edit-expense/${expenseId}`;
}