# Personal Finance Tracker

A Flask-based web application designed to help users manage their personal finances with ease. Users can register, log in, track income and expenses, set budgets, and visualize spending patterns with interactive charts. The app integrates real-time currency conversion and is deployed on Render for public access, making it a robust, user-friendly tool for financial management.

## Features

- **User Authentication**: Secure registration and login system to manage personalized financial data.
- **Transaction Management**: Log income and expenses with categories, amounts, currencies, and dates.
- **Budget Planning**: Set monthly budgets for specific categories to track spending goals.
- **Real-Time Currency Conversion**: Convert transaction amounts to USD using ExchangeRate-API with caching for efficiency.
- **Interactive Visualizations**: View spending by category with Plotly pie charts.
- **Cache Management**: Clear cached exchange rates to fetch fresh data.
- **Responsive Design**: Mobile-friendly UI styled with Tailwind CSS.
- **Security**: CSRF protection, password hashing with Bcrypt, and comprehensive logging.
- **Health Check**: Endpoint to monitor application status.

## Screenshots

Below are screenshots showcasing the main features of the Personal Finance Tracker:

### Registration Page

Register a new account with a username, email, and password.

![Registration Page](screenshots/register.png)

### Login Page

Log in with your email and password to access your financial data.

![Login Page](screenshots/login.png)

### Add Transaction

Log income or expenses with details like category, amount, and currency.

![Add Transaction](screenshots/add_transaction.png)

### Set Budget

Set monthly budgets for specific categories to manage spending.

![Set Budget](screenshots/set_budget.png)

### Dashboard

View transactions, budgets, total spending in USD, and a spending breakdown chart.

![Dashboard](screenshots/dashboard.png)

## Installation and Setup

Follow these steps to run the Personal Finance Tracker locally:

### Prerequisites

- Python 3.10.7 or higher
- Git
- A free API key from [ExchangeRate-API](https://www.exchangerate-api.com)

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/kamaleshpantra/Personal-Finance-Tracker.git
   cd Personal-Finance-Tracker


Create and Activate a Virtual Environment:
python -m venv myenv
myenv\Scripts\activate  # On Windows
# or
source myenv/bin/activate  # On macOS/Linux


Install Dependencies:
pip install -r requirements.txt


Set Environment Variables: Create a .env file in the project root and add:
API_KEY=your_exchange_rate_api_key
SECRET_KEY=your_random_secret_key

Generate a secret key with:
python -c "import os; print(os.urandom(24).hex())"


Initialize the Database:
python -c "from app.db import init_db; init_db()"


Run the Application:
python main.py


Access the App: Open a browser and navigate to http://127.0.0.1:5000.


Usage

Register: Visit /register to create an account with a unique username, email, and password (minimum 6 characters).
Log In: Go to /login with your email and password to access your personalized dashboard.
Add Transactions: Navigate to /add_transaction to log income or expenses, selecting a category, amount, currency, and date.
Set Budgets: Use /set_budget to define monthly budgets for categories like Groceries or Utilities.
View Dashboard: Check /dashboard to see your transactions, budgets, total spending in USD, and a pie chart of spending by category.
Clear Cache: Visit /clear_cache (requires login) to refresh exchange rate data.
Log Out: Click the Logout link to end your session.

Deployment
The Personal Finance Tracker is deployed on Render for public access:

Live URL: https://personal-finance-tracker.onrender.com
Platform: Render (free tier with automatic builds from GitHub)
Note: SQLite data may reset on Render free tier restarts. Users may need to re-register after inactivity.

To deploy your own instance:

Push the repository to GitHub.
Create a Web Service on Render, linking your repository.
Set environment variables (API_KEY, SECRET_KEY, PYTHON_VERSION=3.10.7).
Use the build command pip install -r requirements.txt and start command gunicorn main:app.
Monitor deployment logs and test the live URL.

Technologies Used

Backend: Flask 3.0.3, Flask-Login 0.6.3, Flask-Bcrypt 1.0.1, Flask-WTF 1.2.1
Database: SQLite
Frontend: Tailwind CSS 2.2.19, Jinja2
Data Visualization: Plotly 5.24.1, Pandas 2.2.3
API Integration: ExchangeRate-API (via requests 2.32.3)
Caching: cachetools 5.5.0
Deployment: Render, gunicorn 23.0.0
Other: Python 3.10.7, email_validator 2.2.0

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

Please ensure code follows PEP 8 style guidelines and includes tests where applicable.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact

Author: Kamalesh Pantra
GitHub: kamaleshpantra
Email: kamaleshpantra@example.com
Live Demo: https://personal-finance-tracker.onrender.com

For questions, suggestions, or issues, please open an issue on the GitHub repository or contact me directly.


