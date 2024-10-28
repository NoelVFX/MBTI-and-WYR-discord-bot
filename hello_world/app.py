import json
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import discord
from discord.ext import commands
from discord import app_commands
from pprint import pprint
import base64
import requests
import random
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import boto3
from botocore.exceptions import ClientError
from discord_interactions import InteractionResponseType, InteractionType
from datetime import datetime
import uuid
from discord.ui import Button
from decimal import Decimal
from collections import defaultdict
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import aiohttp
import time

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
APPLICATION_ID = os.environ.get('DISCORD_APPLICATION_ID')
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME')
ALLOWED_CHANNEL_ID = '1210092511637544961'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)
user_sessions = {}

is_registered_commands = False

Qlist = ['Would you rather pet a 1. Dinosaur, 2. Dragon', 'Would you rather eat 1. Hot Soba, 2. Cold Soba', 'Would you rather always have to 1. Whisper, 2. Shout', 'Would you rather be famous for your 1. Dancing Skills, 2. Singing Skills', 'Would you rather never have to do 1. Laundry again, 2. Dishes again', 'Would you rather 1. Sing everytime you say, 2. Dance everytime you move', 'Would you rather 1. New Jeans, 2. Taylor Swift', 
         'Would you rather 1. Read mind, 2. Go invisible', 'Would you rather live without 1. Music, 2. Movies', 'Would you rather see 1. 10 minutes to the future, 2. 10 years to the future', 'Would you rather always feel 1. Too hot, 2. Too cold', 'Would you rather 1. Eat anything and never gain weight, 2. Will not feel tired and never need to sleep', 'Would you rather be the 1. Smartest person in the world, 2. Funniest person in the world',
         'Would you rather 1. Never use technology again, 2. Never leave your home again', 'Would you rather 1. Want personalized features even though personal data is collected, 2. Generic functionality but no data collection', 'Would you rather 1. Speak a new language fluently, 2. Talk to an animal', 'Would you rather 1. Can only tell the truth, 2. Always tell the lie', 'Would you rather 1. Unlimited money, 2. Unlimited knowledge', 
         'Would you rather live in a world 1. with no problems, 2. where you rule', 'Would you rather 1. Control time, 2. Change your appearance at will', 'Would you rather 1. Teleport anywhere instantly, 2. Read minds', 'Would you rather 1. Jojos Bizzare adventure, 2. Demon Slayer', 'Would you rather 1. Doge, 2. Nyan cat', 'Would you rather 1. Jake Paul, 2. Mike Tyson', 'Would you rather marrying a 1. Rich but toxic person, 2. Poor but loving person', 'Would you rather only watch 1. Anime, 2. K-dramas',
         'Would you rather pet be able to breathe 1. In water, 2. In space', 'Would you rather 1. Skincare, 2. Makeup', 'Would you rather 1. Superpower, 2. Magic', 'Would you rather 1. Autumn/winter, 2. Spring/summer', 'Would you rather 1. Always being late, 2. Always being early', 'Would you rather know 1. When you will die, 2. How you will die', 'Would you rather 1. To love, 2. To be loved', 'Would you rather 1. Cat person, 2. Dog person', 'Would you rather 1. Reincarnation, 2. Time Travel', 'Would you rather 1. Have unlimited friends but they all fake, 2. Have one friend who really care about you', 
         'Would you rather 1. IQ, 2. Photographic memory', 'Would you rather 1. Talk with your future self, 2. Speak to your past self', 'Would you rather 1. Cant listen to your favourite music, 2. Cant read your favourite books', 'Would you rather 1. Travel everywhere you want, 2. Never visit your town again', 'Would you rather 1. Have a comfortable job, 2. Own a high ranking company but have no control over it', 'Would you rather 1. Love, 2. Money', 'Would you rather 1. Friends, 2. Family', 'Would you rather 1. Be yourself, 2. Be someone else', 'Would you rather 1. Warm colors, 2. Cool colors', 'Would you rather 1. SamSung, 2. Apple']

quiz_data = {
         "questions": [
        {
            "question": "Friday's here and the gang's rallying for a night out. What's your move?",
            "choices": [
                "A. Home Hermit: \"Big nights out? Hard pass. I'm all about cozy evenings in.\"",
                "B. Maybe...: \"I'll see how I feel. Sometimes yes, but I need my downtime too.\"",
                "C. I'm Down!: \"Absolutely, I'm in! Hanging with friends is always a boost.\"",
                "D. LFG!!!!: \"Oh yes! Bring on the night - I'm here for all the fun and new faces!\""
            ]
        },
        {
            "question": "Friend-o-meter: What's your vibe in the wild?",
            "choices": [
                "A. Stealth Mode: \"I'm wallpaper with eyes-great at observing, not so much at mingling.\"",
                "B. Deep Diver: \"I dive deep into chats that grab my interest, usually one-on-one or in small crews.\"",
                "C. People Presence: \"I soak up the crowd's vibe without needing to dive into the mix.\"",
                "D. Social Butterfly: \"I'm all about chatting up new faces — socializing is my sport!\""
            ]
        },
        {
            "question": "Big win alert! How are you celebrating?",
            "choices": [
                "A. Solo mode activated: \"Quiet time for me — I savor wins solo style!\"",
                "B. Lowkey Vibes: \"Just the inner circle — small gatherings are my jam.\"",
                "C. Hit Up the 'Gram: \"Quick post to share the joy, then back to the grind!\"",
                "D. Full Send!: \"Big bash with everyone! If it's not shared, did it even happen?\""
            ]
        },
        {
            "question": "Thinking about the future... what's your pick?",
            "choices": [
                "A. Team Blueprint: \"All about solid plans and proven paths. Realism is my guide.\"",
                "B. Remix Mode: \"I remix the old with new twists for cool, practical innovations.\"",
                "C. Hybrid Hustle: \"I mix practical steps with bold, new ideas. Always eyeing the next big thing.\"",
                "D. Dream Weaver: \"I dream big and ask 'what if?', pushing boundaries beyond the usual.\""
            ]
        },
        {
            "question": "You're at the park with friends and it suddenly rains! What's the first thought you have?",
            "choices": [
                "A. Umbrella Check: \"Umbrella time? I quickly gauge the rain and seek shelter—always practical!\"",
                "B. Shirt Saver: \"Oh no, my white shirt! I'm on it — finding a dry spot ASAP.\"",
                "C. Idea Tsunami: \"Wow, this rain? Just like life's curveballs — always making me think on my feet.\"",
                "D. Connect-the-Dots Champ: \"Rainy days flood me with memories — each drop a reminder of past moments.\""
            ]
        },
        {
            "question": "You're playing a solo RPG game and you're facing the BOSS level now. How do you approach it?",
            "choices": [
                "A. Study & Win: \"I hit the books and guides to master the game plan before I play.\"",
                "B. Inventory Review: \"I check my gear and past wins to strategize my next move.\"",
                "C. I have a feeling I know what should happen. \"I follow my gut, tweaking my plan with a mix of instinct and insight.\"",
                "D. Just Try First! \"I dive right in and figure it out on the fly — adapt and overcome!\""
            ]
        },
        {
            "question": "Now you're playing a board game with 3 friends. You're winning by far right now. What's on your mind?",
            "choices": [
                "A. CRYING FOR YOU: \"Oops, I'm winning too much! Drinks on me later to make up for this game domination.\"",
                "B. Empathetic Opponent: \"I feel for my pals losing the game; I'm here cheering them on to boost their spirits!\"",
                "C. Diplomatic Sportsman: \"Still playing to win, but I'll ease up a bit — let's keep this game fun for everyone.\"",
                "D. Logic Lord: \"I'm just nailing this game. It's all in the strategy.\""
            ]
        },
        {
            "question": "Your Friend is rejected by a crush. Which unaired Friends episode do you show them?",
            "choices": [
                "A. The One On Your Side: \"I reassure them of their worth, always on their team no matter what.\"",
                "B. The One With the Shoulder to Cry On: \"I'm here for a good cry and a big hug — let it all out.\"",
                "C. The One with the Sugar Coat: \"I gently remind them it's the other person's loss, not theirs.\"",
                "D. The One with the Truth Bomb: \"I lay out the facts and help them figure out what went wrong.\""
            ]
        },
        {
            "question": "Team Troubleshooting: What's Your Style?",
            "choices": [
                "A. Emotions Coach: \"Team cheerleader, boosting spirits and keeping morale sky-high!\"",
                "B. Pep Talk Captain: \"We're all about inspiring talks! Motivation is our magic for victory.\"",
                "C. Balanced Player: \"I mix strategy with good vibes, planning for success while keeping the team happy.\"",
                "D. Strategy Coach: \"Game plan guru here! I design winning strategies and keep emotions off the field.\""
            ]
        },
        {
            "question": "We're turning your first date into a movie! What's the script?",
            "choices": [
                "A. The Detailed Script: \"Scripted to perfection — every moment planned, every detail dialed in!\"",
                "B. Plan and Pivot: \"I plan key scenes but am ready to adjust based on how we vibe together.\"",
                "C. The Guided Journey: \"Starting point set, the rest is up for surprises!\"",
                "D. The Unplanned Adventure: \"Who needs plans? We're winging it for spontaneous thrills!\""
            ]
        },
        {
            "question": "Task Tackling: How do you handle it?",
            "choices": [
                "A. Blueprint Boss: \"I draft every detail and follow my blueprint to the letter — precision is key!\"",
                "B. Flexi-Strategist: \"I mark key milestones and play with different paths to hit them — flexibility meets focus.\"",
                "C. Flow Rider: \"Goal in mind, I ride the wave of creativity and tweak the plan as inspiration strikes.\"",
                "D. Flyin' Free: \"No plans, no problem! I improvise and enjoy the journey as it unfolds.\""
            ]
        },
        {
            "question": "Tomorrow's your day off— yay! What will the day look like?",
            "choices": [
                "A. Itinerary Expert: \"Every hour's booked — my day's as planned as it gets!\"",
                "B. Planned but Pliable: \"I've lined up some cool stuff, yet I'm all for last-minute changes.\"",
                "C. Flexible & Free: \"I've got ideas but no set plans — let's see where the day takes us!\"",
                "D. Go with the Flow: \"Plan? What plan? I make it up as I go!\""
            ]
        }
    ]
    }

def register_commands():
    url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

    commands = [
        {
            "name": "hello",
            "type": 1,
            "description": "Get a friendly greeting from the bot"
        },
        {
            "name": "wyr",
            "type": 1,
            "description": "Play a game of 'Would You Rather'"
        },
        {
            "name": "mbti",
            "type": 1,
            "description": "Take your personalized MBTI (Myers-Briggs Type Indicator) test here!"
        },
        {
            "name": "rules",
            "type": 1,
            "description": "This is an Admin command"
        },
        {
            "name": "verify",
            "type": 1,
            "description": "Verify yourself as a moots or content creator",
            "options": [
                {
                    "name": "link",
                    "description": "Your Mootiez profile link or Social Media link",
                    "type": 3,
                    "required": True
                }
            ]
        },
        {
            "name": "addwyr",
            "type": 1,
            "description": "Add your own 'Would You Rather' question",
            "options": [
                {
                    "name": "question",
                    "description": "The main question for 'Would You Rather'",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "option1",
                    "description": "The first option",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "option2",
                    "description": "The second option",
                    "type": 3,
                    "required": True
                }
            ]
        }
    ]

    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }

    for command in commands:
        max_retries = 5
        retry_after = 1

        for attempt in range(max_retries):
            response = requests.post(url, json=command, headers=headers)

            if response.status_code in (200, 201):
                print(f"Command '{command['name']}' registered successfully")
                break
            elif response.status_code == 429:
                retry_after = json.loads(response.text).get('retry_after', 5)
                print(f"Rate limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                print(f"Failed to register command '{command['name']}'. Status code: {response.status_code}")
                print(response.text)
                break

        else:  # This else clause is executed if the for loop completes without breaking
            print(f"Failed to register command '{command['name']}' after {max_retries} attempts")

        # Add a small delay between command registrations to avoid hitting rate limits
        time.sleep(1)

    print("Command registration process completed.")

async def handle_interaction(body_json: dict) -> dict:
    interaction_type = body_json.get('type')

    if interaction_type == 1:  # Ping
        return success_response({'type': 1})
    elif interaction_type == 2:  # Application Command
        return await handle_application_command(body_json)
    elif interaction_type == 3:  # Button Interaction
        custom_id = body_json['data']['custom_id']
        if custom_id.startswith('mbti_'):
            return await handle_mbti_button_interaction(body_json)
        elif custom_id.startswith('wyr_'):
            return await handle_wyr_button_interaction(body_json)
        elif custom_id.startswith('next_question_'):
            question_id = '_'.join(custom_id.split('_')[2:])
            return await handle_next_question_button_interaction(body_json, question_id)
        elif custom_id == 'agree_rules':
            return await handle_agree_rules_button(body_json)
        else:
            return error_response(400, 'Unrecognized button interaction.')
    else:
        return error_response(400, 'Interaction type not recognized')

async def handle_next_question_button_interaction(body_json: dict, question_id: str) -> dict:
    try:
        conversation_id = body_json.get('channel_id', 'default_channel')

        response = table.get_item(Key={
            'conversationID': conversation_id,
            'message_id': question_id
        })

        if 'Item' not in response:
            return error_response(404, 'Question not found')

        item = response['Item']
        next_question_index = item['question_index'] + 1

        return await present_question(conversation_id, next_question_index)

    except KeyError as e:
        return error_response(400, f'KeyError: {str(e)}')
    except ClientError as e:
        print(f'Error retrieving MBTI question from DynamoDB: {e}')
        return error_response(500, 'Internal server error')
    except Exception as e:
        print(f'Error handling interaction: {e}')
        return error_response(500, 'Internal server error')

async def handle_rules_command(body_json):
    # Check if the command is used in the allowed channel
    if body_json['channel_id'] != ALLOWED_CHANNEL_ID:
            return success_response({
            'type': 4,
            'data': {
                'content': "This is an admin command.",
                'flags': 64
            }
    })
    embed = {
        "title": "📜 Mootiez Server Rules",
        "color": 3447003,
        "fields": [
            {
                "name": "1. Be Respectful",
                "value": "Treat all members with respect and kindness.\nDiscriminatory language, hate speech, and harassment are strictly prohibited."
            },
            {
                "name": "2. No Spamming",
                "value": "Avoid spamming messages, images, or emojis.\nKeep discussions on-topic and use appropriate channels."
            },
            {
                "name": "3. Use Appropriate Channels",
                "value": "Post content in the relevant channels.\nCheck the channel description for guidance on what belongs where."
            },
            {
                "name": "4. No NSFW Content",
                "value": "This is a family-friendly server. Do not post any NSFW (Not Safe For Work) content, including images, links, or discussions."
            },
            {
                "name": "5. Respect Privacy",
                "value": "Do not share personal information about yourself or others.\nRespect the privacy of fellow members."
            },
            {
                "name": "6. No Self-Promotion",
                "value": "Self-promotion, advertising, or sharing referral links without prior approval is not allowed.\nThis includes promoting other Discord servers, social media accounts, or websites."
            },
            {
                "name": "7. Follow Discord's Terms of Service",
                "value": "Abide by Discord's [Terms of Service](https://discord.com/terms) and [Community Guidelines](https://discord.com/guidelines)."
            },
            {
                "name": "8. Use Common Sense",
                "value": "If something feels wrong, it probably is. Use common sense and good judgment."
            },
            {
                "name": "9. Listen to Moderators",
                "value": "Follow the instructions of Mootiez staff and moderators.\nIf you have concerns, approach a moderator privately."
            },
            {
                "name": "10. Have Fun!",
                "value": "Enjoy your time here, make new friends, and share your interests!"
            }
        ],
        "footer": {
            "text": "Thank you for being a part of our community!"
        }
    }

    return success_response({
        'type': 4,
        'data': {
            'embeds': [embed],
            'components': [
                {
                    'type': 1,
                    'components': [
                        {
                            'type': 2,
                            'label': 'I agree to the rules',
                            'style': 1,
                            'custom_id': 'agree_rules'
                        }
                    ]
                }
            ]
        }
    })

async def handle_agree_rules_button(body_json: dict) -> dict:
    try:
        guild_id = 1210085674590539857
        user_id = body_json['member']['user']['id']
        role_id = "1210096098677620776"  # Replace with the actual role ID of "members"

        url = f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
        headers = {
            "Authorization": f"Bot {TOKEN}",
            "Content-Type": "application/json"
        }
        
        response = requests.put(url, headers=headers)
        if response.status_code == 204:
            return success_response({
                'type': 4,
                'data': {
                    'content': "Thank you for agreeing to the rules! You have been assigned the 'members' role.",
                    'flags': 64  # This hides the response from others
                }
            })
        else:
            return error_response(response.status_code, response.text)
    except Exception as e:
        print(f"Error handling agree rules button interaction: {e}")
        return error_response(500, 'Internal server error')


ALLOWED_CHANNEL_IDS = "1265225140321517568"
async def handle_verify_command(body_json):
    link = body_json.get('data', {}).get('options', [{}])[0].get('value')
    user_id = body_json.get('member', {}).get('user', {}).get('id')
    guild_id = body_json.get('guild_id')
    channel_id = body_json.get('channel_id')  # Get the channel ID

    # Role IDs
    role_ids = {
        'moots': "1265207283068043294",  # Role ID for "moots"
        'content_creator': "1265210670228705310"  # Role ID for "content creator"
    }

    # Role names
    role_names = {
        'moots': "moots",
        'content_creator': "content creator"
    }

    # Define the allowed channel ID (replace with your channel ID)

    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }

    if channel_id != ALLOWED_CHANNEL_IDS:
            return success_response({
            'type': 4,
            'data': {
                'content': "Please use this command in #proofs.",
                'flags': 64
            }
    })

    if link:
        if link.startswith("https://mootiez.me/@"):
            role_id = role_ids['moots']
            role_name = role_names['moots']
        elif "https://www.youtube.com/@" in link:
            role_id = role_ids['content_creator']
            role_name = role_names['content_creator']
        elif "https://www.instagram.com/" in link:
            role_id = role_ids['content_creator']
            role_name = role_names['content_creator']
        elif "https://www.tiktok.com/@" in link:
            role_id = role_ids['content_creator']
            role_name = role_names['content_creator']
        else:
            return error_response(400, "Invalid link format. Please provide a valid Mootiez profile link or a recognized content creator link.")

        url = f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
        
        response = requests.put(url, headers=headers)
        if response.status_code == 204:
            return success_response({
                'type': 4,
                'data': {
                    'content': f"Verification successful! You have been assigned the '{role_name}' role.",
                    'flags': 64  # This hides the response from others
                }
            })
        else:
            return error_response(response.status_code, response.text)
    else:
        return error_response(400, "No link provided. Please provide a valid link.")

def lambda_handler(event: dict, context) -> dict:
    http_method = event.get('httpMethod')
    http_path = event.get('path')
    if http_method == 'POST' and http_path == '/hello':
        PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY')
        if not PUBLIC_KEY:
            return error_response(500, 'Server configuration error: Missing public key')

        try:
            verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        except ValueError:
            return error_response(500, 'Server configuration error: Invalid public key format')

        headers = event.get('headers', {})
        signature = headers.get("x-signature-ed25519")
        timestamp = headers.get("x-signature-timestamp")

        if (not signature) or (not timestamp):
            return error_response(401, 'Missing signature or timestamp')

        body = get_request_body(event)

        try:
            verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
        except (BadSignatureError, ValueError):
            return error_response(401, 'Invalid request signature')

        try:
            body_json = json.loads(body)
        except json.JSONDecodeError:
            return error_response(400, 'Invalid JSON in request body')

        try:
            return asyncio.run(handle_interaction(body_json))
        except Exception as e:
            print(f"Error handling interaction: {e}")
            return error_response(500, 'Internal server error')
    elif http_method == 'POST' and http_path == '/register-commands':
        register_commands()
        return success_response({
            'message': 'Command registration process initiated.'
        })

def get_request_body(event: dict) -> str:
    if 'body' not in event:
        return ''

    body = event['body']
    if event.get('isBase64Encoded', False):
        return base64.b64decode(body).decode('utf-8')
    elif isinstance(body, str):
        return body
    else:
        return json.dumps(body)

async def handle_application_command(body_json):
    command_name = body_json.get('data', {}).get('name')
    if command_name == 'hello':
      channel_id = body_json.get('channel_id')
      if channel_id == ALLOWED_CHANNEL_IDS:
            return success_response({
            'type': 4,
            'data': {
                'content': "This command cannot be used in #proofs.",
                'flags': 64
            }
    })
      else:
       user_name = body_json.get('member', {}).get('user', {}).get('username', 'there')
       return success_response({
            'type': 4,
            'data': {
                'content': f"Hello, {user_name}! 👋 Welcome to our Discord bot.  Feel free to set up your unique Mootiez Profile at our official website https://www.mootiez.com/"
            }
        })
    elif command_name == 'wyr':
        return handle_wyr_command(body_json)
    elif command_name == 'mbti':
        return await handle_mbti_command(body_json)
    elif command_name == 'rules':
        return await handle_rules_command(body_json)
    elif command_name == 'verify':
        return await handle_verify_command(body_json)
    elif command_name == 'addwyr':
        return handle_add_wyr_command (body_json)
    else:
        return success_response({
            'type': 4,
            'data': {
                'content': "I'm sorry, I don't recognize that command."
            }
        })

def handle_add_wyr_command(body_json):
    channel_id = body_json.get('channel_id')
    if channel_id == ALLOWED_CHANNEL_IDS:
            return success_response({
            'type': 4,
            'data': {
                'content': "This command cannot be used in #proofs.",
                'flags': 64
            }
    })
    user_id = body_json['member']['user']['id']
    options = body_json['data']['options']
    
    question = next(opt['value'] for opt in options if opt['name'] == 'question')
    option1 = next(opt['value'] for opt in options if opt['name'] == 'option1')
    option2 = next(opt['value'] for opt in options if opt['name'] == 'option2')
    
    # Create the full question string
    full_question = f"Would you rather {question} 1. {option1}, 2. {option2}"
    question_id = f"wyr_user_{int(time.time())}_{random.randint(1000, 9999)}"
    
    try:
        # Store the new question in DynamoDB
        table.put_item(
            Item={
                'conversationID': 'wyr_questions',  # Use a specific conversationID for storing questions
                'message_id': question_id,
                'question': full_question,
                'created_by': user_id,
                'option1_votes': 0,
                'option2_votes': 0,
                'user_votes': []
            }
        )
    except ClientError as e:
        print(f"Error storing new question in DynamoDB: {e}")
        return error_response(500, "Internal server error")
    
    return success_response({
        'type': 4,
        'data': {
            'content': f"Your 'Would You Rather' question has been added successfully!",
            'flags': 64
        }
    })

def get_all_wyr_questions():
    try:
        response = table.query(
            KeyConditionExpression=Key('conversationID').eq('wyr_questions')
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error retrieving WYR questions from DynamoDB: {e}")
        return []

def handle_wyr_command(body_json):
    channel_id = body_json.get('channel_id')
    if channel_id == ALLOWED_CHANNEL_IDS:
        return success_response({
            'type': 4,
            'data': {
                'content': "This command cannot be used in #proofs.",
                'flags': 64
            }
        })

    # Get all questions, including user-created ones
    all_questions = Qlist + get_all_wyr_questions()
    
    if not all_questions:
        return error_response(404, "No questions available")

    question_item = random.choice(all_questions)
    
    # Check if the question is from the original list or user-created
    if isinstance(question_item, str):
        question = question_item
        question_id = f"wyr_{int(time.time())}_{random.randint(1000, 9999)}"
    else:
        question = question_item['question']
        question_id = question_item['message_id']

    conversation_id = body_json.get('channel_id', 'default_channel')
    
    try:
        table.put_item(
            Item={
                'conversationID': conversation_id,
                'message_id': question_id,
                'question': question,
                'option1_votes': 0,
                'option2_votes': 0,
                'user_votes': []
            }
        )
    except ClientError as e:
        print(f"Error storing question in DynamoDB: {e}")
        return error_response(500, "Internal server error")
    
    return success_response({
        'type': 4,
        'data': {
            'content': f"**Would You Rather:**\n{question}",
            'components': [
                {
                    'type': 1,
                    'components': [
                        {'type': 2, 'style': 1, 'label': 'Option 1', 'custom_id': f'wyr_option1_{question_id}'},
                        {'type': 2, 'style': 1, 'label': 'Option 2', 'custom_id': f'wyr_option2_{question_id}'},
                        {'type': 2, 'style': 2, 'label': 'Show Results', 'custom_id': f'wyr_results_{question_id}'},
                        {'type': 2, 'style': 2, 'label': 'Next Question', 'custom_id': 'wyr_next'}
                    ]
                }
            ]
        }
    })
    
# Function to calculate MBTI type
def calculate_mbti_type(responses):
    e_i_score = 0
    s_n_score = 0
    t_f_score = 0
    j_p_score = 0
    processed_indices = set()

    for response in responses:
        if all(option in response for option in ['optionA_votes', 'optionB_votes', 'optionC_votes', 'optionD_votes']):
            optionA_votes = int(response.get('optionA_votes', 0))
            optionB_votes = int(response.get('optionB_votes', 0))
            optionC_votes = int(response.get('optionC_votes', 0))
            optionD_votes = int(response.get('optionD_votes', 0))

            if optionC_votes + optionD_votes > optionA_votes + optionB_votes:
                normalized_score = -1
            else:
                normalized_score = 1

            question_index = response.get('question_index', -1)

            if question_index == -1:
                print("Skipping response due to missing 'question_index'")
                continue

            if question_index in processed_indices:
                print(f"Skipping duplicate response for question_index {question_index}")
                continue

            processed_indices.add(question_index)

            if 0 <= question_index < 3:
                e_i_score += normalized_score
            elif 3 <= question_index < 6:
                s_n_score += normalized_score
            elif 6 <= question_index < 9:
                t_f_score += normalized_score
            elif 9 <= question_index < 12:
                j_p_score += normalized_score

    mbti_type = ''
    mbti_type += 'E' if e_i_score >= 0 else 'I'
    mbti_type += 'S' if s_n_score >= 0 else 'N'
    mbti_type += 'T' if t_f_score >= 0 else 'F'
    mbti_type += 'J' if j_p_score >= 0 else 'P'

    return mbti_type

async def send_mbti_report(conversation_id, mbti_type):
    mbti_descriptions = {
        "ISTJ": {
            "name": "The Inspector",
            "strengths": ["Honest", "Direct", "Strong-willed", "Dutiful", "Practical"],
            "weaknesses": ["Stubborn", "Insensitive", "Always by the book", "Judgmental", "Overly focused on social status"],
            "description": "ISTJs are serious, responsible, and dependable. They are committed to traditions and standards, and they strive for order and consistency in all areas of their lives."
        },
        "ISFJ": {
            "name": "The Protector",
            "strengths": ["Supportive", "Reliable", "Patient", "Imaginative", "Observant"],
            "weaknesses": ["Overly shy", "Take things too personally", "Repress feelings", "Overload themselves", "Reluctant to change"],
            "description": "ISFJs are warm, caring, and considerate individuals. They are loyal to their families and organizations and work hard to ensure the welfare of others."
        },
        "INFJ": {
            "name": "The Counselor",
            "strengths": ["Insightful", "Principled", "Passionate", "Altruistic", "Creative"],
            "weaknesses": ["Perfectionist", "Overly sensitive", "Burnout-prone", "Overly private", "Difficulty with criticism"],
            "description": "INFJs are empathetic and idealistic, with strong values and deep insights into others' motivations. They are dedicated to helping others and making the world a better place."
        },
        "INTJ": {
            "name": "The Architect",
            "strengths": ["Strategic", "Independent", "Innovative", "Analytical", "Determined"],
            "weaknesses": ["Arrogant", "Overly critical", "Dismissive of emotions", "Crave control", "Socially clueless"],
            "description": "INTJs are analytical and insightful thinkers. They have a strong sense of vision and strategy and excel in developing innovative solutions to complex problems."
        },
        "ISTP": {
            "name": "The Craftsman",
            "strengths": ["Optimistic", "Creative", "Practical", "Spontaneous", "Rational"],
            "weaknesses": ["Stubborn", "Insensitive", "Private", "Easily bored", "Risk-prone"],
            "description": "ISTPs are practical and action-oriented individuals who excel in analyzing and solving problems. They enjoy hands-on activities and exploring new opportunities."
        },
        "ISFP": {
            "name": "The Composer",
            "strengths": ["Charming", "Sensitive to others", "Imaginative", "Passionate", "Curious"],
            "weaknesses": ["Fiercely independent", "Unpredictable", "Easily stressed", "Overly competitive", "Fluctuating self-esteem"],
            "description": "ISFPs are gentle and compassionate artists with a deep appreciation for beauty and harmony. They are spontaneous and enjoy exploring their creativity in various forms."
        },
        "INFP": {
            "name": "The Healer",
            "strengths": ["Idealistic", "Empathetic", "Creative", "Open-minded", "Passionate"],
            "weaknesses": ["Overly idealistic", "Impractical", "Self-isolating", "Unfocused", "Self-critical"],
            "description": "INFPs are idealistic dreamers who are guided by strong inner values and a deep sense of compassion. They seek harmony and authenticity in all aspects of their lives."
        },
        "INTP": {
            "name": "The Thinker",
            "strengths": ["Analytical", "Original", "Open-minded", "Curious", "Objective"],
            "weaknesses": ["Insensitive", "Absent-minded", "Condescending", "Loathe rules", "Second-guess themselves"],
            "description": "INTPs are innovative thinkers who are constantly analyzing and questioning the world around them. They are independent and value intellectual autonomy and creativity."
        },
        "ESTP": {
            "name": "The Dynamo",
            "strengths": ["Energetic", "Rational", "Perceptive", "Sociable", "Spontaneous"],
            "weaknesses": ["Impatient", "Risk-prone", "Unstructured", "Defiant", "Insensitive"],
            "description": "ESTPs are energetic and action-oriented individuals who thrive on excitement and adventure. They are practical problem solvers who enjoy living in the moment."
        },
        "ESFP": {
            "name": "The Performer",
            "strengths": ["Bold", "Original", "Practical", "Observant", "Excellent people skills"],
            "weaknesses": ["Sensitive", "Easily bored", "Poor long-term planners", "Conflict-averse", "Unfocused"],
            "description": "ESFPs are spontaneous and outgoing performers who love to entertain and engage with others. They enjoy life and bring joy to those around them."
        },
        "ENFP": {
            "name": "The Inspirer",
            "strengths": ["Enthusiastic", "Creative", "Sociable", "Energetic", "Perceptive"],
            "weaknesses": ["Poor practical skills", "Unfocused", "Overly optimistic", "Restless", "Overly accommodating"],
            "description": "ENFPs are enthusiastic and imaginative individuals who are passionate about exploring new ideas and possibilities. They are empathetic and strive to inspire and motivate others."
        },
        "ENTP": {
            "name": "The Visionary",
            "strengths": ["Innovative", "Enthusiastic", "Strategic", "Charismatic", "Knowledgeable"],
            "weaknesses": ["Argumentative", "Insensitive", "Intolerant", "Poor follow-through", "Unfocused"],
            "description": "ENTPs are innovative and resourceful thinkers who enjoy exploring new concepts and possibilities. They are quick-witted and enjoy debating ideas with others."
        },
        "ESTJ": {
            "name": "The Supervisor",
            "strengths": ["Dedicated", "Strong-willed", "Direct", "Honest", "Loyal"],
            "weaknesses": ["Inflexible", "Uncomfortable with unconventional situations", "Judgmental", "Too focused on social status", "Difficult relaxing"],
            "description": "ESTJs are practical organizers who thrive on order and structure. They are dependable leaders who value tradition and loyalty in their personal and professional lives."
        },
        "ESFJ": {
            "name": "The Provider",
            "strengths": ["Caring", "Loyal", "Warm", "Organized", "Good at connecting"],
            "weaknesses": ["Needy", "Inflexible", "Vulnerable to criticism", "Too selfless", "Prone to worry"],
            "description": "ESFJs are warm-hearted and conscientious individuals who are committed to helping and supporting others. They are dependable and dedicated to creating harmony in their relationships."
        },
        "ENFJ": {
            "name": "The Teacher",
            "strengths": ["Charismatic", "Reliable", "Natural leaders", "Altruistic", "Empathetic"],
            "weaknesses": ["Overly idealistic", "Too selfless", "Overly sensitive", "Fluctuating self-esteem", "Struggle with decisions"],
            "description": "ENFJs are charismatic and inspiring leaders who are dedicated to bringing out the best in others. They are empathetic and compassionate, with a strong sense of social responsibility."
        },
        "ENTJ": {
            "name": "The Commander",
            "strengths": ["Efficient", "Energetic", "Self-confident", "Strong-willed", "Strategic"],
            "weaknesses": ["Impatient", "Arrogant", "Intolerant", "Poor handling of emotions", "Cold and ruthless"],
            "description": "ENTJs are assertive and ambitious leaders who are focused on achieving their goals. They are strategic and decisive, with a natural ability to lead and inspire others."
        }
    }

    mbti_info = mbti_descriptions.get(mbti_type, {
        "name": "Unknown Type",
        "strengths": [],
        "weaknesses": [],
        "description": "Unfortunately, there is no description available for this MBTI type."
    })

    strengths_list = "\n".join(f"- {strength}" for strength in mbti_info["strengths"])
    weaknesses_list = "\n".join(f"- {weakness}" for weakness in mbti_info["weaknesses"])

    embed = {
        'type': 4,
        'data': {
            'embeds': [
                {
                    'title': f"MBTI Type: {mbti_info['name']} ({mbti_type})",
                    'description': mbti_info['description'],
                    'fields': [
                        {'name': 'Strengths', 'value': strengths_list, 'inline': False},
                        {'name': 'Weaknesses', 'value': weaknesses_list, 'inline': False}
                    ]
                }
            ]
        }
    }
    return success_response(embed)

async def get_channel_name(channel_id):
    url = f"https://discord.com/api/v10/channels/{channel_id}"
    headers = {
        "Authorization": f"Bot {TOKEN}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return None
            channel_data = await response.json()
            return channel_data.get("name")

async def handle_mbti_command(body_json):
    channel_id = body_json.get('channel_id')
    channel_name = await get_channel_name(channel_id)

    if channel_id == ALLOWED_CHANNEL_IDS:
            return success_response({
            'type': 4,
            'data': {
                'content': "This command cannot be used in #proofs.",
                'flags': 64
            }
    })

    if not channel_name or not channel_name.startswith("ticket"):
        return success_response({
            'type': 4,
            'data': {
                'content': "This command can only be used in ticketed channels. Use the ticket bot to type /open to get a ticketed channel!",
                'flags': 64  # Optional: This flag makes the message ephemeral (visible only to the user who triggered the command)
            }
        })

    conversation_id = body_json.get('channel_id', 'default_channel')
    user_id = body_json['member']['user']['id']
    return await present_question(conversation_id, user_id, 0)

async def present_question(conversation_id, user_id, question_index):
    if isinstance(question_index, Decimal):
        question_index = int(question_index)

    if question_index >= len(quiz_data["questions"]):
        return success_response({
            'type': 4,
            'data': {
                'content': "Quiz completed! Thank you for your responses."
            }
        })

    question_data = quiz_data["questions"][question_index]
    question = question_data["question"]
    choices_text = "\n".join(question_data["choices"])

    question_text = f"**{question}**\n{choices_text}"
    question_id = f"mbti_{conversation_id}_{question_index}"

    try:
        table.put_item(
            Item={
                'conversationID': conversation_id,
                'userID': user_id,
                'message_id': question_id,
                'question_index': question_index,
                'question': question,
                'optionA_votes': 0,
                'optionB_votes': 0,
                'optionC_votes': 0,
                'optionD_votes': 0,
                'user_votes': []
            }
        )
    except ClientError as e:
        print(f"Error storing MBTI question in DynamoDB: {e}")
        return error_response(500, "Internal server error")

    return success_response({
        'type': 4,
        'data': {
            'content': question_text,
            'components': [
                {
                    'type': 1,
                    'components': [
                        {'type': 2, 'style': 1, 'label': 'A', 'custom_id': f'mbti_optionA_{question_id}'},
                        {'type': 2, 'style': 1, 'label': 'B', 'custom_id': f'mbti_optionB_{question_id}'},
                        {'type': 2, 'style': 1, 'label': 'C', 'custom_id': f'mbti_optionC_{question_id}'},
                        {'type': 2, 'style': 1, 'label': 'D', 'custom_id': f'mbti_optionD_{question_id}'}
                    ]
                }
            ]
        }
    })
    
async def handle_mbti_vote(body_json):
    custom_id = body_json['data']['custom_id']
    user_id = body_json['member']['user']['id']
    conversation_id = body_json.get('channel_id', 'default_channel')
    option = custom_id.split('_')[1]  # 'A', 'B', 'C', or 'D'
    question_id = '_'.join(custom_id.split('_')[2:])  # Extract the question ID

    # Ensure option is valid
    if option not in ['optionA', 'optionB', 'optionC', 'optionD']:
        return error_response(400, "Invalid option")

    try:
        # Retrieve the current state of the question from DynamoDB
        response = table.get_item(Key={
            'conversationID': conversation_id,
            'message_id': question_id
        })
    except ClientError as e:
        print(f"Error retrieving MBTI question from DynamoDB: {e}")
        return error_response(500, "Internal server error")

    if 'Item' not in response:
        return error_response(404, "Question not found")

    item = response['Item']
    if user_id in item.get('user_votes', []):
        return success_response({
            'type': 4,
            'data': {
                'content': "You have already voted for this question.",
                'flags': 64
            }
        })

    # Ensure only the user who started the test can vote
    if item['userID'] != user_id:
        return success_response({
            'type': 4,
            'data': {
                'content': "This is someone else's MBTI test, you're not authorized for this action.",
                'flags': 64
            }
        })

    vote_column = f'{option}_votes'  # Determine which vote column to increment
    try:
        # Update the vote count and add user_id to user_votes list
        table.update_item(
            Key={'conversationID': conversation_id, 'message_id': question_id},
            UpdateExpression=f'SET {vote_column} = if_not_exists({vote_column}, :start) + :inc, user_votes = list_append(if_not_exists(user_votes, :empty_list), :user)',
            ExpressionAttributeValues={
                ':inc': 1, 
                ':user': [user_id], 
                ':empty_list': [], 
                ':start': 0  # Initialize the vote column if it doesn't exist
            }
        )
    except ClientError as e:
        print(f"Error updating vote in DynamoDB: {e}")
        return error_response(500, "Internal server error")

    # Check if it's the last question
    total_questions = len(quiz_data["questions"])
    current_question_index = item['question_index']
    if current_question_index + 1 >= total_questions:
        # Retrieve all responses for the conversation
        try:
            response = table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('conversationID').eq(conversation_id)
            )
            responses = response.get('Items', [])
        except ClientError as e:
            print(f"Error scanning responses from DynamoDB: {e}")
            return error_response(500, "Internal server error")

        # Calculate MBTI type based on user responses
        mbti_type = calculate_mbti_type(responses)

        # Send MBTI report
        return await send_mbti_report(conversation_id, mbti_type)

    # Otherwise, proceed to the next question
    next_question_index = current_question_index + 1

    return await present_question(conversation_id, user_id, next_question_index)

async def handle_mbti_button_interaction(body_json):
    custom_id = body_json['data']['custom_id']
    if custom_id.startswith('mbti_option'):
        return await handle_mbti_vote(body_json)
    else:
        return success_response({
            'type': 4,
            'data': {
                'content': "I'm sorry, I don't recognize that button."
            }
        })

def handle_wyr_button(body_json):
    custom_id = body_json['data']['custom_id']
    user_id = body_json['member']['user']['id']
    conversation_id = body_json.get('channel_id', 'default_channel')
    
    if custom_id.startswith('wyr_option'):
        option, question_id = custom_id.split('_')[1], '_'.join(custom_id.split('_')[2:])
        return handle_vote(conversation_id, question_id, option, user_id)
    elif custom_id.startswith('wyr_results'):
        question_id = '_'.join(custom_id.split('_')[2:])
        return show_wyr_results(conversation_id, question_id)
    elif custom_id == 'wyr_next':
        return handle_wyr_command(body_json)

def handle_vote(conversation_id, question_id, option, user_id):
    try:
        response = table.get_item(Key={
            'conversationID': conversation_id,
            'message_id': question_id
        })
    except ClientError as e:
        print(f"Error retrieving question from DynamoDB: {e}")
        return error_response(500, "Internal server error")
    
    if 'Item' not in response:
        return error_response(404, "Question not found")
    
    item = response['Item']
    if user_id in item['user_votes']:
        return success_response({
            'type': 4,
            'data': {
                'content': "You have already voted for this question.",
                'flags': 64
            }
        })
    
    vote_column = f'option{option[-1]}_votes'
    try:
        table.update_item(
            Key={'conversationID': conversation_id, 'message_id': question_id},
            UpdateExpression=f'SET {vote_column} = {vote_column} + :inc, user_votes = list_append(user_votes, :user)',
            ExpressionAttributeValues={':inc': 1, ':user': [user_id]}
        )
    except ClientError as e:
        print(f"Error updating vote in DynamoDB: {e}")
        return error_response(500, "Internal server error")
    
    return success_response({
        'type': 4,
        'data': {
            'content': f"You selected Option {option[-1]}!",
            'flags': 64
        }
    })
    
async def handle_wyr_button_interaction(body_json):
    custom_id = body_json['data']['custom_id']
    if custom_id.startswith('wyr_'):
        return handle_wyr_button(body_json)
    else:
        return success_response({
            'type': 4,
            'data': {
                'content': "I'm sorry, I don't recognize that button."
            }
        })

def show_wyr_results(conversation_id, question_id):
    try:
        response = table.get_item(Key={
            'conversationID': conversation_id,
            'message_id': question_id
        })
    except ClientError as e:
        print(f"Error retrieving question from DynamoDB: {e}")
        return error_response(500, "Internal server error")
    
    if 'Item' not in response:
        return error_response(404, "Question not found")
    
    item = response['Item']
    question = item['question']
    option1_votes = item['option1_votes']
    option2_votes = item['option2_votes']
    total_votes = option1_votes + option2_votes

    if total_votes == 0:
        percentage1 = 0
        percentage2 = 0
    else:
        percentage1 = (option1_votes / total_votes) * 100
        percentage2 = (option2_votes / total_votes) * 100

    return success_response({
        'type': 4,
        'data': {
            'content': f"**Results for:**\n{question}\n\nOption 1: {percentage1:.1f}% ({option1_votes} votes)\nOption 2: {percentage2:.1f}% ({option2_votes} votes)\n\nTotal votes: {total_votes}",
            'flags': 64
        }
    })

def error_response(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps({'error': message})
    }

def success_response(body):
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

def error_response(status, message):
    return {
        "statusCode": status,
        "body": json.dumps({
            "message": message
        })
    }

def success_response(body):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }