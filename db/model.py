from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.mysql import (
    INTEGER, SMALLINT, TINYINT, VARCHAR, BIGINT
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class CatalogGroup(Base):
    """Product categories / groups."""
    __tablename__ = "tbl_catalog_group"
    __table_args__ = {
        "mysql_engine": "MyISAM",
        "mysql_charset": "cp1251",
    }

    catalog_group_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    catalog_group_name: Mapped[str] = mapped_column(
        VARCHAR(255), unique=True, nullable=False
    )
    catalog_group_output_order: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), nullable=False, server_default="0"
    )

    # One-to-many: group -> items
    catalog_items: Mapped[List["Catalog"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )


class Catalog(Base):
    """Individual inventory items."""
    __tablename__ = "tbl_catalog"
    __table_args__ = (
        Index("catalog_block_id", "catalog_group_id", "catalog_item_in_report"),
        {"mysql_engine": "MyISAM", "mysql_charset": "cp1251"},
    )

    catalog_item_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    catalog_group_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("tbl_catalog_group.catalog_group_id"),
        nullable=False
    )
    catalog_item_in_report: Mapped[int] = mapped_column(
        SMALLINT(unsigned=True), nullable=False, server_default="1"
    )
    catalog_item_output_order: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
        server_default="0",
        comment="Определяет в каком порядке в группе выводить позиции",
    )
    catalog_item_name: Mapped[str] = mapped_column(
        VARCHAR(255), unique=True, nullable=False
    )
    catalog_item_delivery_period: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), nullable=False, server_default="0"
    )
    catalog_item_data_hold_time: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), nullable=False
    )

    # Relationships
    group: Mapped["CatalogGroup"] = relationship(
        back_populates="catalog_items", foreign_keys=[catalog_group_id]
    )
    help_records: Mapped[List["Help"]] = relationship(
        back_populates="catalog_item", cascade="all, delete-orphan"
    )


class People(Base):
    """Persons receiving aid."""
    __tablename__ = "tbl_people"
    __table_args__ = (
        Index("people_family", "people_family", "people_name", "people_patronymic"),
        {"mysql_engine": "MyISAM", "mysql_charset": "cp1251"},
    )

    people_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    people_family: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    people_name: Mapped[str] = mapped_column(
        VARCHAR(100), nullable=False, server_default=""
    )
    people_patronymic: Mapped[str] = mapped_column(
        VARCHAR(100), nullable=False, server_default=""
    )
    people_gender: Mapped[Optional[int]] = mapped_column(
        TINYINT(unsigned=True),
        nullable=True,
        comment="1- мужской 2 - женский",
    )
    people_came_from: Mapped[str] = mapped_column(
        VARCHAR(100), nullable=False, server_default=""
    )
    people_birthday: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), nullable=False, server_default="0"
    )
    people_time_reg: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), nullable=False, server_default="0"
    )
    people_time_last_visit: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), nullable=False, server_default="0"
    )
    people_comment: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=False, server_default=""
    )

    # One-to-many: people -> help records
    help_records: Mapped[List["Help"]] = relationship(
        back_populates="people", cascade="all, delete-orphan"
    )


class Help(Base):
    """Issuance records (many-to-many between People and Catalog)."""
    __tablename__ = "tbl_help"
    __table_args__ = (
        UniqueConstraint(
            "people_id", "catalog_item_id", "help_time", name="people_id"
        ),
        {"mysql_engine": "MyISAM", "mysql_charset": "cp1251"},
    )

    people_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("tbl_people.people_id", ondelete="CASCADE"),
        primary_key=True,  # part of composite PK
    )
    catalog_item_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("tbl_catalog.catalog_item_id", ondelete="CASCADE"),
        primary_key=True,
    )
    help_time: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        comment="Сохраняется тайм стамп на момент 01:01:01 даты выдачи",
    )

    # Relationships
    people: Mapped["People"] = relationship(back_populates="help_records")
    catalog_item: Mapped["Catalog"] = relationship(back_populates="help_records")