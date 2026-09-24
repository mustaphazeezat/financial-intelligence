from sqlalchemy import text

from app.db.database import engine


def get_or_create_sector(sector_name):

    query = text("""
        INSERT INTO sectors (name)
        VALUES (:name)
        ON CONFLICT (name)
        DO UPDATE SET name = EXCLUDED.name
        RETURNING id
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {"name": sector_name}
        )

        return result.scalar_one()

def get_or_create_industry(industry_name, sector_id):

    query = text("""
        INSERT INTO industries (name, sector_id)
        VALUES (:name, :sector_id)
        ON CONFLICT (name)
        DO UPDATE SET sector_id = EXCLUDED.sector_id
        RETURNING id
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "name": industry_name,
                "sector_id": sector_id
            }
        )

        return result.scalar_one()

def get_industry_by_id_db(id: int):
    query = text("""
        SELECT name, sector_id
        FROM industries
        WHERE id = :id
    """)

    with engine.connect() as connection:
        result = connection.execute(query, {"id": id})
        industry = result.mappings().first()

        return dict(industry) if industry else None
    
def get_sectorname_db(id: int):
    query = text("""
        SELECT name
        FROM sectors
        WHERE id = :id
    """)

    with engine.connect() as connection:
        result = connection.execute(query, {"id": id})
        return result.scalar_one_or_none()