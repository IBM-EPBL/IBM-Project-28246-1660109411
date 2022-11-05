from flask import Flask, redirect, url_for, render_template, request
import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT=""
COS_API_KEY_ID=" "
COS_INSTANCE_CRN=""

cos= ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT)

app=Flask(__name__)


@app.route('/')
def index():
    #files=get_bucket_contents()
    return render_template('index.html',files="files")