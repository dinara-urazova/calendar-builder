from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from config_reader import env_config
from entity.event import Event
from typing import List, Optional
   
from sqlalchemy import text


class EventStorageSqlAlchemy:
    def __init__(self):
        connection_str = f"postgresql+pg8000://{env_config.postgresql_username}:{env_config.postgresql_password}@{env_config.postgresql_hostname}:{env_config.postgresql_port}/{env_config.postgresql_database}"
        self.engine = create_engine(connection_str, echo=True)



    def get_events_calendar_view(self, start_date: str, end_date: str):
        query = text("""
            SELECT TO_CHAR(d::date, 'YYYY-MM-DD') AS date,
                COALESCE(e.base_type, '0') AS base_type
            FROM generate_series(:start_date, :end_date, '1 day'::interval) d
            LEFT JOIN events e ON d::date = e.date
        """)
        with Session(self.engine) as session:
            result = session.execute(query, {"start_date": start_date, "end_date": end_date}).fetchall()
            return result
        
    