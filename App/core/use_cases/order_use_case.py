from datetime import datetime
from typing import List

from fastapi import Depends, Request
from App.Http.Controllers.OrderController import OrderController
from App.core.auth.LoginController import get_current_user_from_cookie
from App.input_ports.schemas.OrderSchema import OrderResponseModel, SingleOrderResponseModel

from App.output_ports.repositories.order_repository import OrderRepository

from sqlalchemy.orm import Session
from App.output_ports.repositories.product_repository import ProductRepository

from App.output_ports.repositories.user_repository import UserRepository


class OrderUsecase:
    def __init__(self, db_local: Session, db_cscart: Session) -> None:
        self.db_local = db_local
        self.db_cscart = db_cscart
        self.order_repository = OrderRepository(db_local=self.db_local, db_cscart=self.db_cscart)
        self.user_repository = UserRepository(self.db_local)
        self.prod_repository = ProductRepository(db_cscart=self.db_cscart, db_local=self.db_local)
    
    def get_order_list(self, request: Request, skip: int, limit: int, 
        status: list, start_time: datetime, end_time: datetime, order_by: str, sort_order: str
    ) -> OrderResponseModel:
        return self.order_repository.get_orders(request=request,skip=skip, limit=limit, 
            status=status, start_time=start_time, end_time=end_time, order_by=order_by, sort_order=sort_order
        )
    
    def get_order(self, request: Request, order_id: int) -> SingleOrderResponseModel:
        result = self.order_repository.get_order(request=request, order_id=order_id)
        return {"order": result}
    
    def get_detail_order(self, request: Request, order_id: int):
  
        result = self.order_repository.get_detail_order(request, order_id)
        return result
    
    def get_orders_by_vendor_connected(self, request: Request, skip: int, limit: int, statuses: list):
        return self.order_repository.get_orders_by_vendor_connected(request, skip, limit, statuses)

    def get_order_statistics(self, request: Request, start_date: str, end_date: str):
        _user = get_current_user_from_cookie(request=request, db=self.db_local)
        start_date_string = f"{start_date} 00:00:00"
        end_date_string = f"{end_date} 23:59:59"
        company_id=_user.company_id

        if (company_id == None and _user.parent_id != None):
            parent = self.user_repository.get_parent(_user.parent_id)

            company_id = parent.company_id
        order_cont = OrderController(db_local=self.db_local, db_cscart=self.db_cscart)
        res = order_cont.get_order_stats(start_date_string, end_date_string, company_id)
        p_res = self.prod_repository.get_product_stats(company_id)

        # Chart data
        chart_datas = order_cont.get_grouped_orders(start_date, end_date, company_id)

        res.update(p_res)
        res.update({ "chart_datas": chart_datas })

        res.update(p_res)

        # dealing with the previous period
        prev_period = order_cont.get_previous_interval([start_date, end_date])
        p_stats = order_cont.get_order_stats(prev_period[0], prev_period[1], company_id)
        p_chart_datas = order_cont.get_grouped_orders(prev_period[0], prev_period[1], company_id)
        p_stats.update({
            'percent_income': order_cont.progression_percentage(res['income'], p_stats['income']),
            'percent_sales': order_cont.progression_percentage(res['sales'], p_stats['sales']),
            'percent_orders': order_cont.progression_percentage(res['orders'], p_stats['orders']),
            'label': "previous period",
            'prev_chart': p_chart_datas
        })
        res.update({
            'prev_period': p_stats
        })
        res.update({
            'start_date': start_date,
            'end_date': end_date
        })
        return res

