import json

from pricing.config.boto3_config import ConfigureClient
import pricing.utility.extract as extract
import pricing.utility.mapping as mapping


def add_values(storage_dict, value_range, key):
    storage_dict = storage_dict

    index = 0
    for b in sorted(value_range):
        storage_dict[index][key] = b
        index += 1

    return storage_dict


class S3:
    def __init__(self):
        self.client = ConfigureClient().client
        self.region_mapping_dict = mapping.region_mapping_dict

    def put_copy_post_list_requests_price(self, region):
        try:
            data = self.client.get_products(ServiceCode='AmazonS3', Filters=
            [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'groupDescription', 'Value': 'PUT/COPY/POST or LIST requests'}
            ])

            for value in data['PriceList']:
                json_value = json.loads(value)

            price = extract.extract_values(json_value, 'USD')

        except Exception as e:
            print(str(e))
            return "Error retrieving price"

        return price

    def get_select_requests_price(self, region):
        try:
            data = self.client.get_products(ServiceCode='AmazonS3', Filters=
            [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'groupDescription', 'Value': 'GET and all other requests'}
            ])

            for value in data['PriceList']:
                json_value = json.loads(value)

            price = extract.extract_values(json_value, 'USD')

        except Exception as e:
            print(str(e))
            return "Error retrieving price"

        return price

    def put_storage_prices(self, region):
        try:
            data = self.client.get_products(ServiceCode='AmazonS3', Filters=
            [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'storageClass', 'Value': 'General Purpose'},
            ])

            for value in data['PriceList']:
                json_values = json.loads(value)

            begin_range = extract.item_generator(json_values, 'beginRange')
            end_range = extract.item_generator(json_values, 'endRange')
            price = extract.item_generator(json_values, 'USD')

            general_purpose_storage = {}
            for i in range(3):
                general_purpose_storage.setdefault(i, {})

            add_values(general_purpose_storage, begin_range, 'beginRange')
            add_values(general_purpose_storage, end_range, 'endRange')
            add_values(general_purpose_storage, price, 'price')

        except Exception as e:
            print(str(e))
            return "Error retrieving price"

        return general_purpose_storage

    def get_data_returned_price(self, region):
        try:
            data = self.client.get_products(ServiceCode='AmazonS3', Filters=
            [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'groupDescription', 'Value': 'Data Returned by S3 Select in Standard'}
            ])

            for value in data['PriceList']:
                json_value = json.loads(value)

            price = extract.extract_values(json_value, 'USD')

        except Exception as e:
            print(str(e))
            return "Error retrieving price"

        return price

    def get_data_scanned_price(self, region):
        try:
            data = self.client.get_products(ServiceCode='AmazonS3', Filters=
            [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'groupDescription', 'Value': 'Data Scanned by S3 Select in Standard'}
            ])

            for value in data['PriceList']:
                json_value = json.loads(value)

            price = extract.extract_values(json_value, 'USD')

        except Exception as e:
            print(str(e))
            return "Error retrieving price"

        return price


def main():
    region = 'US East (Ohio)'

    s3 = S3()
    value = s3.put_copy_post_list_requests_price(region)
    print(value)
    value = s3.get_select_requests_price(region)
    print(value)
    value = s3.put_storage_prices(region)
    print(value)
    value = s3.get_data_returned_price(region)
    print(value)
    value = s3.get_data_scanned_price(region)
    print(value)


main()
