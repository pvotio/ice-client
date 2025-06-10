import pandas as pd
import requests

from config import logger
from utils import Request


class Engine:

    URL = "https://www.ice.com/api/cds-settlement-prices/icc-single-names"

    def __init__(self, max_retries: int, backoff_factor: int) -> None:
        self.request = Request(max_retries=max_retries, backoff_factor=backoff_factor)

    def fetch(self, content: str = None) -> pd.DataFrame:
        logger.debug(f"Attempting to fetch content from {self.URL}.")
        if not content:
            data = self.get_content()
            logger.debug(
                f"Successfully fetched content from {self.URL}. Now parsing the content."  # noqa: E501
            )
        else:
            logger.debug(
                "Successfully loaded the content from the user provided argument. Now parsing the content."  # noqa: E501
            )

        df = self.convert_to_df(data)
        logger.debug(f"\n{df}")
        self.validate_data(df)
        logger.info(f"Parsed content from {self.URL}. Extracted {len(df)} rows.")
        return df

    def get_content(self) -> str:
        try:
            r = self.request.request("GET", self.URL)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching content from {self.URL}. Error: {e}")
            raise ConnectionError(f"Failed to connect to {self.URL}.") from e

    def convert_to_df(self, data: list) -> pd.DataFrame:
        try:
            df = pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Error parsing HTML via pandas. Error: {e}")
            raise e

        if len(df):
            logger.debug(
                f"Successfully parsed content from {self.URL}. Extracted {len(df)} rows."  # noqa: E501
            )
            return df
        else:
            raise ValueError(f"No data found when parsing content from {self.URL}.")

    def validate_data(self, df: pd.DataFrame) -> None:
        if df["clearingDate"].str.contains("No data found").any() or not len(df):
            logger.error("Data validation failed")
            raise ValueError("No price data provided by the provider as of now.")

        logger.debug("Data validation succeeded.")
