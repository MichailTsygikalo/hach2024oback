from sqlalchemy import Integer, String, Boolean, select, DECIMAL,ForeignKey,Float
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapped_column, relationship
from passlib.context import CryptContext

from app.core.db import Base, Session

pwd_context =  CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(Base):
    __tablename__ = 'user'
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(255), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    status = mapped_column(Boolean, nullable=False, default=False)
    products = relationship("ProductModel", back_populates="user")
    accounts = relationship("AccountModel", back_populates="user")
    co2 = mapped_column(Float, default=0.0)

    def check_user_exists(self,session:Session):
        with session.begin():
            user = session.execute(select(UserModel).filter(UserModel.email == self.email)).scalars().first()
        return True if user else False
    
    def create_new_user(self,session:Session):
        user = UserModel(
            email = self.email,
            # password = pwd_context.hash(self.password),
            password = self.password,
            status = False
        )
        with session.begin():
            try:
                session.add(user)
                session.commit()
                return user
            except IntegrityError as e:
                session.rollback()
                raise {"IntegrityError:":e}
    
    def change_user_status(self, status: bool, session:Session):
        with session.begin():
            user = session.execute(select(UserModel).filter(UserModel.email == self.email)).scalars().first()
            user.status = status
            session.commit()

class ProductModel(Base):
    __tablename__ = 'product'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), nullable=False)
    price = mapped_column(DECIMAL, nullable=False)
    cashback = mapped_column(DECIMAL)
    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("UserModel", back_populates="products") 
    is_dropped = mapped_column(Boolean)
    type_id = mapped_column(Integer, ForeignKey('product_type.id'), nullable=False)
    product_type = relationship("TypeOfProductModel", back_populates="product")
    container_id = mapped_column(Integer, ForeignKey('container.id'))
    container = relationship("СontainerModel", back_populates="product")
    co2 = mapped_column(Float, default=0.0)
    count = mapped_column(Float, default=0.0)

    def get_product(self, session:Session):
        with session.begin():
            product = session.execute(select(ProductModel).filter(ProductModel.id == self.id)).scalars().first()
            return product
        
    def change_product_status(self, status: bool, session:Session):
        with session.begin():
            prod = session.execute(select(ProductModel).filter(ProductModel.id == self.id)).scalars().first()
            c = session.execute(select(СontainerModel).filter(СontainerModel.id == self.container_id)).scalars().first()
            print(prod.type_id, c.type_id)
            if prod.type_id == c.type_id:
                prod.is_dropped = status
                prod.container_id = self.container_id
                session.commit()
                return prod
            return 1
        
class AccountModel(Base):
    __tablename__ = 'account'
    id = mapped_column(Integer, primary_key=True)
    bonus_count = mapped_column(DECIMAL)
    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("UserModel", back_populates="accounts")

    def create_new_account(self,session:Session):
        with session.begin():
            try:
                session.add(self)
                session.commit()
                return self
            except IntegrityError as e:
                session.rollback()
                raise {"IntegrityError:":e}
            
    def change_bonus_count(self, count: float, session:Session):
        with session.begin():
            acc = session.execute(select(AccountModel).filter(AccountModel.user_id == self.user_id)).scalars().first()
            acc.bonus_count += count
            session.commit()
            return acc
        
class TypeOfProductModel(Base):
    __tablename__ = 'product_type'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), nullable=False)
    container = relationship("СontainerModel", back_populates="product_type")
    product = relationship("ProductModel", back_populates="product_type")
    product_e = relationship("ProductEModel", back_populates="product_type")

class СontainerModel(Base):
    __tablename__ = 'container'
    id = mapped_column(Integer, primary_key=True)
    type_id = mapped_column(Integer, ForeignKey('product_type.id'), nullable=False)
    product_type = relationship("TypeOfProductModel", back_populates="container")
    x = mapped_column(DECIMAL(11,8), nullable=False)
    y = mapped_column(DECIMAL(11,8), nullable=False)
    product = relationship("ProductModel", back_populates="container")

class ProductEModel(Base):
    __tablename__ = 'product_e'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), nullable=False)
    price = mapped_column(DECIMAL, nullable=False)
    cashback = mapped_column(DECIMAL)
    co2 = mapped_column(Float, default=0.0)
    type_id = mapped_column(Integer, ForeignKey('product_type.id'), nullable=False)
    product_type = relationship("TypeOfProductModel", back_populates="product_e")