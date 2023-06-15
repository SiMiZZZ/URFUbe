import boto3
session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    endpoint_url='https://hb.bizmrg.com',
    aws_access_key_id='f49g9cz4r1TNbBSfQu1g4S',
    aws_secret_access_key='eYofqqYRtFy5SrZpWuhPe72tQPQhDDyhZuzzmLkG94vQ'
)


bucket_name = "urfube"


url = s3_client.generate_presigned_url(ClientMethod='get_object',
                                                      Params={
                                                          'Bucket': "urfube",
                                                          'Key': "Коты.mp4"
                                                      })

print(url)