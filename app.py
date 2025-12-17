from flask import Flask
from flask_restx import Resource, Api
from livekit import api as lk_api
import os 

app = Flask(__name__)
api = Api(app)

@api.route('/api/token')
class GetToken(Resource):
    def get(self):
        token = lk_api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
            .with_identity("identity-h8U3") \
            .with_name("name") \
            .with_grants(lk_api.VideoGrants(
                room_join=True,
                room="info-bot",
            )).to_jwt()

        return {"token": token}


if __name__ == '__main__':
    app.run(debug=True)



    
