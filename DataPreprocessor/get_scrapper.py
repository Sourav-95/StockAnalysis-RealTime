import sys
import io

class StockScrapper:
    def __init__(self, ticker_base:str):
        self.ticker_base = ticker_base

    def _scrapper_(self):
        # stock_info_dictionary = yf.Ticker(self.ticker_base)

        # Backup the original stdout and stderr
        stdout_backup = sys.stdout
        stderr_backup = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        try:
            scrapped_data = self.ticker_base.info

            # Get any output or error messages
            output = sys.stdout.getvalue()
            error_output = sys.stderr.getvalue()

            # Check for "404 Client Error" and pass if found
            if "404 Client Error" in error_output:
                pass
            else:
                return scrapped_data
        finally:
            sys.stdout = stdout_backup
            sys.stderr = stderr_backup

