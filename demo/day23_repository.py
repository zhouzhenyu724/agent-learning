from sqlalchemy import BigInteger, Double, Integer, Text, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
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
