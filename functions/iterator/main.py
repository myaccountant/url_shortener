import zipfile
import zlib
import io
import boto3

PYTHON_FILE = 'main.py'
FUNCTION_NAME = 'shortener_iterator'
I = 10

def handle(event, context):

    # Load this code into a string
    with open(PYTHON_FILE, 'r') as myfile:
        data = myfile.read()

    # Increment I in the version of this code to be zipped
    data = data.replace(f"I = {str(I)}", f"I = {str(I + 1)}")

    zipBuffer = io.BytesIO()

    # Zip up this code to an in-memory buffer
    with zipfile.ZipFile(zipBuffer, 'w', zipfile.ZIP_DEFLATED) as iteratorZip:
        filename = zipfile.ZipInfo(PYTHON_FILE)

        # give full access to included file
        filename.external_attr = 0o755 << 16

        iteratorZip.writestr(filename, data)

    awsLambda = boto3.client('lambda')

    response = awsLambda.update_function_code(
        FunctionName=FUNCTION_NAME,
        ZipFile=zipBuffer.getvalue(),
        Publish=True,
        DryRun=False
    )

    return {
        'statusCode': 200,
        'body': str(I)
    }
