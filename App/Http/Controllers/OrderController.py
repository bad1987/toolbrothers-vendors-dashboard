from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import func, select, text, Date
from fastapi import Request
from App.Http.Schema.UserSchema import UserSchema
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

from App.core.auth import LoginController
from App.output_ports.models.CscartModels import CscartOrders
from App.output_ports.repositories.order_repository import OrderRepository

class OrderController:

    def __init__(self, db_local, db_cscart) -> None:
        self.db_local = db_local
        self.db_cscart = db_cscart
        self.order_repo = OrderRepository(db_cscart=db_cscart, db_local=db_local)

    def get_orders_by_vendor_connected(self, request: Request, skip: int, limit: int):
        
        return self.order_repo.get_orders_by_vendor_connected(request=request, skip=skip, limit=limit)
    
    def get_order_stats(self, start_date: str, end_date: str, company_id):
        return self.order_repo.get_order_stats(start_date=start_date, end_date=end_date, company_id=company_id)

    def get_grouped_orders(self, start_date: str, end_date: str, company_id: int):
        return self.order_repo.get_grouped_orders(start_date=start_date, end_date=end_date, company_id=company_id)

    def get_previous_interval(self, date_range):
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

    def progression_percentage(self, current, previous):
        if current is None:
            current = 0
        if previous is None:
            previous = 0
        
        if previous == 0:
            return f"{current:.2f}%"
        
        percent = ((current - previous) / previous) * 100
        percent = f"{percent:.2f}%"
        return percent
