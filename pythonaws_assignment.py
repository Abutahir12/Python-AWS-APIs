# Importing the neccessary libraries
from flask import Flask, json, jsonify, request
import boto3

# Note : AWS user credentials below 
# Please add the access key id and secret access key by replacing the '--' 
# Make sure to use Postman to test the below code

s3_client=boto3.client('s3',
    aws_access_key_id='-------------------------',
    aws_secret_access_key='---------------------'
    )

s3_resource = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='-----------------------',
    aws_secret_access_key='--------------------'
)

app=Flask(__name__)

@app.route('/add/<string:newuser>', methods=['POST'])
def add_profile(newuser):
    """Create a user profile in S3 bucket 

            Creates a unique json file, if it already exists , it overwrites it

            :param newuser: newuser name , this will also be used as unique json file name
            :return: Success code and success message 
            :Revisions: Can be done in future 
    """
    new_users = []
    request_data=request.get_json()

    success = {
     "statusCode": 201,
     "body": "Requested data created successfully"
    }

    docs={
    "name": request_data['name'],
    "skills": [
        request_data['skills']
    ],
    "industry": request_data['industry'],
    "jobRole": request_data['jobRole'],
    "proficiencyLevel": request_data['proficiencyLevel'],
    "relocation": request_data['relocation'],
    "state": request_data['state'],
    "city": request_data['city'],
    "experience": request_data['experience'],
    "linkedinUrl": request_data['linkedinUrl'],
    "visibilityDuration": request_data['visibilityDuration']
    }
    try:
        #Creates a json file with the data you pass through the request
        s3_resource.Object('talentboardusers', newuser+'.json').put(Body=bytes(json.dumps(docs).encode('UTF-8')))
        new_users.append(docs)
    except Exception as e:
        return jsonify({'Error':'Please check the aws config'})
    return jsonify(success)

@app.route('/fetchdetails', methods=['GET'])
def fetch_details():
    """Fetches all the data from the aws s3 bucket

            Reads all the objects present in a specified bucket and fetches

            :params: None
            :return: Json format of all the details
            :Revisions: Can be done in future
    """
    details=[]
    bucket='talentboardusers'
    try:
        for obj in s3_resource.Bucket(bucket).objects.all():
            key = obj.key
            body = obj.get()['Body'].read()
            details.append(json.loads(body))
    except Exception as e:
        return jsonify({'Error':'Please check the aws config'})      
    return jsonify(details)

if __name__=='__main__':
    # run the app, feel free to pass port number to run() if you want, it's optional otherwise
	app.run(debug=True)
