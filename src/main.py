from src.mercadona.mercadona_scrapper import MercadonaScrapper
import pandas as pd
import os

scrapper = MercadonaScrapper()
mercadona_raw_data = scrapper.get_products()

mercadona_df = pd.DataFrame.from_dict(mercadona_raw_data)

mercadona_df.to_csv(os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), r'\raw_data\mercadona_data.csv'), sep=';')

if __name__ == "__main__":
    print("main")