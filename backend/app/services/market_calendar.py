from typing import Optional
import pandas as pd
import exchange_calendars as xcals
from datetime import date, datetime, timedelta,timezone
from zoneinfo import ZoneInfo


def get_latest_market_date():
    calendar = xcals.get_calendar("XNYS")

    now = datetime.now(ZoneInfo("America/New_York"))
    today = pd.Timestamp(now.date())

    if calendar.is_session(today):
        close_time = calendar.session_close(today).to_pydatetime()

        if now >= close_time.astimezone(
            ZoneInfo("America/New_York")
        ):
            return today.date()

    previous_sessions = calendar.sessions_in_range(
        today - pd.Timedelta(days=10),
        today - pd.Timedelta(days=1),
    )

    return previous_sessions[-1].date()

def should_check_for_new_quarter(latest_db_date: Optional[date], finance_type: str) -> bool :
    if latest_db_date is None:
        return True
    
    today = datetime.now(
        ZoneInfo("America/New_York")
    ).date()
    if finance_type == "quarter":

        # Determine the next quarter's first month
        current_quarter = (latest_db_date.month - 1) // 3 + 1

        if current_quarter == 4:
            next_quarter_month = 1
            next_year = latest_db_date.year + 1
        else:
            next_quarter_month = current_quarter * 3 + 1
            next_year = latest_db_date.year

        check_date = date(
            next_year,
            next_quarter_month,
            15
        )

        return today >= check_date

    elif finance_type == "annual":

        check_date = date(
            latest_db_date.year + 1,
            2,
            15
        )

        return today >= check_date

    return False

def seconds_until_market_close():
    nyse = xcals.get_calendar("XNYS")

    now = datetime.now(ZoneInfo("America/New_York"))
    today = now.date()

    if not nyse.is_session(today):
        return None

    market_close = nyse.session_close(today).to_pydatetime()

    return max(
        0,
        int(
            (
                market_close.astimezone(ZoneInfo("America/New_York"))
                - now
            ).total_seconds()
        ),
    )

def should_refresh_financial_data(last_updated, report_type):
    if last_updated is None:
        return True

    now = datetime.now(timezone.utc)

    if last_updated.tzinfo is None:
        last_updated = last_updated.replace(tzinfo=timezone.utc)

    if report_type == "quarter":
        refresh_interval = timedelta(days=28)

    elif report_type == "annual":
        refresh_interval = timedelta(days=150)

    else:
        return False

    return now - last_updated >= refresh_interval