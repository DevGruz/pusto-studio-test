from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    levels: Mapped["PlayerLevel"] = relationship(back_populates="player")


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    order: Mapped[int] = mapped_column(default=0)

    prizes: Mapped["LevelPrize"] = relationship(back_populates="level")


class Prize(Base):
    __tablename__ = "prizes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)


class PlayerLevel(Base):
    __tablename__ = "player_levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"), nullable=False
    )
    level_id: Mapped[int] = mapped_column(
        ForeignKey("levels.id", ondelete="CASCADE"), nullable=False
    )
    completed_date: Mapped[datetime.datetime] = mapped_column()
    is_completed: Mapped[bool] = mapped_column(default=False)
    score: Mapped[int] = mapped_column(default=0)

    player: Mapped["Player"] = relationship(back_populates="levels")
    level: Mapped["Level"] = relationship()
    player_level_prizes: Mapped["PlayerLevelPrize"] = relationship(
        back_populates="player_level"
    )


class LevelPrize(Base):
    __tablename__ = "level_prizes"

    id: Mapped[int] = mapped_column(primary_key=True)
    level_id: Mapped[int] = mapped_column(
        ForeignKey("levels.id", ondelete="CASCADE"), nullable=False
    )
    prize_id: Mapped[int] = mapped_column(
        ForeignKey("prizes.id", ondelete="CASCADE"), nullable=False
    )

    level: Mapped["Level"] = relationship(back_populates="prizes")
    prize: Mapped["Prize"] = relationship()
    player_level_prizes: Mapped["PlayerLevelPrize"] = relationship(
        back_populates="level_prize"
    )


class PlayerLevelPrize(Base):
    __tablename__ = "player_level_prizes"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_level_id: Mapped[int] = mapped_column(
        ForeignKey("player_levels.id", ondelete="CASCADE"), nullable=False
    )
    level_prize_id: Mapped[int] = mapped_column(
        ForeignKey("level_prizes.id", ondelete="CASCADE"), nullable=False
    )
    received_date: Mapped[datetime.datetime] = mapped_column()

    player_level: Mapped["PlayerLevel"] = relationship(
        back_populates="player_level_prizes"
    )
    level_prize: Mapped["LevelPrize"] = relationship(
        back_populates="player_level_prizes"
    )
