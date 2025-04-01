from fastapi import APIRouter, Request, HTTPException
import boto3
from botocore.exceptions import ClientError

router = APIRouter()

@router.post("/list_buckets")
async def list_buckets(request: Request):
    data = await request.json()
    aws_access_key = data.get("aws_access_key")
    aws_secret_key = data.get("aws_secret_key")
    region = data.get("region", "us-east-1")
    if not aws_access_key or not aws_secret_key:
        raise HTTPException(status_code=400, detail="Missing AWS credentials")
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        response = s3_client.list_buckets()
        buckets = [bucket["Name"] for bucket in response.get("Buckets", [])]
        return {"buckets": buckets}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/list_ec2_instances")
async def list_ec2_instances(request: Request):
    data = await request.json()
    aws_access_key = data.get("aws_access_key")
    aws_secret_key = data.get("aws_secret_key")
    region = data.get("region", "us-east-1")
    if not aws_access_key or not aws_secret_key:
        raise HTTPException(status_code=400, detail="Missing AWS credentials")
    try:
        ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        response = ec2_client.describe_instances()
        instance_ids = []
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_ids.append(instance.get("InstanceId"))
        return {"instances": instance_ids}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
