## Import and use boto3 library and classes Game and GameMapping
import boto3

from entities import Game, UserGameMapping


#Initialise a var for dynamo db table
dynamodb = boto3.client('dynamodb')

#Create a const for game id string literal
GAME_ID = "3d4285f0-e52b-401a-a59b-112b38c4a26b"

#Function for retrieving all users in game
def fetch_game_and_users(game_id):
    resp = dynamodb.query(
        TableName='battle-royale',
        KeyConditionExpression="PK = :pk AND SK BETWEEN :metadata AND :users",
        ExpressionAttributeValues={
            ":pk": { "S": "GAME#{}".format(game_id) },
            ":metadata": { "S": "#METADATA#{}".format(game_id) },
            ":users": { "S": "USER$" },
        },
        ScanIndexForward=True
    )

#set variable game to a new instance of Game passing in the response from dynamo 
    game = Game(resp['Items'][0])
#set instance variable users equal to an array of UserGameMapping 
    game.users = [UserGameMapping(item) for item in resp['Items'][1:]]

    return game


game = fetch_game_and_users(GAME_ID)

print(game)
for user in game.users:
    print(user)

