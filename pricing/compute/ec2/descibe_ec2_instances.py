import boto3

def describe_instance_types(instance_type):
    client = boto3.client('ec2')
    response = client.describe_instance_types(InstanceTypes=[instance_type])
    info = response['InstanceTypes']
    instance_type_info = {}
    for i in info:
        instance_type_info['vCPUs'] = i['VCpuInfo']['DefaultVCpus']
        instance_type_info['Memory'] = i['MemoryInfo']['SizeInMiB']
        instance_type_info['Network'] = i['NetworkInfo']['NetworkPerformance']
        try:
            gpu_info = i['GpuInfo']['Gpus']
            instance_type_info['GPUs'] = gpu_info[0]['Count']
        except KeyError:
            instance_type_info['GPUs'] = 'NA'

    return instance_type_info





