import os
import csv
import logging
import time
import sys
from sqlmodel import Session, create_engine, SQLModel
from lib.models import RobotPath

# Konfigurace logovani - cas a uroven jsou dulezite pro diagnostiku v Dockeru
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logging.info("ETL proces inicializovan...")

# Nacteni konfigurace z ENV - bezpecne a flexibilni reseni (12-factor app)
DB_HOST = os.getenv("DB_HOST", "db_server")
DB_NAME = os.getenv("DB_DATABASE", "robot_db")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")
DATA_PATH = os.getenv("DATA_PATH", "/app/data/R1.csv")

# Connection string pro PyMySQL driver
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
engine = create_engine(DB_URL)

def init_db():
    """
    Zajistuje integritu DB schematu s Retry logikou pro Docker start.
    """
    logging.info(f"Navazovani spojeni s DB: {DB_HOST}...")
    for i in range(1, 6):
        try:
            SQLModel.metadata.create_all(engine)
            logging.info("Databaze a tabulky jsou pripraveny.")
            return True
        except Exception as e:
            logging.warning(f"DB neni ready (pokus {i}/5): {e}")
            time.sleep(3)
    return False

def run_etl():
    """
    Hlavni pipeline: Extract (CSV) -> Transform (Typovani) -> Load (SQLModel)
    """
    if not os.path.exists(DATA_PATH):
        logging.error(f"SOUBOR NENALEZEN: {DATA_PATH}")
        return

    logging.info(f"Ctu soubor: {DATA_PATH}")
    
    with open(DATA_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',')
        try:
            header = next(reader)
            logging.info(f"Hlavicka nactena, sloupcu: {len(header)}")
        except StopIteration:
            logging.error("Soubor je prazdny!")
            return

        with Session(engine) as session:
            count = 0
            for row in reader:
                if len(row) < 11:
                    continue
                try:
                    # Mapovani: 0=Time, 8=X, 9=Y, 10=Z (podle specifikace robota)
                    record = RobotPath(
                        time=float(row[0]),
                        pos_x=float(row[8]),
                        pos_y=float(row[9]),
                        pos_z=float(row[10])
                    )
                    session.add(record)
                    count += 1
                    if count % 500 == 0:
                        logging.info(f"Zpracovano {count} radku...")
                except (ValueError, IndexError) as e:
                    continue
            
            # Ulozeni dat (najednou)
            session.commit()
            logging.info(f"HOTOVO! Ulozeno {count} zaznamu.")

if __name__ == "__main__":
    if init_db():
        run_etl()
    else:
        logging.critical("ETL selhalo - chyba databaze.")
        sys.exit(1)
