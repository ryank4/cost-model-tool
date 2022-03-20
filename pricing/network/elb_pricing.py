import json

from pricing.config.boto3_config import ConfigureClient
import pricing.utils.extract as extract
import pricing.utils.mapping as mapping
from pricing.price import AWSPricer

class ELB:
    def __init__(self):
        self.client = ConfigureClient().client

    # Network Load Balancer
    def get_price_per_nlb_hour(self, region):
        try:
            filters = [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'operation', 'Value': 'LoadBalancing:Network'},
            ]

            pricer = AWSPricer()
            price_list = pricer.get_prices('AWSELB', filters)
            price_list = sorted(price_list, reverse=True)
            price_dict = {"NLB-hour": price_list[0], "NLCU-hour": price_list[1]}

        except Exception as e:
            print(str(e))

        return price_dict

    def calc_nlb_charge(self, region):
        prices = self.get_price_per_nlb_hour(region)
        nlb = float(prices['NLB-hour'][0])

        price_per_month = nlb * 730

        return price_per_month

    def calc_tcp_traffic(self, region, bytes_processes, new_connections, connection_duration):
        prices = self.get_price_per_nlb_hour(region)
        nlcu = float(prices['NLCU-hour'][0])

        # LCU = Load Capacity Unit
        processed_bytes_lcu = bytes_processes / 1
        new_connections_lcu = new_connections / 800
        active_connections_lcu = (new_connections * connection_duration) / 100000

        max_lcu = max(processed_bytes_lcu, new_connections_lcu, active_connections_lcu)

        price_per_hour = max_lcu * nlcu

        price_per_month = price_per_hour * 730

        return price_per_month

    def calc_udp_traffic(self, region, bytes_processes, new_connections, connection_duration):
        prices = self.get_price_per_nlb_hour(region)
        nlcu = float(prices['NLCU-hour'][0])

        # LCU = Load Capacity Unit
        processed_bytes_lcu = bytes_processes / 1
        new_connections_lcu = new_connections / 400
        active_connections_lcu = (new_connections * connection_duration) / 50000

        max_lcu = max(processed_bytes_lcu, new_connections_lcu, active_connections_lcu)

        price_per_hour = max_lcu * nlcu

        price_per_month = price_per_hour * 730

        return price_per_month

    def calc_tls_traffic(self, region, bytes_processes, new_connections, connection_duration):
        prices = self.get_price_per_nlb_hour(region)
        nlcu = float(prices['NLCU-hour'][0])

        # LCU = Load Capacity Unit
        processed_bytes_lcu = bytes_processes / 1
        new_connections_lcu = new_connections / 50
        active_connections_lcu = (new_connections * connection_duration) / 3000

        max_lcu = max(processed_bytes_lcu, new_connections_lcu, active_connections_lcu)

        price_per_hour = max_lcu * nlcu

        price_per_month = price_per_hour * 730

        return price_per_month

    def calc_total_nlcu_charge(self, tcp, udp, tls):
        return tcp + udp + tls

    def calc_total_monthly_cost(self, nlb_cost, nlcu_cost):
        return round(nlb_cost + nlcu_cost, 2)

def main():
    elb = ELB()
    region = "US East (N. Virginia)"
    tcp = elb.calc_tcp_traffic(region, 1.08, 3, 120)
    udp = elb.calc_udp_traffic(region, 1.08, 3, 120)
    tls = elb.calc_tls_traffic(region, 1.08, 3, 120)
    nlcu = elb.calc_total_nlcu_charge(tcp, udp, tls)
    nlb = elb.calc_nlb_charge(region)
    total = elb.calc_total_monthly_cost(nlb, nlcu)
    print(total)

main()