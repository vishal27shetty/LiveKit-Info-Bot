from flask import Flask
from flask_restx import Resource, Api
from livekit import api as lk_api
import os 
import asyncio
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

@api.route('/api/token')
class CreateRoom(Resource):
    def get(self):
        async def create_room():
            async with lk_api.LiveKitAPI() as lkapi:
                await lkapi.room.create_room(
                    lk_api.CreateRoomRequest(
                        name="info-bot-2",
                        empty_timeout=10 * 60,
                        max_participants=20,
                    )
                )
        asyncio.run(create_room())
    
        token = lk_api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
            .with_identity("agent-AJ_GCTNz4waAwhE") \
            .with_name("info-agent") \
            .with_grants(lk_api.VideoGrants(
                room_join=True,
                room="info-bot-2",
            )).to_jwt()

        return {"token": token}


if __name__ == '__main__':
    app.run(debug=True)



    
