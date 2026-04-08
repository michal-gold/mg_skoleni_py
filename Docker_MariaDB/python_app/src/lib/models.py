from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

class RobotPath(SQLModel, table=True):
    """
    Reprezentuje zaznam polohy TCP (Tool Center Point) robotu v case.
    Slouzi pro ukladani a naslednou analyzu trajektorie z PDF reportu.
    """
    # Explicitni nazev tabulky pro prehlednost v DB
    __tablename__ = "robot_trajectory"

    # Primarni klic - SQLModel/SQLAlchemy ho resi automaticky pri insertu
    id: int | None = Field(default=None, primary_key=True)

    # Relativni cas od zacatku cyklu (napr. v sekundach [s])
    # Klicove pro vypocet rychlosti a zrychleni
    time: float

    # Kartezske souradnice TCP vuci aktualnimu Wobj
    # Predpoklad: Jednotky jsou milimetry [mm]
    pos_x: float
    pos_y: float
    pos_z: float

    # Auditni zaznam: Kdy byl radek fyzicky vlozen do DB (UTC)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp vlozeni zaznamu do DB (UTC)"
    )
