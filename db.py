from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://2bM8t9gUjeUemkf.root:lmR9lq8RUuSOhv2u@gateway01.ap-northeast-1.prod.aws.tidbcloud.com:4000/test"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"ssl":{}}
    
)
sessionlocal = sessionmaker(bind=engine)
Base = declarative_base()