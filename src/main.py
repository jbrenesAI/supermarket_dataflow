from src.mercadona.mercadona_scrapper import MercadonaScrapper
from src.mercadona.mercadona_processor import MercadonaProcessor
import pandas as pd
import os


if __name__ == "__main__":
    # r"../../raw_data/mercadona_data.csv"
    raw_data_path = os.path.join(os.getcwd(), r"../raw_data/mercadona_data.csv")

    # r"../../processed_data/processed_mercadona_data.csv"
    processed_data_path = os.path.join(os.getcwd(), r"../processed_data/processed_mercadona_data.csv")

    scrapper = MercadonaScrapper()
    mercadona_raw_data = scrapper.get_products()

    mercadona_df = pd.DataFrame.from_dict(mercadona_raw_data)

    mercadona_df.to_csv(raw_data_path,
                        sep=';',
                        encoding='utf-8',
                        index=False)

    processor = MercadonaProcessor(raw_data_path, processed_data_path)
    processor.process_data()


