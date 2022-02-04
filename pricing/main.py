from pricing.compute.ec2.ec2 import EC2

os = 'Windows'
instance_type = 't3a.xlarge'
region = 'eu-west-2'
ec2 = EC2()
value = ec2.get_instance_price(os, instance_type, region)
ec2_price1 = float(value) * 730
instance1 = "Instance 1 (EU)"

os = 'Linux'
instance_type = 't4g.xlarge'
region = 'us-east-2'
ec2 = EC2()
value = ec2.get_instance_price(os, instance_type, region)
ec2_price2 = float(value) * 730
instance2 = "Instance 2 (US)"

print("---------Price Per Month---------")
print("EC2 {0} price: {1}".format(instance1, ec2_price1))
print("EC2 {0} price: {1}".format(instance2, ec2_price2))

