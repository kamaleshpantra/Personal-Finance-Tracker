from flask import render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange
from .db import get_db_connection
from .utils import get_exchange_rate
import pandas as pd
import plotly.express as px
import logging

logger = logging.getLogger(__name__)

class TransactionForm(FlaskForm):
    type = SelectField('Type', choices=[('Income', 'Income'), ('Expense', 'Expense')], validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    currency = SelectField('Currency', choices=[('USD', 'USD'), ('EUR', 'EUR'), ('INR', 'INR')], validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])

class BudgetForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    month = StringField('Month', validators=[DataRequired()])

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    
    @app.route('/add_transaction', methods=['GET', 'POST'])
    def add_transaction():
        form = TransactionForm()
        if form.validate_on_submit():
            try:
                conn = get_db_connection()
                conn.execute('INSERT INTO transactions (type, category, amount, currency, date) VALUES (?, ?, ?, ?, ?)',
                        (form.type.data, form.category.data, form.amount.data, form.currency.data, form.date.data.isoformat()))
                conn.commit()
                flash('Transaction added successfully!', 'success')
                logger.info(f"Added transaction: {form.category.data}, {form.amount.data} {form.currency.data}")
                return redirect(url_for('dashboard'))
            except Exception as e:
                conn.rollback()
                flash(f'Error adding transaction: {str(e)}', 'error')
                logger.error(f"Transaction add error: {e}")
            finally:
                conn.close()
        return render_template('add_transaction.html', form=form)

    @app.route('/set_budget', methods=['GET', 'POST'])
    def set_budget():
        form = BudgetForm()
        if form.validate_on_submit():
            try:
                conn = get_db_connection()
                conn.execute('INSERT INTO budgets (category, amount, month) VALUES (?, ?, ?)',
                            (form.category.data, form.amount.data, form.month.data))
                conn.commit()
                flash('Budget set successfully!', 'success')
                logger.info(f"Set budget: {form.category.data}, {form.amount.data}")
                return redirect(url_for('dashboard'))
            except Exception as e:
                conn.rollback()
                flash(f'Error setting budget: {str(e)}', 'error')
                logger.error(f"Budget set error: {e}")
            finally:
                conn.close()
        return render_template('set_budget.html', form=form)
    @app.route('/dashboard')
    def dashboard():
        try:
            conn = get_db_connection()
            transactions = conn.execute('SELECT * FROM transactions').fetchall()
            budgets = conn.execute('SELECT * FROM budgets').fetchall()
        
            # Convert transactions to a list of dictionaries
            transactions_list = [dict(row) for row in transactions]
        
            # Create DataFrame with explicit columns
            df = pd.DataFrame(transactions_list, columns=['id', 'type', 'category', 'amount', 'currency', 'date'])
        
            plot_html = "<p>No transactions available.</p>"
            if not df.empty:
                fig = px.pie(df, values='amount', names='category', title='Spending by Category')
                plot_html = fig.to_html(full_html=False)
        
            # Convert transaction amounts to USD for summary
            total_spending = 0
            for t in transactions:
                rate = get_exchange_rate(t['currency'], 'USD')
                total_spending += t['amount'] * rate
        
            conn.close()
            return render_template('dashboard.html', transactions=transactions, budgets=budgets, 
                             plot_html=plot_html, total_spending=total_spending)
        except Exception as e:
            flash(f'Error loading dashboard: {str(e)}', 'error')
            logger.error(f"Dashboard error: {e}")
            return render_template('dashboard.html', transactions=[], budgets=[], plot_html="<p>Error loading chart.</p>", total_spending=0)
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
    
    # Add inside init_routes(app) function, before other routes
    @app.route('/clear_cache')
    def clear_cache():
        from .utils import clear_cache
        clear_cache()
        flash('Cache cleared successfully!', 'success')
        return redirect(url_for('dashboard'))