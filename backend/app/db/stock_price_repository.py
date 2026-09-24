from sqlalchemy import text
import datetime 
from app.db.database import engine



def save_stock_prices(prices, company_id, source):

    query = text("""
        INSERT INTO stock_prices (
            company_id,
            date,
            open,
            high,
            low,
            close,
            volume,
            change,
            change_percent,
            vwap,
            source,
            created_at
        )
        VALUES (
            :company_id,
            :date,
            :open,
            :high,
            :low,
            :close,
            :volume,
            :change,
            :change_percent,
            :vwap,
            :source,
            :created_at
        )
        ON CONFLICT (company_id, date)
        DO UPDATE SET
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume,
            change = EXCLUDED.change,
            change_percent = EXCLUDED.change_percent,
            vwap = EXCLUDED.vwap;
    """)
    records = [
        {
            "company_id": company_id,
            "date": price["date"],
            "open": price["open"],
            "high": price["high"],
            "low": price["low"],
            "close": price["close"],
            "volume": price["volume"],
            "change": price.get("change"),
            "change_percent": price.get("changePercent"),
            "vwap": price.get("vwap"),
            "source": source,
            "created_at": datetime.datetime.utcnow()
        }
        for price in prices
    ]

    with engine.begin() as connection:
        connection.execute(
            query,
            records
        )

def get_stock_prices_from_db(
    company_id: int,
    start_date,
    end_date
):
    query = text("""
        SELECT *
        FROM stock_prices
        WHERE company_id = :company_id
          AND date BETWEEN :start_date AND :end_date
        ORDER BY date ASC
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "company_id": company_id,
                "start_date": start_date,
                "end_date": end_date
            }
        ).mappings().all()

    return result

def get_latest_stock_price_date(company_id:int):
    query = text("""
        SELECT MAX(date)
        FROM stock_prices
        WHERE company_id = :company_id
    """)

    with engine.connect() as connection:
        return connection.execute(
            query,
            {"company_id": company_id}
        ).scalar_one_or_none()


def get_company_performance_db(company_id: int):
    query = text("""
        WITH prices AS (
            SELECT
                date,
                close,
                high,
                low,
                volume,
                vwap
            FROM stock_prices
            WHERE company_id = :company_id
        ),

        latest AS (
            SELECT *
            FROM prices
            ORDER BY date DESC
            LIMIT 1
        ),

        previous AS (
            SELECT *
            FROM prices
            WHERE date < (SELECT date FROM latest)
            ORDER BY date DESC
            LIMIT 1
        ),

        month_ago AS (
            SELECT *
            FROM prices
            WHERE date <= (
                (SELECT date FROM latest) - INTERVAL '1 month'
            )
            ORDER BY date DESC
            LIMIT 1
        ),

        three_months_ago AS (
            SELECT *
            FROM prices
            WHERE date <= (
                (SELECT date FROM latest) - INTERVAL '3 months'
            )
            ORDER BY date DESC
            LIMIT 1
        ),

        six_months_ago AS (
            SELECT *
            FROM prices
            WHERE date <= (
                (SELECT date FROM latest) - INTERVAL '6 months'
            )
            ORDER BY date DESC
            LIMIT 1
        ),

        year_ago AS (
            SELECT *
            FROM prices
            WHERE date <= (
                (SELECT date FROM latest) - INTERVAL '1 year'
            )
            ORDER BY date DESC
            LIMIT 1
        )

        SELECT
            latest.date,
            latest.close,
            latest.high,
            latest.low,
            latest.volume,
            latest.vwap,

            previous.close AS previous_close,
            month_ago.close AS month_ago_close,
            three_months_ago.close AS three_months_ago_close,
            six_months_ago.close AS six_months_ago_close,
            year_ago.close AS year_ago_close

        FROM latest
        LEFT JOIN previous ON TRUE
        LEFT JOIN month_ago ON TRUE
        LEFT JOIN three_months_ago ON TRUE
        LEFT JOIN six_months_ago ON TRUE
        LEFT JOIN year_ago ON TRUE
    """)

    with engine.connect() as connection:
        return connection.execute(
            query,
            {"company_id": company_id}
        ).mappings().first()
