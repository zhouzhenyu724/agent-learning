from sqlalchemy import BigInteger, Double, Integer, Text, select, update, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    topic: Mapped[str] = mapped_column(Text)
    hours: Mapped[float] = mapped_column(Double)


def find_record(
    session: Session, *, user_id: int, record_id: int
) -> Record | None:
    statement = select(Record).where(
        Record.user_id == user_id,
        Record.id == record_id,
    )
    return session.scalars(statement).one_or_none()

def create_record(session: Session, *, user_id: int, topic: str, hours: float) -> Record:
    record = Record(user_id=user_id, topic=topic, hours=hours)
    session.add(record)
    session.flush()
    return record

def update_record(
    session: Session, *, user_id: int, record_id: int, changes: dict[str, str | float]
) -> Record | None:
    statement = (
        update(Record)
        .where(Record.user_id == user_id, Record.id == record_id)
        .values(**changes)
        .returning(Record)
    )
    return session.scalars(statement).one_or_none()


def delete_record(session: Session, *, user_id: int, record_id: int) -> bool:
    statement = (
        delete(Record)
        .where(Record.user_id == user_id, Record.id == record_id)
        .returning(Record.id)
    )
    return session.scalars(statement).one_or_none() is not None


def find_all_records(session: Session, *, user_id: int) -> list[Record]:
    statement = select(Record).where(Record.user_id == user_id)
    return session.scalars(statement).all()