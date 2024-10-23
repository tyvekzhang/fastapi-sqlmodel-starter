from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

# 配置数据库连接字符串（请替换为您实际的数据库连接信息）
DATABASE_URL = "sqlite:///fss/migrations/db/fss.db"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)


# 获取数据库中的所有表名
@app.get("/tables")
async def get_tables():
    try:
        # 使用 SQLAlchemy 的 inspector 获取数据库表信息
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        return {"tables": tables}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# 获取指定表的字段及其类型
@app.get("/table/{table_name}/fields")
async def get_table_fields(table_name: str):
    try:
        # 使用 SQLAlchemy 的 inspector 获取表的列信息
        inspector = inspect(engine)

        # 检查表是否存在
        if table_name not in inspector.get_table_names():
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

        # 获取指定表的列信息
        columns = inspector.get_columns(table_name)
        fields = []
        for column in columns:
            fields.append({
                "name": column["name"],
                "type": str(column["type"])
            })
        return {"table": table_name, "fields": fields}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")