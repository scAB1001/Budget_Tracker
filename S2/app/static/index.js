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

// Example using Chart.js
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: '# of Votes',
      data: [12, 19, 3, 5, 2, 3],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

// Example using a wheel library (e.g., Winwheel.js)
var winwheel = new Winwheel({
  numSegments: 6,
  segments: [
    { fillStyle: '#eae56f', text: 'Prize 1' },
    { fillStyle: '#89f26e', text: 'Prize 2' },
    { fillStyle: '#7de6ef', text: 'Prize 3' },
    { fillStyle: '#e7706f', text: 'Prize 4' },
    { fillStyle: '#eae56f', text: 'Prize 5' },
    { fillStyle: '#89f26e', text: 'Prize 6' }
  ]
});
