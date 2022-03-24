import json

from pricing.config.boto3_config import ConfigureClient
import pricing.utils.extract as extract
import pricing.utils.mapping as mapping
from pricing.price import AWSPricer

class RDS:
    def __init__(self):
        self.client = ConfigureClient().client

    # MySQL
    def get_db_instance_price(self, region, instance_type, deployment_option):
        try:
            filters = [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
                {'Type': 'TERM_MATCH', 'Field': 'deploymentOption', 'Value': deployment_option},
                {'Type': 'TERM_MATCH', 'Field': 'databaseEngine', 'Value': 'MySQL'},
                {'Type': 'TERM_MATCH', 'Field': 'termType', 'Value': 'OnDemand'},
            ]

            pricer = AWSPricer()
            price_list = pricer.get_prices('AmazonRDS', filters)

            if len(price_list) == 0:
                return 0

            price_per_hour = float(price_list[0][0])

        except Exception as e:
            print(str(e))

        return price_per_hour

    def get_storage_price(self, region, volume_type, deployment_option, storage_amount):
        try:
            filters = [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': volume_type}
            ]

            pricer = AWSPricer()
            price_list = pricer.get_prices('AmazonRDS', filters)
            price_per_gb = float(price_list[0][0])

            if deployment_option == "Multi-AZ":
                price_per_gb = (price_per_gb * 2) - 0.001

            price = price_per_gb * storage_amount

        except Exception as e:
            print(str(e))

        return price

    def calc_total_cost(self, instance_cost, storage_cost):
        # calculate monthly costs - 730 hours in a month
        instance_cost_per_month = instance_cost * 730

        return instance_cost_per_month + storage_cost


def main():
    rds = RDS()
    region = "EU (Ireland)"
    instance_type = "db.m1.large"
    deployment_option = "Single-AZ"
    volume_type = "Provisioned IOPS (SSD)"
    instance_cost = rds.get_db_instance_price(region, instance_type, deployment_option)
    storage_cost = rds.get_storage_price(region, volume_type, deployment_option)
    print(instance_cost)
    print(storage_cost)

#main()