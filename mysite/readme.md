# Portfolio Builder Website

## Idea
Build a website that allows users to easily create a personalized portfolio.

## Workflow
1. **User Login**  
   - User logs in. If no account exists, the user must create one.
2. **Template Selection**  
   - User selects a portfolio template.
3. **Form Completion**  
   - User fills out a form with all required information (including photos of self and projects). (Note: File uploads vs direct links are yet to be decided.)
4. **Result**  
   - Display a preview of the generated portfolio or offer the website download, allowing the user to keep or discard it.

## Implementation Plan
1. Identify suitable single-page portfolio templates.
2. Create a user model in the database.
3. Implement authentication using JWT.
4. Develop the base form.
5. Write backend logic to process the form data and populate the portfolio template.
6. Determine the delivery method for the generated files.



