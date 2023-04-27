from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import func, select, text, Date
from fastapi import Request
from Security.Controllers import LoginController
from Database.CscartModels import CscartOrders
from schemas.UserSchema import UserSchema
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

class OrderController:
    def get_orders_by_vendor_connected(request: Request, db_local: Session, db_cscart: Session, skip: int, limit: int):
        
        user = LoginController.get_current_user_from_cookie(request, db_local)

        query = db_cscart.query(CscartOrders).filter(CscartOrders.company_id == user.company_id)

        total = query.count()
        orders = query.offset(skip).limit(limit).all()
        
        return {"user": user, "orders": orders, "total": total}
    
    def get_order_stats(db_cscart: Session, start_date: str, end_date: str, company_id):
        # get the number of orders and total revenue for March 25 to April 25, 2023
        num_orders = db_cscart.query(func.count(CscartOrders.order_id))\
            .filter(CscartOrders.company_id == company_id, CscartOrders.timestamp >= func.unix_timestamp(start_date), CscartOrders.timestamp <= func.unix_timestamp(end_date))\
            .scalar()
        # total_revenue = db_cscart.query(func.sum(CscartOrders.total)).filter(CscartOrders.timestamp >= start_date, CscartOrders.timestamp <= end_date).scalar()
        total_sales = db_cscart.query(func.sum(CscartOrders.total).label('total_sales')) \
            .filter(CscartOrders.company_id == company_id) \
            .filter(CscartOrders.status.in_(['C', 'P'])) \
            .filter(CscartOrders.timestamp >= func.unix_timestamp(start_date)) \
            .filter(CscartOrders.timestamp <= func.unix_timestamp(end_date)) \
            .one()

        total_income = db_cscart.query(func.sum(CscartOrders.total).label('total_income')) \
            .filter(CscartOrders.company_id == company_id) \
            .filter(CscartOrders.status.in_(['C', 'P', 'O'])) \
            .filter(CscartOrders.timestamp >= func.unix_timestamp(start_date)) \
            .filter(CscartOrders.timestamp <= func.unix_timestamp(end_date)) \
            .one()

        return {
            'orders': num_orders or 0,
            'income': total_income.total_income or 0,
            'sales': total_sales.total_sales or 0
        }

    def get_grouped_orders(db_cscart: Session, user: UserSchema, start_date: str, end_date: str):
        start = datetime.strptime(f"{start_date} 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp()
        end = datetime.strptime(f"{end_date} 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp()


        query = text(f""" 
                SELECT FROM_UNIXTIME(cscart_orders.timestamp, '%Y-%m-%d') AS date, sum(cscart_orders.total) AS order_total 
                FROM cscart_orders 
                WHERE company_id={user.company_id} and
                timestamp >= {start} and timestamp <= {end} and
                status in ('C', 'P') 
                GROUP BY date
            """)

        result = db_cscart.execute(query)

        ans = [{ "date": row[0], "count": row[1] } for row in result]

        return ans

    def get_previous_interval(date_range):
        # Parse the input dates into datetime objects
        start_date = parse(date_range[0])
        end_date = parse(date_range[1])

        # Compute the number of years between the start and end years
        num_years = relativedelta(end_date, start_date).years

        # Compute the year of the previous period
        prev_year_end = start_date.year - 1
        prev_year_start = prev_year_end - num_years

        # Compute the start and end dates of the previous period
        prev_start_date = start_date.replace(year=prev_year_start)
        prev_end_date = end_date.replace(year=prev_year_end)

        # Adjust end date for leap years
        if prev_end_date.year % 4 == 0 and (prev_end_date.year % 100 != 0 or prev_end_date.year % 400 == 0):
            prev_end_date += relativedelta(days=1)

        # Format output dates as strings in the desired format
        start_date_prev_str = prev_start_date.strftime('%Y-%m-%d')
        end_date_prev_str = prev_end_date.strftime('%Y-%m-%d')

        res = [start_date_prev_str, end_date_prev_str]
        print(res)
        return res

    def progression_percentage(current, previous):
        if current is None:
            current = 0
        if previous is None:
            previous = 0
        
        if previous == 0:
            return f"{current:.2f}%"
        
        percent = ((current - previous) / previous) * 100
        percent = f"{percent:.2f}%"
        return percent
