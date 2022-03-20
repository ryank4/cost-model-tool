import json

from pricing.config.boto3_config import ConfigureClient
from pricing.utils import mapping, extract


class AWSPricer:
    def __init__(self):
        self.client = ConfigureClient().client
        self.region_mapping_dict = mapping.region_mapping_dict

    def get_prices(self, service, filters):
        prices = []
        try:
            data = self.client.get_products(ServiceCode=service, Filters=filters)

            for value in data['PriceList']:
                json_value = json.loads(value)
                prices.append(extract.extract_values(json_value, 'USD'))
               # prices.append(extract.item_generator(json_value, 'USD'))

        except Exception as e:
            print(str(e))

        return prices
