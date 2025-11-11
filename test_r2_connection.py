import os
import boto3
from dotenv import load_dotenv

load_dotenv()

def test_r2_connection():
    """Test R2 connection and credentials."""
    try:
        account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        access_key = os.getenv('R2_ACCESS_KEY_ID')
        secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
        bucket_name = os.getenv('R2_BUCKET_NAME')

        print(f"Account ID: {account_id}")
        print(f"Bucket: {bucket_name}")
        print(f"Access Key: {access_key[:8]}...")

        # Initialize R2 client
        s3_client = boto3.client(
            's3',
            endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='auto'
        )

        # Test 1: List buckets
        print("\n1. Testing bucket listing...")
        response = s3_client.list_buckets()
        buckets = [b['Name'] for b in response['Buckets']]
        print(f"✓ Found buckets: {buckets}")

        # Test 2: Check if our bucket exists
        if bucket_name in buckets:
            print(f"✓ Bucket '{bucket_name}' exists")
        else:
            print(f"✗ Bucket '{bucket_name}' not found")
            return False

        # Test 3: List objects in bucket
        print("\n2. Testing object listing...")
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name)
            objects = response.get('Contents', [])
            print(f"✓ Found {len(objects)} objects in bucket")
            if objects:
                print("Objects:")
                for obj in objects[:3]:  # Show first 3
                    print(f"  - {obj['Key']}")
        except Exception as e:
            print(f"✗ Error listing objects: {str(e)}")

        print("\n✓ R2 connection test passed!")
        return True

    except Exception as e:
        print(f"\n✗ R2 connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_r2_connection()