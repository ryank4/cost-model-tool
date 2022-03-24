import json

from pricing.config.boto3_config import ConfigureClient
import pricing.utils.extract as extract
import pricing.utils.mapping as mapping
from pricing.price import AWSPricer


def add_metric_values(price_dict, value_range, key):
    index = 0
    len_value_range = 4

    if key == 'price':
        for b in sorted(value_range, reverse=True):
            price_dict[index][key] = b
            index += 1

    else:
        for b in value_range:
            # explicitly cast b to int to make comparison work
            if b.isnumeric():
                b = int(b)
                price_dict[index][key] = b
                # the tier ranges are not being sorted correctly
                # therefore we need to manually sort it
                if 0 < index < len_value_range:
                    if b < price_dict[index - 1][key]:
                        # swap the prices
                        price_dict[index][key] = price_dict[index - 1][key]
                        price_dict[index - 1][key] = b
            else:
                price_dict[index][key] = b
            index += 1

    return price_dict


def add_log_values(price_dict, value_range, key):
    index = 0

    if key == 'price':
        for b in sorted(value_range, reverse=True):
            price_dict[index][key] = b
            index += 1

    else:
        for b in sorted(value_range):
            price_dict[index][key] = b
            index += 1

    return price_dict

'''
Calculate the costs by tier
Cloudwatch pricing tier information: https://aws.amazon.com/cloudwatch/pricing/
'''
def calc_log_cost(storage_prices, amount):
    first_10tb = int(storage_prices[0]['endRange'])
    first_10tb_price = float(storage_prices[0]['price'])

    next20tb = int(storage_prices[1]['endRange'])
    next20tb_price = float(storage_prices[1]['price'])

    next20tb2 = int(storage_prices[2]['endRange'])
    next20tb_price2 = float(storage_prices[2]['price'])

    over_50tb = int(storage_prices[3]['beginRange'])
    over_50tb_price = float(storage_prices[3]['price'])
    amount = float(amount)
    cost = 0

    if amount <= first_10tb:
        cost += amount * first_10tb_price
        return cost
    else:
        cost += first_10tb * first_10tb_price

    if first_10tb < amount <= next20tb:
        cost += (amount - first_10tb) * next20tb_price
        return cost
    else:
        cost += (next20tb - first_10tb) * next20tb_price

    if next20tb < amount <= next20tb2:
        cost += (amount - next20tb) * next20tb_price2
        return cost
    else:
        cost += (next20tb2 - next20tb) * next20tb_price2

    if amount > over_50tb:
        cost += abs(amount - over_50tb) * over_50tb_price

    return cost


def calc_metric_cost(metric_price_dict, num_metrics):
    tier1 = int(metric_price_dict[0]['endRange'])
    tier1_price = float(metric_price_dict[0]['price'])

    tier2 = int(metric_price_dict[1]['endRange'])
    tier2_price = float(metric_price_dict[1]['price'])

    tier3 = int(metric_price_dict[2]['endRange'])
    tier3_price = float(metric_price_dict[2]['price'])

    tier4 = int(metric_price_dict[3]['beginRange'])
    tier4_price = float(metric_price_dict[3]['price'])

    amount = float(num_metrics)
    cost = 0

    if amount <= tier1:
        cost += amount * tier1_price
        return cost
    else:
        cost += tier1 * tier1_price

    if tier1 < amount <= tier2:
        cost += (amount - tier1) * tier2_price
        return cost
    else:
        cost += (tier2 - tier1) * tier2_price

    if tier2 < amount <= tier3:
        cost += (amount - tier2) * tier3_price
        return cost
    else:
        cost += (tier3 - tier2) * tier3_price

    if amount > tier4:
        cost += abs(amount - tier4) * tier4_price

    return cost


def calc_total_log_cost(logs_ingested, storage_cost):
    # price of logs ingested plus the monthly storage cost
    return logs_ingested + storage_cost


class CloudWatch:
    def __init__(self):
        self.client = ConfigureClient().client
        self.pricer = AWSPricer()

    def price_helper(self, filters):
        try:
            price_list = self.pricer.get_prices('AmazonCloudWatch', filters)

            if len(price_list) == 0:
                return 0

            price_per_metric = float(price_list[0][0])

        except Exception as e:
            print(str(e))

        return price_per_metric

    def get_metric_price(self, region, num_metrics):
        data = self.client.get_products(ServiceCode='AmazonCloudWatch', Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'group', 'Value': 'Metric'},
        ])

        for value in data['PriceList']:
            json_values = json.loads(value)

        # a range of values is expected
        begin_range = extract.item_generator(json_values, 'beginRange')
        end_range = extract.item_generator(json_values, 'endRange')
        prices = extract.item_generator(json_values, 'USD')

        # create and initialise price dict of dicts
        metric_price_dict = {}
        for i in range(4):
            metric_price_dict.setdefault(i, {})

        # add values to the dictionary in the correct order
        add_metric_values(metric_price_dict, begin_range, 'beginRange')
        add_metric_values(metric_price_dict, end_range, 'endRange')
        add_metric_values(metric_price_dict, prices, 'price')

        price = calc_metric_cost(metric_price_dict, num_metrics)

        return price

    def api_get_metric_data(self, region, num_metrics):
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'operation', 'Value': 'GetMetricData'}
        ]

        price_per_metric = self.price_helper(filters)
        price = price_per_metric * float(num_metrics)

        return price

    def api_get_metric_widget_image(self, region, num_metrics):
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'operation', 'Value': 'GetMetricWidgetImage'}
        ]

        price_per_metric = self.price_helper(filters)
        price = price_per_metric * float(num_metrics)

        return price

    def standard_log_ingested(self, region, num_metrics):
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'group', 'Value': 'Ingested Logs'}
        ]

        price_per_metric = self.price_helper(filters)
        price = price_per_metric * float(num_metrics)

        return price

    def log_storage(self, region, num_standard_logs, num_vended_logs):
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'storageMedia', 'Value': 'Amazon S3'}
        ]

        price_per_metric = self.price_helper(filters)
        compression_factor = 0.15
        total_logs = float(num_standard_logs) + float(num_vended_logs)
        price = price_per_metric * compression_factor * total_logs

        return price

    def logs_delivered(self, region, destination, amount):
        if destination == "Amazon S3":
            data = self.client.get_products(ServiceCode='AmazonCloudWatch', Filters=[
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'group', 'Value': 'Delivered Logs'},
                {'Type': 'TERM_MATCH', 'Field': 'logsDestination', 'Value': destination}
            ])
        else:
            data = self.client.get_products(ServiceCode='AmazonCloudWatch', Filters=[
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'logsDestination', 'Value': destination}
            ])

        for value in data['PriceList']:
            json_values = json.loads(value)

        # a range of values is expected
        begin_range = extract.item_generator(json_values, 'beginRange')
        end_range = extract.item_generator(json_values, 'endRange')
        prices = extract.item_generator(json_values, 'USD')

        # create and initialise price dict of dicts
        log_price_dict = {}
        for i in range(4):
            log_price_dict.setdefault(i, {})

        # add values to the dictionary in the correct order
        add_log_values(log_price_dict, begin_range, 'beginRange')
        add_log_values(log_price_dict, end_range, 'endRange')
        add_log_values(log_price_dict, prices, 'price')

        price = calc_log_cost(log_price_dict, amount)

        return price

    def parquet_conversion(self, region, num_metrics):
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'operation', 'Value': 'ParquetConversion'}
        ]

        price_per_metric = self.price_helper(filters)
        price = round(price_per_metric * float(num_metrics), 2)

        return price


def main():
    cw = CloudWatch()
    region = "US East (Ohio)"
    num_metrics = 21000
    #   get_metric = cw.api_get_metric_data(region, num_metrics)
    #   get_metric_image = cw.api_get_metric_widget_image(region, num_metrics)
    #   print(get_metric)
    #  print(get_metric_image)

    #  metrics = cw.get_metric_price(region, num_metrics)
    # print(metrics)
    print(cw.logs_delivered(region, "CloudWatch-Logs", 73000))
    logs_ingested = cw.standard_log_ingested(region, num_metrics)
    storage = cw.log_storage(region, num_metrics)
    #print(calc_total_log_cost(logs_ingested, storage))
    p = cw.parquet_conversion(region, num_metrics)
   # print(p)


#main()
