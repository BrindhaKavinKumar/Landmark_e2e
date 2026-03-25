from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class FileProcessing(Base):
    __tablename__ = "file_processing"

    file_id = Column(UUID(as_uuid=True), primary_key=True)
    store_id = Column(String(50), nullable=False)
    file_name = Column(String(255), nullable=False)
    source_path = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    uploaded_at = Column(TIMESTAMP)
    processing_started_at = Column(TIMESTAMP)
    processing_completed_at = Column(TIMESTAMP)
    total_records = Column(Integer, default=0)
    success_records = Column(Integer, default=0)
    failed_records = Column(Integer, default=0)
    error_message = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())

class RecordProcessing(Base):
    __tablename__ = "record_processing"

    record_id = Column(UUID(as_uuid=True), primary_key=True)
    file_id = Column(UUID(as_uuid=True), ForeignKey("file_processing.file_id"))
    row_number = Column(Integer, nullable=False)
    sku = Column(String(100))
    status = Column(String(50), nullable=False)
    error_message = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class ProductUpdate(Base):
    __tablename__ = "product_updates"

    id = Column(UUID(as_uuid=True), primary_key=True)
    file_id = Column(UUID(as_uuid=True), ForeignKey("file_processing.file_id"))
    store_id = Column(String(50), nullable=False)
    sku = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    offer_price = Column(Numeric(10, 2))
    stock = Column(Integer, nullable=False)
    campaign_id = Column(String(100))
    last_updated = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())

class ErrorLog(Base):
    __tablename__ = "error_logs"

    error_id = Column(UUID(as_uuid=True), primary_key=True)
    file_id = Column(UUID(as_uuid=True), ForeignKey("file_processing.file_id"))
    row_number = Column(Integer)
    error_type = Column(String(100))
    error_message = Column(Text)
    raw_data = Column(JSONB)
    created_at = Column(TIMESTAMP, server_default=func.now())