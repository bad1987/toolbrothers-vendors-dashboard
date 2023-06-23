from datetime import datetime, time
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func, text
from fastapi.encoders import jsonable_encoder
from fastapi import Request, status
from App.Enums.OrderEnums import OrderOrderBy, SortOrder
from App.core.auth import LoginController
from fastapi.responses import JSONResponse

import phpserialize
from App.input_ports.schemas.OrderSchema import CscartOrderDetailSchema
from App.output_ports.models.CscartModels import CscartOrderDetails

from App.input_ports.schemas.OrderSchema import OrderResponseModel, OrdersSchema
from App.core.entities.order_repository import IOrderRepository
from App.output_ports.models.CscartModels import CscartOrders
from App.output_ports.models.Models import User

class OrderRepository(IOrderRepository):
    def __init__(self, db_local: Session, db_cscart: Session) -> None:
        super().__init__()
        self.db_local = db_local
        self.db_cscart = db_cscart

    def get_orders(self, request: Request, skip: int, limit: int, status: list,
        start_time: datetime, end_time: datetime, order_by: str, sort_order: str
    ) -> OrderResponseModel:
        user = LoginController.get_current_user_from_cookie(request, self.db_local)

        query = self.db_cscart.query(CscartOrders).filter(CscartOrders.company_id == user.company_id)

        # process the status
        if status:
            query = query.filter(CscartOrders.status.in_(status))

        # apply start_time and end_time filter
        if start_time and end_time:
            start_time = datetime.combine(start_time.date(), time.min)
            start_timestamp = int(start_time.timestamp())
            end_time = datetime.combine(end_time.date(), time.max)
            end_timestamp = int(end_time.timestamp())
            query = query.filter(and_(CscartOrders.timestamp >= start_timestamp, CscartOrders.timestamp <= end_timestamp))
        elif start_time:
            start_time = datetime.combine(start_time.date(), time.min)
            start_timestamp = int(start_time.timestamp())
            query = query.filter(CscartOrders.timestamp >= start_timestamp)
        elif end_time:
            end_time = datetime.combine(end_time.date(), time.max)
            end_timestamp = int(end_time.timestamp())
            query = query.filter(CscartOrders.timestamp <= end_timestamp)

        # ordering the result
        if order_by:
            if sort_order == SortOrder.desc.value:
                if order_by == OrderOrderBy.timestamp.value:
                    query = query.order_by(CscartOrders.timestamp.desc())
                elif order_by == OrderOrderBy.status.value:
                    query = query.order_by(CscartOrders.status.desc())
            else:
                if order_by == OrderOrderBy.timestamp.value:
                    query = query.order_by(CscartOrders.timestamp.asc())
                elif order_by == OrderOrderBy.status.value:
                    query = query.order_by(CscartOrders.status.asc())

        total = query.count()
        orders = query.offset(skip).limit(limit).all()
        orders = [OrdersSchema.from_orm(p) for p in orders]
        return {"orders": orders, "total": total}

    def get_order(self, request: Request, order_id: int) -> Optional[OrdersSchema]:
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        query = self.db_cscart.query(CscartOrders).filter(CscartOrders.company_id == user.company_id, CscartOrders.order_id == order_id)
        result = query.first()
        return OrdersSchema.from_orm(result)
    
    def get_orders_by_vendor_connected(self, request: Request, skip: int, limit: int, statuses: list):
        
        user = LoginController.get_current_user_from_cookie(request, self.db_local)

        parent = self.db_local.query(User).filter(User.id == user.parent_id).first()

        query = self.db_cscart.query(CscartOrders).filter(CscartOrders.company_id == parent.company_id).filter(CscartOrders.status.in_(statuses)).order_by(desc(CscartOrders.order_id))

        total = query.count()
        orders = query.offset(skip).limit(limit).all()
        
        return {"orders": orders, "total": total}
    
    def get_detail_order(self, request: Request, order_id: int):
        user = LoginController.get_current_user_from_cookie(request, self.db_local)
        
        if not user:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content='Access denied') 

        order = self.db_cscart.query(CscartOrders).filter(CscartOrders.order_id == order_id).first()
        
        order_detail = self.db_cscart.query(CscartOrderDetails).filter(CscartOrderDetails.order_id == order_id).all()
        data_detail = []
        for u in order_detail:
            detail_product = phpserialize.loads(u.extra)

            temp = jsonable_encoder(u)
            temp['extra'] = OrderRepository.decode(detail_product)
            temp = CscartOrderDetailSchema(**temp)
            
            data_detail.append(temp)
            
        return {"order": order, "order_detail": data_detail}
    
    def decode(data: dict):
        result = {}
        for k, v in data.items():
            k = k.decode("utf-8")
            result[k] = v.decode("utf-8") if isinstance(v, bytes) else v
            
        return result
    
    def get_order_stats(self, start_date: str, end_date: str, company_id):
        # get the number of orders and total revenue
        num_orders = self.db_cscart.query(func.count(CscartOrders.order_id))\
            .filter(CscartOrders.company_id == company_id, CscartOrders.timestamp >= func.unix_timestamp(start_date), CscartOrders.timestamp <= func.unix_timestamp(end_date))\
            .scalar()
        total_sales = self.db_cscart.query(func.sum(CscartOrders.total).label('total_sales')) \
            .filter(CscartOrders.company_id == company_id) \
            .filter(CscartOrders.status.in_(['C', 'P'])) \
            .filter(CscartOrders.timestamp >= func.unix_timestamp(start_date)) \
            .filter(CscartOrders.timestamp <= func.unix_timestamp(end_date)) \
            .one()

        total_income = self.db_cscart.query(func.sum(CscartOrders.total).label('total_income')) \
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
    
    def get_grouped_orders(self, start_date: str, end_date: str, company_id: int):
        start = datetime.strptime(f"{start_date} 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp()
        end = datetime.strptime(f"{end_date} 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp()


        query = text(f""" 
                SELECT FROM_UNIXTIME(cscart_orders.timestamp, '%Y-%m-%d') AS date, sum(cscart_orders.total) AS order_total 
                FROM cscart_orders 
                WHERE company_id={company_id} and
                timestamp >= {start} and timestamp <= {end} and
                status in ('C', 'P') 
                GROUP BY date
            """)

        result = self.db_cscart.execute(query)

        ans = [{ "date": row[0], "count": row[1] } for row in result]

        return ans