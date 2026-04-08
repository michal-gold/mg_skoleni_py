# Robot Data ETL Assignment

## Popis reseni
1. **Priprava site**: Vyuziva bridge sit `etl_network` pro izolovanou komunikaci mezi kontejnery.
2. **Sluzba db_server**: MariaDB 11 (verze 11 doporucena kvuli stabilite) s vlastnim Dockerfilem, optimalizovana pro ukladani trajektorii.
3. **Sluzba python_app**: 
   - **Extract**: Cteni dat z `R1.csv` (snaha o logovani, z duvodu zapasu s dockerem pres prikazovy radek, most: docker - linux vs virtualka s windows s vs code).
   - **Transform**: mapovani jen urcitych dat (Time, X, Y, Z) pomoci SQLModel - chtel jsem vedet, jak prenaset jen vybrana data - SQLModel mi byl doporucen jako elegantni reseni.
   - **Load**: vlozeni dat do databaze po nacteni celeho csv souboru.


## Spusteni (Standardni cesta)
Pro prostredi s nainstalovanym Docker Desktop / Docker Compose:

```bash
# Sestaveni a spusteni celeho stacku
docker-compose up --build

# Kontrola dat v DB
docker-compose exec db_server mariadb -u myuser -pmypassword -e "SELECT * FROM robot_trajectory LIMIT 5;" robot_db
```

## Pristupove udaje (Defaultni)
Pro ucely testovani jsou v `docker-compose.yml` nastaveny tyto udaje:
- **Host:** db_server (v ramci docker site)
- **User:** myuser
- **Password:** mypassword
- **Database:** robot_db
