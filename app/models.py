from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from .database import Base
class FileType(PyEnum):
	csv = "csv"
	image = "image"
class File(Base):
	__tablename__ = "files"
	id = Column(Integer, primary_key=True, index=True)
	filename = Column(String, index=True, nullable=False)
	filetype = Column(Enum(FileType), index=True, nullable=False)
	path = Column(String, nullable=False)
	size = Column(Integer, nullable=False)
	meta = Column(JSON, nullable=True)
	created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

