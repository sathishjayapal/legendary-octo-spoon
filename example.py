import boto3

s3 = boto3.client("s3")
sts = boto3.client("sts")


def lambda_handler(event, context):
    print("identity:", sts.get_caller_identity()["Arn"])

    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        print(f"reading file from bucket={bucket!r} key={key!r}")

        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read()
            content_type = response.get('ContentType', 'unknown')
            file_size = len(content)

            print(f"File: {key}")
            print(f"Size: {file_size} bytes")
            print(f"Content-Type: {content_type}")

            # Try to decode as text, otherwise show as binary
            try:
                text_content = content.decode('utf-8')
                print(f"Content:\n{text_content}")
            except UnicodeDecodeError:
                print(f"Content (binary): {content[:100]}...")  # Show first 100 bytes

        except Exception as e:
            print(f"Error reading file {key}: {e}")

    return {"ok": True}

