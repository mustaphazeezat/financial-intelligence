from app.services.ingestion_service import IngestionService


def main():
    service = IngestionService()

    # service.ingest_company_data()
    # service.ingest_movers_data()
    # service.ingest_stock__price_data()
    #service.ingest_income_statements_data("AAPL")
    service.ingest_balance_sheet_data("AAPL")
    service.ingest_cash_flow_data("AAPL")


if __name__ == "__main__":
    main()