## 1. Assignment Guidance

You will create a simple budget tracker web application using Flask with a SQLAlchemy database. Users should be able to:

- Add incomes and expenditures 
- See a list of all incomes and a list of all expenditures
- Edit an income or expenditure
- See their total income and total expenditure
- Add a savings goal
- See their progress towards this goal
- Edit or delete their goal.

You are not expected to add a logic or authentication system.
You should ensure that you validate any data entered by the user, both client- and server-side where appropriate.

Your website should have a professional layout which is easy to navigate and complies with the WCAG standards for accessibility. 
You can use open source CSS libraries such as Bootstrap, but should not rely on them for all of your styling – add some additional CSS to make your site stand out. You must develop your layout yourself using HTML, CSS and JavaScript if appropriate. You cannot use any software or services to create your layout for you. All JavaScript and CSS should be in its own file(s) in the ‘static’ folder.

## 2. Assessment Tasks

### Homepage

The homepage should have some basic analytics:

- The total value of all expenditures
- The total value of all incomes
- The difference between those two values
- If they have a goal, their progress towards this goal

If there are no incomes/expenditures then an appropriate message should be shown instead.

### Incomes and Expenditures

You should create models to represent incomes and expenditures. You can do this with a single model, but it may make things more difficult for you- using two separate models is recommended. They should have:

- A unique name
- An amount

For example,
```python
Income(name=”June Salary”, amount=530.21)
```

To create a new income or expenditure, the user should be directed to a form which takes their inputs, validates them to ensure that sensible values have been used, and adds this data to the database. The user should be able to see a list of both incomes and expenditures, and should be able to edit or delete them.

### Goals
The user should be able to create a single savings goal. This should have:

- A name (optional)
- A value

Once the user has created their goal, they should be able to edit or delete it. They should be able to see their progress towards their current goal, based on the difference between their total incomes/expenditures.

## 3. General Guidance and Study Support
You should use the module website, accessed via Minerva, as your primary source for information. 

## 4. Assessment Criteria and Marking Process
Your submission will be marked based on:

- How much of the required functionality has been implemented
- The accessibility of your website
- The overall design and layout of your website
- The quality and readability of your code
- All work will be manually marked against the rubrics given in Section 7 below, and your feedback will be in the form of a marked up rubric and a short comment. 
- Feedback will be provided through Gradescope within 3 weeks of the final submission deadline.

Any copyrighted material should be referenced by comment in your code.

## 5. Submission Requirements
You should submit only the files required to run your website and not your venv. 
Make sure that your site is ready-to-run: databases should be initialized but, if possible, empty of any test data.
All your files and folders should be submitted in a single zip file to allow me to run them without modification.
