import difflib as dl
import json
import pprint

from pricing.config.boto3_config import ConfigureClient
import pricing.utility.extract as extract
import pricing.utility.mapping as mapping


class EC2:
    def __init__(self):
        self.client = ConfigureClient().client
        self.region_mapping_dict = mapping.region_mapping_dict

    def get_instance_price(self, os, instance_type, region):
        for key, value in self.region_mapping_dict.items():
            if region == key:
                region_name = value
                break

        ec2_price_per_hour = 0
        try:
            box_usage = mapping.box_usage
            usage_type = box_usage[region] + instance_type

            data = self.client.get_products(ServiceCode='AmazonEC2', Filters=
            [
                {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': os},
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region_name},
                {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
                {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'},
                {'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': 'used'},
                {'Type': 'TERM_MATCH', 'Field': 'usagetype', 'Value': usage_type},
                {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Compute Instance'},
                {'Type': 'TERM_MATCH', 'Field': 'licenseModel', 'Value': "No License required"},
            ])

            for value in data['PriceList']:
                json_value = json.loads(value)

            price = extract.extract_values(json_value, 'USD')
            ec2_price_per_hour = price[0]

        except Exception as e:
            print(str(e))

        return ec2_price_per_hour

    def get_instance_price2(self, region, os, vcpu, memory):
        for key, value in self.region_mapping_dict.items():
            if region == key:
                region_name = value
                break
        ec2_price_per_hour = 0
        try:
            data = self.client.get_products(ServiceCode='AmazonEC2', Filters=
            [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region_name},
                {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                {'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': 'used'},
                {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'},
                {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': os},
                {'Type': 'TERM_MATCH', 'Field': 'vcpu', 'Value': vcpu},
                {'Type': 'TERM_MATCH', 'Field': 'memory', 'Value': memory},
                {'Type': 'TERM_MATCH', 'Field': 'licenseModel', 'Value': "No License required"},
                {'Type': 'TERM_MATCH', 'Field': 'storage', 'Value': "EBS only"},
            ])

            prices = []
            for value in data['PriceList']:
                json_value = json.loads(value)
                prices.append(extract.extract_values(json_value, 'USD'))

            instance_types = []
            for d in data['PriceList']:
                v = json.loads(d)
                instance_types.append(extract.extract_values(v, 'instanceType'))

            price = extract.extract_values(json_value, 'USD')
            p = sorted(i for i in prices if float(i[0]) > 0.0000)

            ec2_price_per_hour = p[0][0]
           # instance =

        except Exception as e:
            print(str(e))

        return ec2_price_per_hour


def main():
    os = 'Windows'
    instance_type = 't3.large'
    region = 'us-east-2'
    vcpu = '8'
    memory = '32 GiB'

    ec2 = EC2()
    value = ec2.get_instance_price(os, instance_type, region)
    value = ec2.get_instance_price2(region, os, vcpu, memory)
    cost_per_month = float(value) * 730
    print("%.2f" % cost_per_month)


#main()
