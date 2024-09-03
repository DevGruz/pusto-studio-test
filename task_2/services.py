import csv
from datetime import date

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from models import PlayerLevel, PlayerLevelPrize, Player, Level, Prize, LevelPrize


def assign_prize_to_player(
    player_id: int, level_id: int, prize_id: int, session: Session
):
    player_level = session.execute(
        select(PlayerLevel).filter_by(player_id=player_id, level_id=level_id)
    ).scalar_one_or_none()

    if player_level and player_level.is_completed:
        player_level_prize = session.execute(
            insert(PlayerLevelPrize).values(
                player_level_id=player_level.id,
                level_prize_id=prize_id,
                received_date=date.today(),
            )
        )
        player_level_prize.fetchall()
        session.commit()


def export_player_data_to_csv(session: Session, file_path: str):
    stmt = (
        select(
            Player.id.label("Player ID"),
            Level.title.label("Level Title"),
            PlayerLevel.is_completed.label("Level Completed"),
            Prize.title.label("Prize Title"),
        )
        .join(PlayerLevel, Player.id == PlayerLevel.player_id)
        .join(Level, Level.id == PlayerLevel.level_id)
        .join(PlayerLevelPrize, PlayerLevel.id == PlayerLevelPrize.player_level_id)
        .join(LevelPrize, LevelPrize.id == PlayerLevelPrize.level_prize_id)
        .join(Prize, Prize.id == LevelPrize.prize_id)
    )
    result = session.execute(stmt).yield_per(1000).mappings()

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Player ID", "Level Title", "Level Completed", "Prize Title"])
        for row in result:
            writer.writerow(
                [
                    row["Player ID"],
                    row["Level Title"],
                    row["Level Completed"],
                    row["Prize Title"],
                ]
            )
