from sqlalchemy import text

from app.db.database import engine


def save_movers(movers, category):
    query = text("""
        INSERT INTO market_movers (
            symbol,
            category,
            price,
            change_amount,
            change_percentage,
            volume
        )
        VALUES (
            :symbol,
            :category,
            :price,
            :change_amount,
            :change_percentage,
            :volume
        )
    """)
    records = []

    for mover in movers:
        records.append({
            "symbol": mover["ticker"],
            "category": category,
            "price": float(mover["price"]),
            "change_amount": float(mover["change_amount"]),
            "change_percentage": float(
                mover["change_percentage"].rstrip("%")
            ),
            "volume": int(mover["volume"])
        })
    with engine.begin() as connection:
        connection.execute(query, records)

def delete_movers_data():
    with engine.begin() as connection:
        connection.execute(
            text("DELETE FROM market_movers")
        )


def get_latest_movers_date():
    query = text("""
        SELECT MAX(snapshot_at)
        FROM market_movers
    """)

    with engine.connect() as connection:
        return connection.execute(query).scalar_one_or_none()

def get_market_movers_from_db(category: str):
    query = text("""
            SELECT *
            FROM market_movers
            WHERE category = :category
        """)
    
    with engine.connect() as connection:
        return connection.execute(
            query,
           {
                "category": category
            }
        ).mappings().all()
        
