import sqlite3
from flask import render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange
from flask_login import login_user, logout_user, login_required, current_user
from .db import get_db_connection
from .utils import get_exchange_rate
from .forms import TransactionForm, BudgetForm, RegistrationForm, LoginForm
from .models import User
from flask_bcrypt import Bcrypt
import pandas as pd
import plotly.express as px
import logging

logger = logging.getLogger(__name__)

def init_routes(app):
    bcrypt = Bcrypt(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = RegistrationForm()
        if form.validate_on_submit():
            try:
                conn = get_db_connection()
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                            (form.username.data, form.email.data, hashed_password))
                conn.commit()
                flash('Your account has been created! Please log in.', 'success')
                logger.info(f"User registered: {form.email.data}")
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                conn.rollback()
                flash('Username or email already exists.', 'error')
            except Exception as e:
                conn.rollback()
                flash(f'Error registering user: {str(e)}', 'error')
                logger.error(f"Registration error: {e}")
            finally:
                conn.close()
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.find_by_email(form.email.data)
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Login successful!', 'success')
                logger.info(f"User logged in: {user.email}")
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Login failed. Check email and password.', 'error')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(url_for('index'))

    @app.route('/add_transaction', methods=['GET', 'POST'])
    @login_required
    def add_transaction():
        form = TransactionForm()
        if form.validate_on_submit():
            try:
                conn = get_db_connection()
                conn.execute('INSERT INTO transactions (user_id, type, category, amount, currency, date) VALUES (?, ?, ?, ?, ?, ?)',
                            (current_user.id, form.type.data, form.category.data, form.amount.data, form.currency.data, form.date.data.isoformat()))
                conn.commit()
                flash('Transaction added successfully!', 'success')
                logger.info(f"Added transaction for user {current_user.id}: {form.category.data}, {form.amount.data} {form.currency.data}")
                return redirect(url_for('dashboard'))
            except Exception as e:
                conn.rollback()
                flash(f'Error adding transaction: {str(e)}', 'error')
                logger.error(f"Transaction add error for user {current_user.id}: {e}")
            finally:
                conn.close()
        return render_template('add_transaction.html', form=form)

    @app.route('/set_budget', methods=['GET', 'POST'])
    @login_required
    def set_budget():
        form = BudgetForm()
        if form.validate_on_submit():
            try:
                conn = get_db_connection()
                conn.execute('INSERT INTO budgets (user_id, category, amount, month) VALUES (?, ?, ?, ?)',
                            (current_user.id, form.category.data, form.amount.data, form.month.data))
                conn.commit()
                flash('Budget set successfully!', 'success')
                logger.info(f"Set budget for user {current_user.id}: {form.category.data}, {form.amount.data}")
                return redirect(url_for('dashboard'))
            except Exception as e:
                conn.rollback()
                flash(f'Error setting budget: {str(e)}', 'error')
                logger.error(f"Budget set error for user {current_user.id}: {e}")
            finally:
                conn.close()
        return render_template('set_budget.html', form=form)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        try:
            conn = get_db_connection()
            transactions = conn.execute('SELECT * FROM transactions WHERE user_id = ?', (current_user.id,)).fetchall()
            budgets = conn.execute('SELECT * FROM budgets WHERE user_id = ?', (current_user.id,)).fetchall()
            
            transactions_list = [dict(row) for row in transactions]
            df = pd.DataFrame(transactions_list, columns=['id', 'user_id', 'type', 'category', 'amount', 'currency', 'date'])
            
            plot_html = "<p>No transactions available.</p>"
            if not df.empty:
                fig = px.pie(df, values='amount', names='category', title='Spending by Category')
                plot_html = fig.to_html(full_html=False)
            
            total_spending = 0
            for t in transactions:
                rate = get_exchange_rate(t['currency'], 'USD')
                total_spending += t['amount'] * rate
            
            conn.close()
            return render_template('dashboard.html', transactions=transactions, budgets=budgets, 
                                 plot_html=plot_html, total_spending=total_spending)
        except Exception as e:
            flash(f'Error loading dashboard: {str(e)}', 'error')
            logger.error(f"Dashboard error for user {current_user.id}: {e}")
            return render_template('dashboard.html', transactions=[], budgets=[], plot_html="<p>Error loading chart.</p>", total_spending=0)

    @app.route('/clear_cache')
    @login_required
    def clear_cache():
        from .utils import clear_cache
        clear_cache()
        flash('Cache cleared successfully!', 'success')
        return redirect(url_for('dashboard'))

    @app.route('/health')
    def health():
        try:
            conn = get_db_connection()
            conn.execute('SELECT 1')
            conn.close()
            return {"status": "healthy"}, 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}, 500