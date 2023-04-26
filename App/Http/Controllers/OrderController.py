from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import func, select, text, Date
from fastapi import Request
from Security.Controllers import LoginController
from Database.CscartModels import CscartOrders
from schemas.UserSchema import UserSchema
from datetime import datetime

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
            'orders': num_orders,
            'income': total_income.total_income,
            'sales': total_sales.total_sales
        }

    def get_grouped_orders(db_cscart: Session, user: UserSchema):
        # query = select(func.from_unixtime(CscartOrders.timestamp, '%D %M %Y').label('date'), func.count(CscartOrders.order_id).label('order_count'))\
        #         .where(CscartOrders.company_id == user.company_id)\
        #         .offset(0)\
        #         .limit(5)\
        #         .group_by('date')


        start = datetime.strptime("22-02-01 00:00:00", "%y-%m-%d %H:%M:%S").timestamp()
        end = datetime.strptime("22-04-01 23:59:59", "%y-%m-%d %H:%M:%S").timestamp()


        print(start, end)

        query = text(f""" 
                SELECT FROM_UNIXTIME(cscart_orders.timestamp, '%y-%m-%d') AS date, sum(cscart_orders.total) AS order_total 
                FROM cscart_orders 
                WHERE company_id={user.company_id} and
                timestamp >= {start} and timestamp <= {end} and
                status in ('C', 'P') 
                GROUP BY date
            """)

        # print(str(query))

        result = db_cscart.execute(query)

        ans = [{ "date": row[0], "count": row[1] } for row in result]

        return ans
