import pandas as pd
import os
from typing import List

project_name = 'mercadona'


# TODO : Automate the upload of the csv file to GCS:
#  - https://stackoverflow.com/questions/36314797/write-a-pandas-dataframe-to-google-cloud-storage-or-bigquery
class MercadonaProcessor:
    def __init__(self, source_path, dst_path):
        self.mercadona_df = None
        self.source_path = source_path
        self.destination_path = os.path.join(os.getcwd(), dst_path)

    def process_data(self):
        self.read_raw_data()
        self.clean_product_name()
        self.clean_product_size()
        self.clean_price()
        self.clean_decimal_values()
        self.remove_redundant_data()
        self.define_schema()
        self.write_data(self.destination_path)

    def read_raw_data(self):
        print('\nReading {} raw data csv file'.format(project_name))
        self.mercadona_df = pd.read_csv(self.source_path,
                                        sep=';',
                                        encoding='utf-8')
        # If index column, remove it
        if self.mercadona_df.shape[1] == 3:
            self.mercadona_df = self.mercadona_df[self.mercadona_df.columns[1:]]

        self.original_shape = self.mercadona_df.shape
        print('{} raw data read with shape {}'.format(project_name, self.original_shape))

    def clean_product_name(self):
        print('\nSplitting product_name column into product_name, brand and product_size')
        name_split = self.mercadona_df['product_name'].str.split(',')
        self.mercadona_df['brand'] = name_split.str[-2]
        self.mercadona_df['product_size'] = name_split.str[-1]
        self.mercadona_df['product_name'] = name_split.str[:-2].str.join(',')
        print('product_name split finished')

    def clean_product_size(self):
        """
        ################ PRODUCT_SIZE FORMAT ###################
        [CONTAINER | CAPACITY | UNIT | .......]
        """
        print('\nSplitting product_size into container, capacity and unit')
        product_size_split = self.mercadona_df['product_size'].str.strip().str.split(' ')

        product_size_split = product_size_split.apply(lambda x: obtain_container_capacity_unit(x))

        self.mercadona_df['container'] = product_size_split.str[-3]
        self.mercadona_df['product_capacity'] = product_size_split.str[-2]
        self.mercadona_df['product_unit'] = product_size_split.str[-1]
        print('Product size split finished')

    def clean_price(self):
        """
        ################ PRICE_DESC COLUMN FORMAT ################
        - If product size == 1 [price per metric unit]
        - If product size != 1 [ unit price | 1 | METRIC UNIT | : | PRICE PER METRIC UNIT ] -> 8,95 1 KILO: 10,53 Euros
        """
        self.mercadona_df['price_desc'] = self.mercadona_df['price_desc'].str.replace('\n', ' ')
        self.mercadona_df['price_desc'] = self.mercadona_df['price_desc'].str.replace(':', '')
        price_desc_split = self.mercadona_df['price_desc'].str.split(' ')

        self.mercadona_df['product_price'] = price_desc_split
        self.mercadona_df['unitary_price'] = price_desc_split
        self.mercadona_df['product_price'] = self.mercadona_df['product_price'].apply(lambda x: x[0])
        self.mercadona_df['unitary_price'] = self.mercadona_df['unitary_price'].apply(
            lambda x: x[0] if len(x) == 1 else x[-2])
        self.mercadona_df['unitary_capacity'] = price_desc_split.apply(lambda x: None if len(x) == 1 else x[1])
        self.mercadona_df['unitary_price_unit'] = price_desc_split.apply(
            lambda x: None if len(x) == 1
            else [x[0], x[1]] if len(x) == 2 else x[2]
        )

    def clean_decimal_values(self):
        # SUBSTITUTE COMMA FOR DOTS AS DECIMAL SEPARATORS
        self.mercadona_df['unitary_price'] = self.mercadona_df['unitary_price'].str.replace(',', '.')
        self.mercadona_df['product_price'] = self.mercadona_df['product_price'].str.replace(',', '.')

    def remove_redundant_data(self):
        # REMOVE REDUNDANT DATA AND DEFINE SCHEMA
        self.mercadona_df = self.mercadona_df.drop(columns=['price_desc', 'product_size'])

    def define_schema(self):
        self.mercadona_df['product_capacity'] = self.mercadona_df['product_capacity'].astype('float64')
        self.mercadona_df['product_price'] = self.mercadona_df['product_price'].astype('float64')
        self.mercadona_df['unitary_price'] = self.mercadona_df['unitary_price'].astype('float64')

    def write_data(self, path):
        self.mercadona_df.to_csv(os.path.join(os.getcwd(), path),
                                 encoding='utf-8', index=False)

        self.processed_shape = self.mercadona_df.shape
        print('\nData saved. Original shape {} - final shape {}'.format(self.original_shape, self.processed_shape))
        print('\nData columns: {}'.format(self.mercadona_df.columns))
        print('\nData sample \n{}'.format(self.mercadona_df.head()))


def obtain_container_capacity_unit(product_size_split: List[str]):
    final_split = []

    if len(product_size_split) == 3:
        final_split = product_size_split
    elif len(product_size_split) == 1 and product_size_split[0].lower() == 'u':
        final_split = ['no-container or multiple container pack', 0, 'no-unit']
    else:
        for i in range(len(product_size_split)):
            elem = product_size_split[i]
            try:
                cast = int(elem)
                if product_size_split[i + 1].lower() in ['g', 'l', 'kg', 'ml', 'gr)']:
                    final_split = [product_size_split[i - 1], elem, product_size_split[i + 1]]
            except:
                pass

    return final_split


# r"../../raw_data/mercadona_data.csv"
src_path = os.path.join(os.getcwd(), r"../../raw_data/mercadona_data.csv")

# r"../../processed_data/processed_mercadona_data.csv"
dst_path = os.path.join(os.getcwd(), r"../../processed_data/processed_mercadona_data.csv")

mercadona_processor = MercadonaProcessor(src_path, dst_path)
mercadona_processor.process_data()
print(mercadona_processor.mercadona_df.head())
