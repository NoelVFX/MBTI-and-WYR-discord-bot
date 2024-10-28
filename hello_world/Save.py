# import json
# import os
# from nacl.signing import VerifyKey
# from nacl.exceptions import BadSignatureError
# import discord
# from discord.ext import commands
# from pprint import pprint
# import base64
# import requests
# import random
# import asyncio
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import boto3
# from botocore.exceptions import ClientError
# from datetime import datetime
# import uuid

# TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
# APPLICATION_ID = os.environ.get('DISCORD_APPLICATION_ID')
# DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME')
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(DYNAMODB_TABLE_NAME)
# vote_counts = {}
# user_votes = {}

# with open("test.json", "r") as file:
#     quizData = json.load(file)

# mbti_types = {
#     "ISTJ": {
#         "name": "The Inspector",
#         "strengths": ["Honest", "Direct", "Strong-willed", "Dutiful", "Practical"],
#         "weaknesses": ["Stubborn", "Insensitive", "Always by the book", "Judgmental", "Overly focused on social status"]
#     },
#     "ISFJ": {
#         "name": "The Protector",
#         "strengths": ["Supportive", "Reliable", "Patient", "Imaginative", "Observant"],
#         "weaknesses": ["Overly shy", "Take things too personally", "Repress feelings", "Overload themselves", "Reluctant to change"]
#     },
#     "INFJ": {
#         "name": "The Counselor",
#         "strengths": ["Insightful", "Principled", "Passionate", "Altruistic", "Creative"],
#         "weaknesses": ["Perfectionist", "Overly sensitive", "Burnout-prone", "Overly private", "Difficulty with criticism"]
#     },
#     "INTJ": {
#         "name": "The Architect",
#         "strengths": ["Strategic", "Independent", "Innovative", "Analytical", "Determined"],
#         "weaknesses": ["Arrogant", "Overly critical", "Dismissive of emotions", "Crave control", "Socially clueless"]
#     },
#     "ISTP": {
#         "name": "The Craftsman",
#         "strengths": ["Optimistic", "Creative", "Practical", "Spontaneous", "Rational"],
#         "weaknesses": ["Stubborn", "Insensitive", "Private", "Easily bored", "Risk-prone"]
#     },
#     "ISFP": {
#         "name": "The Composer",
#         "strengths": ["Charming", "Sensitive to others", "Imaginative", "Passionate", "Curious"],
#         "weaknesses": ["Fiercely independent", "Unpredictable", "Easily stressed", "Overly competitive", "Fluctuating self-esteem"]
#     },
#     "INFP": {
#         "name": "The Healer",
#         "strengths": ["Idealistic", "Empathetic", "Creative", "Open-minded", "Passionate"],
#         "weaknesses": ["Overly idealistic", "Impractical", "Self-isolating", "Unfocused", "Self-critical"]
#     },
#     "INTP": {
#         "name": "The Architect",
#         "strengths": ["Analytical", "Original", "Open-minded", "Curious", "Objective"],
#         "weaknesses": ["Insensitive", "Absent-minded", "Condescending", "Loathe rules", "Second-guess themselves"]
#     },
#     "ESTP": {
#         "name": "The Dynamo",
#         "strengths": ["Energetic", "Rational", "Perceptive", "Sociable", "Spontaneous"],
#         "weaknesses": ["Impatient", "Risk-prone", "Unstructured", "Defiant", "Insensitive"]
#     },
#     "ESFP": {
#         "name": "The Performer",
#         "strengths": ["Bold", "Original", "Practical", "Observant", "Excellent people skills"],
#         "weaknesses": ["Sensitive", "Easily bored", "Poor long-term planners", "Conflict-averse", "Unfocused"]
#     },
#     "ENFP": {
#         "name": "The Champion",
#         "strengths": ["Enthusiastic", "Creative", "Sociable", "Energetic", "Perceptive"],
#         "weaknesses": ["Poor practical skills", "Unfocused", "Overly optimistic", "Restless", "Overly accommodating"]
#     },
#     "ENTP": {
#         "name": "The Visionary",
#         "strengths": ["Innovative", "Enthusiastic", "Strategic", "Charismatic", "Knowledgeable"],
#         "weaknesses": ["Argumentative", "Insensitive", "Intolerant", "Poor follow-through", "Unfocused"]
#     },
#     "ESTJ": {
#         "name": "The Supervisor",
#         "strengths": ["Dedicated", "Strong-willed", "Direct", "Honest", "Loyal"],
#         "weaknesses": ["Inflexible", "Uncomfortable with unconventional situations", "Judgmental", "Too focused on social status", "Difficult relaxing"]
#     },
#     "ESFJ": {
#         "name": "The Provider",
#         "strengths": ["Caring", "Loyal", "Warm", "Organized", "Good at connecting"],
#         "weaknesses": ["Needy", "Inflexible", "Vulnerable to criticism", "Too selfless", "Prone to worry"]
#     },
#     "ENFJ": {
#         "name": "The Teacher",
#         "strengths": ["Charismatic", "Reliable", "Natural leaders", "Altruistic", "Empathetic"],
#         "weaknesses": ["Overly idealistic", "Too selfless", "Overly sensitive", "Fluctuating self-esteem", "Struggle with decisions"]
#     },
#     "ENTJ": {
#         "name": "The Commander",
#         "strengths": ["Efficient", "Energetic", "Self-confident", "Strong-willed", "Strategic"],
#         "weaknesses": ["Impatient", "Arrogant", "Intolerant", "Poor handling of emotions", "Cold and ruthless"]
#     }
# }

# Qlist = ['Would you rather pet a 1. Dinosaur, 2. Dragon', 'Would you rather eat 1. Hot Soba, 2. Cold Soba', 'Would you rather always have to 1. Whisper, 2. Shout', 'Would you rather be famous for your 1. Dancing Skills, 2. Singing Skills', 'Would you rather never have to do 1. Laundry again, 2. Dishes again', 'Would you rather 1. Sing everytime you say, 2. Dance everytime you move', 'Would you rather 1. New Jeans, 2. Taylor Swift', 
#          'Would you rather 1. Read mind, 2. Go invisible', 'Would you rather live without 1. Music, 2. Movies', 'Would you rather see 1. 10 minutes to the future, 2. 10 years to the future', 'Would you rather always feel 1. Too hot, 2. Too cold', 'Would you rather 1. Eat anything and never gain weight, 2. Will not feel tired and never need to sleep', 'Would you rather be the 1. Smartest person in the world, 2. Funniest person in the world',
#          'Would you rather 1. Never use technology again, 2. Never leave your home again', 'Would you rather 1. Want personalized features even though personal data is collected, 2. Generic functionality but no data collection', 'Would you rather 1. Speak a new language fluently, 2. Talk to an animal', 'Would you rather 1. Can only tell the truth, 2. Always tell the lie', 'Would you rather 1. Unlimited money, 2. Unlimited knowledge', 
#          'Would you rather live in a world 1. with no problems, 2. where you rule', 'Would you rather 1. Control time, 2. Change your appearance at will', 'Would you rather 1. Teleport anywhere instantly, 2. Read minds', 'Would you rather 1. Jojos Bizzare adventure, 2. Demon Slayer', 'Would you rather 1. Doge, 2. Nyan cat', 'Would you rather 1. Jake Paul, 2. Mike Tyson', 'Would you rather marrying a 1. Rich but toxic person, 2. Poor but loving person', 'Would you rather only watch 1. Anime, 2. K-dramas',
#          'Would you rather pet be able to breathe 1. In water, 2. In space', 'Would you rather 1. Skincare, 2. Makeup', 'Would you rather 1. Superpower, 2. Magic', 'Would you rather 1. Autumn/winter, 2. Spring/summer', 'Would you rather 1. Always being late, 2. Always being early', 'Would you rather know 1. When you will die, 2. How you will die', 'Would you rather 1. To love, 2. To be loved', 'Would you rather 1. Cat person, 2. Dog person', 'Would you rather 1. Reincarnation, 2. Time Travel', 'Would you rather 1. Have unlimited friends but they all fake, 2. Have one friend who really care about you', 
#          'Would you rather 1. IQ, 2. Photographic memory', 'Would you rather 1. Talk with your future self, 2. Speak to your past self', 'Would you rather 1. Cant listen to your favourite music, 2. Cant read your favourite books', 'Would you rather 1. Travel everywhere you want, 2. Never visit your town again', 'Would you rather 1. Have a comfortable job, 2. Own a high ranking company but have no control over it', 'Would you rather 1. Love, 2. Money', 'Would you rather 1. Friends, 2. Family', 'Would you rather 1. Be yourself, 2. Be someone else', 'Would you rather 1. Warm colors, 2. Cool colors', 'Would you rather 1. SamSung, 2. Apple']

# count1 = 1
# count2 = 1
# questioncount = 0

# def register_commands():
#     url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

#     commands = [
#         {
#             "name": "hello",
#             "type": 1,
#             "description": "Get a friendly greeting from the bot"
#         },
#         {
#             "name": "wyr",
#             "type": 1,
#             "description": "Play a game of 'Would You Rather'"
#         }
#     ]

#     headers = {
#         "Authorization": f"Bot {TOKEN}",
#         "Content-Type": "application/json"
#     }

#     for command in commands:
#         response = requests.post(url, json=command, headers=headers)
#         if response.status_code == 200 or response.status_code == 201:
#             print(f"Command '{command['name']}' registered successfully")
#         else:
#             print(f"Failed to register command '{command['name']}'. Status code: {response.status_code}")
#             print(response.text)

# register_commands()

# def lambda_handler(event: dict, context) -> dict:
#     print(json.dumps(event))
#     PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY')
    
#     if not PUBLIC_KEY:
#         return error_response(500, 'Server configuration error: Missing public key')

#     try:
#         verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
#     except ValueError:
#         return error_response(500, 'Server configuration error: Invalid public key format')

#     headers = event.get('headers', {})
#     signature = headers.get("x-signature-ed25519")
#     timestamp = headers.get("x-signature-timestamp")

#     if (not signature) or (not timestamp):
#         return error_response(401, 'Missing signature or timestamp')

#     body = get_request_body(event)

#     try:
#         verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
#     except (BadSignatureError, ValueError):
#         return error_response(401, 'Invalid request signature')

#     try:
#         body_json = json.loads(body)
#     except json.JSONDecodeError:
#         return error_response(400, 'Invalid JSON in request body')

#     # Check if this is a ping from Discord
#     if body_json.get('type') == 1:
#         return success_response({'type': 1})

#     # Handle other types of interactions
#     if body_json.get('type') == 2:  # Application Command
#         return handle_application_command(body_json)
    
#     if body_json.get('type') == 3:  # Button Interaction
#         return handle_button_interaction(body_json)

#     return success_response('Interaction type not recognized')

#     # If no conditions are met, return a default response
#     return success_response('Command not recognized')

# def get_request_body(event: dict) -> str:
#     if 'body' not in event:
#         return ''

#     body = event['body']
#     if event.get('isBase64Encoded', False):
#         return base64.b64decode(body).decode('utf-8')
#     elif isinstance(body, str):
#         return body
#     else:
#         return json.dumps(body)

# def handle_application_command(body_json):
#     command_name = body_json.get('data', {}).get('name')
#     if command_name == 'hello':
#         user_name = body_json.get('member', {}).get('user', {}).get('username', 'there')
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': f"Hello, {user_name}! 👋 Welcome to our Discord bot. How can I assist you today?"
#             }
#         })
#     elif command_name == 'wyr':
#         return handle_wyr_command(body_json)
#     else:
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': "I'm sorry, I don't recognize that command."
#             }
#         })

# def handle_wyr_command(body_json):
#     question = random.choice(Qlist)
#     vote_counts[question] = {'option1': 0, 'option2': 0}
#     user_votes[question] = set()
    
#     return success_response({
#         'type': 4,
#         'data': {
#             'content': f"**Would You Rather:**\n{question}",
#             'components': [
#                 {
#                     'type': 1,
#                     'components': [
#                         {'type': 2, 'style': 1, 'label': 'Option 1', 'custom_id': f'wyr_option1_{question}'},
#                         {'type': 2, 'style': 1, 'label': 'Option 2', 'custom_id': f'wyr_option2_{question}'},
#                         {'type': 2, 'style': 2, 'label': 'Show Results', 'custom_id': f'wyr_results_{question}'},
#                         {'type': 2, 'style': 2, 'label': 'Next Question', 'custom_id': 'wyr_next'}
#                     ]
#                 }
#             ]
#         }
#     })

# def handle_wyr_button(body_json):
#     custom_id = body_json['data']['custom_id']
#     user_id = body_json['member']['user']['id']
    
#     if custom_id.startswith('wyr_option'):
#         option, question = custom_id.split('_')[1], '_'.join(custom_id.split('_')[2:])
        
#         if user_id in user_votes[question]:
#             return success_response({
#                 'type': 4,
#                 'data': {
#                     'content': "You have already voted for this question.",
#                     'flags': 64
#                 }
#             })
        
#         vote_counts[question][option] += 1
#         user_votes[question].add(user_id)
        
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': f"You selected {option.capitalize()}!",
#                 'flags': 64
#             }
#         })
#     elif custom_id.startswith('wyr_results'):
#         question = '_'.join(custom_id.split('_')[2:])
#         return show_wyr_results(question)
#     elif custom_id == 'wyr_next':
#         return handle_wyr_command(body_json)

# def show_wyr_results(question):
#     option1_votes = vote_counts[question]['option1']
#     option2_votes = vote_counts[question]['option2']
#     total_votes = option1_votes + option2_votes

#     if total_votes == 0:
#         percentage1 = 0
#         percentage2 = 0
#     else:
#         percentage1 = (option1_votes / total_votes) * 100
#         percentage2 = (option2_votes / total_votes) * 100

#     return success_response({
#         'type': 4,
#         'data': {
#             'content': f"**Results for:**\n{question}\n\nOption 1: {percentage1:.1f}% ({option1_votes} votes)\nOption 2: {percentage2:.1f}% ({option2_votes} votes)\n\nTotal votes: {total_votes}",
#             'flags': 64
#         }
#     })

# def handle_button_interaction(body_json):
#     custom_id = body_json['data']['custom_id']
#     if custom_id.startswith('wyr_'):
#         return handle_wyr_button(body_json)
#     else:
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': "I'm sorry, I don't recognize that button."
#             }
#         })

# def error_response(status, message):
#     return {
#         "statusCode": status,  # Use the provided status
#         "body": json.dumps({
#             "message": message
#         })
#     }

# def success_response(body):
#     return {
#         'statusCode': 200,
#         'headers': {
#             'Content-Type': 'application/json'
#         },
#         'body': json.dumps(body)
#     }







# Code for the /MBTI command
# async def handle_mbti_command(body_json):
#     conversation_id = body_json.get('channel_id', 'default_channel')

#     # Asynchronously handle MBTI command
#     result = await handle_mbti_command_async(body_json)

#     # Assuming result is a JSON string returned from async function
#     try:
#         result_json = json.loads(result)
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON result: {e}")
#         return error_response(500, "Internal server error")

#     return {
#         'type': 4,
#         'data': {
#             'embeds': [result_json.get('embed')],  # Assuming embed is returned from async function
#             'components': result_json.get('components', [])  # Assuming components are optional in the async function
#         }
#     }

# async def handle_mbti_command_async(body_json):
#     try:
#         interaction_data = body_json['interaction']
#     except KeyError:
#         return json.dumps(error_response(400, "Invalid input: 'interaction' key not found in body_json"))

#     try:
#         view = MBTIView(interaction_data)  # Assuming MBTIView is properly defined
#     except Exception as e:
#         return json.dumps(error_response(500, f"Failed to create MBTIView: {str(e)}"))

#     # Assume some processing here to generate response_data as a dictionary
#     response_data = {
#         'embed': {  # Ensure 'embed' key exists
#             'title': "MBTI Quiz",
#             'description': "Welcome to the MBTI Quiz! Answer the questions below.",
#             'color': discord.Color.green().value  # Assuming discord is imported for this
#         },
#         'components': [
#             {
#                 'type': 1,
#                 'components': [
#                     {'type': 2, 'style': 1, 'label': 'Option A', 'custom_id': 'mbti_option_a'},
#                     {'type': 2, 'style': 1, 'label': 'Option B', 'custom_id': 'mbti_option_b'},
#                     {'type': 2, 'style': 1, 'label': 'Option C', 'custom_id': 'mbti_option_c'},
#                     {'type': 2, 'style': 1, 'label': 'Option D', 'custom_id': 'mbti_option_d'},
#                     {'type': 2, 'style': 2, 'label': 'Next Question', 'custom_id': 'mbti_next'}
#                 ]
#             }
#         ]
#     }
#     try:
#         # Convert response_data dictionary to JSON string
#         response_json = json.dumps(response_data)
#         return response_json
#     except Exception as e:
#         return error_response(500, f"Failed to encode response data: {str(e)}")

# def button_to_dict(button):
#     return {
#         'type': 2,
#         'style': button.style.value,
#         'label': button.label,
#         'custom_id': button.custom_id
#     }

# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, discord.ui.Button):
#             return {
#                 'type': 2,
#                 'style': obj.style.value,
#                 'label': obj.label,
#                 'custom_id': obj.custom_id
#             }
#         return super().default(obj)

# class MBTIView:
#     def __init__(self, interaction, timeout=180):
#         self.interaction = interaction
#         self.current_question_index = 0
#         self.user_responses = []
#         self.user_email = None

#         self.add_buttons()

#     def add_buttons(self):
#         for label, custom_id in [("A", "button_a"), ("B", "button_b"), ("C", "button_c"), ("D", "button_d")]:
#             self.add_item(discord.ui.Button(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id))

#     async def process_response(self, interaction, response):
#         if interaction['user'] != self.interaction['user']:
#             return {"type": 4, "data": {"content": "This quiz is not for you!", "flags": 64}}

#         self.user_responses.append(response)
#         self.current_question_index += 1

#         if self.current_question_index < len(quizData['pages'][0]['elements']):
#             await self.ask_question(interaction)
#         else:
#             await self.finish_quiz(interaction)

#     async def ask_question(self, interaction):
#         try:
#             question = quizData['pages'][0]['elements'][self.current_question_index]
#             question_text = question.get('title', question.get('name', '')) + '\n'

#             if question['type'] == 'radiogroup':
#                 for choice in question.get('choices', []):
#                     question_text += f"{choice.get('value', '')}: {choice.get('text', '')}\n"
#             elif question['type'] == 'html':
#                 question_text += question.get('html', '')

#             embed = {
#                 'title': f"Question {self.current_question_index + 1}",
#                 'description': question_text,
#                 'color': discord.Color.blue().value  # Assuming discord is imported for this
#             }

#             await edit_interaction_message(interaction, embed=embed, components=[button_to_dict(btn) for btn in self.children])
#         except (KeyError, IndexError) as e:
#             print(f"Error asking question: {e}")

#     async def finish_quiz(self, interaction):
#         try:
#             await edit_interaction_message(interaction, content="Quiz completed! Processing your results...", components=None)
#             result = processResults(self.user_responses)
#             type_info = mbti_types[result]
#             embed = create_result_embed(result, type_info)
#             await send_followup_message(interaction, embed=embed)

#             await self.store_responses(str(interaction.user['id']), self.user_email, result, self.user_responses)

#             if self.user_email:
#                 success = await sendmail_via_gmail(self.user_email, result, type_info, self.user_responses)
#                 if success:
#                     await send_followup_message(interaction, content=f"Your results have been sent to {self.user_email}. Please check your inbox!")
#                 else:
#                     await send_followup_message(interaction, content="There was an error sending the email. Please try again later.")
#             else:
#                 await send_followup_message(interaction, content="No email was provided, so we couldn't send you the detailed report.")

#             await send_detailed_report(interaction, result, self.user_responses)
#         except Exception as e:
#             print(f"Error finishing quiz: {e}")

#     async def store_responses(self, user_id, email, mbti_result, responses):
#         try:
#             # Implement your storage logic here
#             pass
#         except Exception as e:
#             print(f"Error storing responses in DynamoDB: {e}")

# class MBTICog:
#     def __init__(self):
#         pass

#     async def mbti(self, interaction):
#         view = MBTIView(interaction)
#         embed = {
#             'title': "MBTI Personality Test",
#             'description': "Welcome to the MBTI personality test! Click the buttons to answer the questions.",
#             'color': discord.Color.blue().value  # Assuming discord is imported for this
#         }
#         await edit_interaction_message(interaction, embed=embed, components=[button_to_dict(btn) for btn in view.children])

# async def sendmail_via_gmail(receiver_email, mbti_result, type_info, user_responses):
#     sender_email = "mootiezxdiscord@gmail.com"  # Your Gmail address
#     password = "syevjyvorwggegqb"  # Your Gmail password or App Password

#     message = MIMEMultipart("alternative")
#     message["Subject"] = f"Your MBTI Result: {mbti_result}"
#     message["From"] = sender_email
#     message["To"] = receiver_email

#     email_content = f"""
#     <html>
#     <body>
#         <h2>Your MBTI Result: {mbti_result} - {type_info['name']}</h2>
#         <p>Here's a comprehensive overview of your {mbti_result} personality type:</p>
#         <h3>Type Description:</h3>
#         <p>{mbti_result} types, known as '{type_info['name']}', are typically characterized by their {', '.join(type_info['strengths'][:3]).lower()} nature. They tend to approach life with a {type_info['strengths'][3].lower()} and {type_info['strengths'][4].lower()} attitude.</p>
#         <h3>Key Strengths:</h3>
#         <ul>
#             {''.join(f'<li>{strength}</li>' for strength in type_info['strengths'])}
#         </ul>
#         <h3>Potential Challenges:</h3>
#         <ul>
#             {''.join(f'<li>{weakness}</li>' for weakness in type_info['weaknesses'])}
#         </ul>
#         <h3>MBTI Dimensions Explained:</h3>
#         <ul>
#             {''.join(f'<li>{letter}: {get_dimension_description(letter)}</li>' for letter in mbti_result)}
#         </ul>
#         <h3>Personal Growth Opportunities:</h3>
#         <p>{get_personal_growth_advice(mbti_result)}</p>
#         <h3>Your Quiz Responses:</h3>
#         <ol>
#             {''.join(f'<li>{response}</li>' for response in user_responses)}
#         </ol>
#         <p><a href="https://mootiez.com">Join mootiez to enjoy the full function and a more detailed MBTI report!</a></p>
#     </body>
#     </html>
#     """

#     part = MIMEText(email_content, "html")
#     message.attach(part)

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email, message.as_string())
#         print(f"Email sent successfully to {receiver_email}")
#         return True
#     except Exception as e:
#         print(f"Error sending email: {e}")
#         return False

# def create_result_embed(result, type_info):
#     embed = discord.Embed(
#         title=f"Your MBTI Result: {result} - {type_info['name']}",
#         description=f"Here's a comprehensive overview of your {result} personality type:",
#         color=discord.Color.blue()
#     )

#     embed.add_field(
#         name="Type Description",
#         value=f"{result} types, known as '{type_info['name']}', are typically characterized by their {', '.join(type_info['strengths'][:3]).lower()} nature. They tend to approach life with a {type_info['strengths'][3].lower()} and {type_info['strengths'][4].lower()} attitude.",
#         inline=False
#     )

#     strengths = "\n".join([f"• {strength}" for strength in type_info['strengths']])
#     embed.add_field(name="Key Strengths", value=strengths, inline=False)

#     challenges = "\n".join([f"• {weakness}" for weakness in type_info['weaknesses']])
#     embed.add_field(name="Potential Challenges", value=challenges, inline=False)

#     dimensions = "\n".join([f"{letter}: {get_dimension_description(letter)}" for letter in result])
#     embed.add_field(name="MBTI Dimensions Explained", value=dimensions, inline=False)

#     growth = get_personal_growth_advice(result)
#     embed.add_field(name="Personal Growth Opportunities", value=growth, inline=False)

#     embed.add_field(name="", value="Join mootiez to enjoy the full function and a more detailed MBTI report!", inline=False)

#     return embed

# async def send_detailed_report(interaction, result, user_responses):
#     user_id = str(interaction.user.id)

#     if result in mbti_types:
#         type_info = mbti_types[result]

#         embed = create_result_embed(result, type_info)

#         # Additional details (e.g., career suggestions, personal growth)
#         careers = get_career_suggestions(result)
#         embed.add_field(name="Potential Career Paths", value=careers, inline=False)

#         growth = get_personal_growth_advice(result)
#         embed.add_field(name="Personal Growth Opportunities", value=growth, inline=False)

#         embed.add_field(name="", value="Join mootiez to enjoy the full function and a more detailed MBTI report!", inline=False)

#         try:
#             await interaction.send(embed=embed)
#             await store_result(user_id, result, user_responses)
#         except discord.HTTPException as e:
#             print(f"Failed to send embed: {e}")
#             await interaction.send(f"There was an error sending your detailed results. Your MBTI type is: {result}")
#     else:
#         await interaction.send(f"Your MBTI type is: {result}\nSorry, detailed information for this type is not available.")

# async def store_result(user_id, result, responses):
#     try:
#         table.put_item(
#             Item={
#                 'ResponseId': str(uuid.uuid4()),
#                 'UserId': user_id,
#                 'MBTIResult': result,
#                 'Responses': responses,
#                 'Timestamp': datetime.utcnow().isoformat()
#             }
#         )
#         print(f"Result stored successfully for user {user_id}")
#     except Exception as e:
#         print(f"Error storing result in DynamoDB: {e}")

# def processResults(responses):
#     # This is a simplified example. You'll need to implement the actual MBTI scoring logic.
#     e_i = sum(1 for r in responses[:3] if r in ['a', 'b']) > 1
#     s_n = sum(1 for r in responses[3:6] if r in ['a', 'b']) > 1
#     t_f = sum(1 for r in responses[6:9] if r in ['a', 'b']) > 1
#     j_p = sum(1 for r in responses[9:12] if r in ['a', 'b']) > 1

#     result = ''
#     result += 'E' if e_i else 'I'
#     result += 'S' if s_n else 'N'
#     result += 'T' if t_f else 'F'
#     result += 'J' if j_p else 'P'

#     return result

# async def edit_interaction_message(interaction, **kwargs):
#     headers = {
#         "Authorization": f"Bot {TOKEN}",
#         "Content-Type": "application/json"
#     }
#     url = f"{INTERACTION_ENDPOINT_URL}/messages/{interaction['id']}/{interaction['token']}/edit"
#     data = json.dumps(kwargs)
#     try:
#         response = requests.patch(url, headers=headers, data=data)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to edit interaction message: {e}")

# async def send_followup_message(interaction, **kwargs):
#     headers = {
#         "Authorization": f"Bot {TOKEN}",
#         "Content-Type": "application/json"
#     }
#     url = f"{INTERACTION_ENDPOINT_URL}/webhooks/{interaction['application_id']}/{interaction['token']}"
#     data = json.dumps(kwargs)
#     try:
#         response = requests.post(url, headers=headers, data=data)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to send follow-up message: {e}")

# def get_dimension_description(letter):
#     descriptions = {
#         'E': 'Extraversion',
#         'I': 'Introversion',
#         'S': 'Sensing',
#         'N': 'Intuition',
#         'T': 'Thinking',
#         'F': 'Feeling',
#         'J': 'Judging',
#         'P': 'Perceiving'
#     }
#     return descriptions.get(letter, "Unknown dimension")

# def get_personal_growth_advice(mbti_type):
#     growth_advice = {
#         'ISTJ': "Practice flexibility and consider alternative viewpoints.",
#         'ISFJ': "Assert your needs and avoid overcommitting yourself.",
#         'INFJ': "Set realistic expectations and learn to accept imperfection.",
#         'INTJ': "Develop emotional intelligence and practice patience with others.",
#         'ISTP': "Work on long-term planning and following through on commitments.",
#         'ISFP': "Develop assertiveness and work on setting clear goals.",
#         'INFP': "Focus on practical skills and learn to handle criticism constructively.",
#         'INTP': "Develop social skills and practice expressing emotions.",
#         'ESTP': "Work on patience and long-term planning.",
#         'ESFP': "Develop self-discipline and focus on long-term consequences.",
#         'ENFP': "Improve follow-through on projects and develop realistic expectations.",
#         'ENTP': "Practice patience and work on finishing what you start.",
#         'ESTJ': "Develop emotional awareness and practice flexibility.",
#         'ESFJ': "Learn to say no and focus on self-care.",
#         'ENFJ': "Set personal boundaries and learn to handle criticism.",
#         'ENTJ': "Develop patience and emotional sensitivity towards others."
#     }
#     return growth_advice.get(mbti_type, "Focus on self-reflection and continuous personal development.")

# def get_career_suggestions(mbti_type):
#     # Define a function to return career suggestions based on MBTI type
#     career_suggestions = {
#         'ISTJ': "Accountant, Auditor, Project Manager",
#         'ISFJ': "Nurse, Social Worker, Librarian",
#         'INFJ': "Counselor, Writer, Psychologist",
#         'INTJ': "Scientist, Engineer, Lawyer",
#         'ISTP': "Mechanic, Pilot, Detective",
#         'ISFP': "Artist, Chef, Designer",
#         'INFP': "Therapist, Author, Teacher",
#         'INTP': "Philosopher, Architect, Software Developer",
#         'ESTP': "Sales Representative, Entrepreneur, Athlete",
#         'ESFP': "Performer, Event Planner, Public Relations",
#         'ENFP': "Journalist, Actor, Publicist",
#         'ENTP': "Inventor, Marketing Director, Lawyer",
#         'ESTJ': "Executive, Judge, Military Officer",
#         'ESFJ': "Teacher, Healthcare Worker, Office Manager",
#         'ENFJ': "Human Resources, Counselor, Teacher",
#         'ENTJ': "CEO, Business Owner, Consultant"
#     }
#     return career_suggestions.get(mbti_type, "Consider exploring various career paths to find what suits you best.")











# import json
# import os
# from nacl.signing import VerifyKey
# from nacl.exceptions import BadSignatureError
# import discord
# from discord.ext import commands
# from discord import app_commands
# from pprint import pprint
# import base64
# import requests
# import random
# import asyncio
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import boto3
# from botocore.exceptions import ClientError
# from discord_interactions import InteractionResponseType, InteractionType
# from datetime import datetime
# import uuid
# from discord.ui import Button
# from decimal import Decimal
# from collections import defaultdict
# from boto3.dynamodb.conditions import Key
# from boto3.dynamodb.conditions import Attr

# TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
# APPLICATION_ID = os.environ.get('DISCORD_APPLICATION_ID')
# DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME')
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(DYNAMODB_TABLE_NAME)
# user_sessions = {}

# Qlist = ['Would you rather pet a 1. Dinosaur, 2. Dragon', 'Would you rather eat 1. Hot Soba, 2. Cold Soba', 'Would you rather always have to 1. Whisper, 2. Shout', 'Would you rather be famous for your 1. Dancing Skills, 2. Singing Skills', 'Would you rather never have to do 1. Laundry again, 2. Dishes again', 'Would you rather 1. Sing everytime you say, 2. Dance everytime you move', 'Would you rather 1. New Jeans, 2. Taylor Swift', 
#          'Would you rather 1. Read mind, 2. Go invisible', 'Would you rather live without 1. Music, 2. Movies', 'Would you rather see 1. 10 minutes to the future, 2. 10 years to the future', 'Would you rather always feel 1. Too hot, 2. Too cold', 'Would you rather 1. Eat anything and never gain weight, 2. Will not feel tired and never need to sleep', 'Would you rather be the 1. Smartest person in the world, 2. Funniest person in the world',
#          'Would you rather 1. Never use technology again, 2. Never leave your home again', 'Would you rather 1. Want personalized features even though personal data is collected, 2. Generic functionality but no data collection', 'Would you rather 1. Speak a new language fluently, 2. Talk to an animal', 'Would you rather 1. Can only tell the truth, 2. Always tell the lie', 'Would you rather 1. Unlimited money, 2. Unlimited knowledge', 
#          'Would you rather live in a world 1. with no problems, 2. where you rule', 'Would you rather 1. Control time, 2. Change your appearance at will', 'Would you rather 1. Teleport anywhere instantly, 2. Read minds', 'Would you rather 1. Jojos Bizzare adventure, 2. Demon Slayer', 'Would you rather 1. Doge, 2. Nyan cat', 'Would you rather 1. Jake Paul, 2. Mike Tyson', 'Would you rather marrying a 1. Rich but toxic person, 2. Poor but loving person', 'Would you rather only watch 1. Anime, 2. K-dramas',
#          'Would you rather pet be able to breathe 1. In water, 2. In space', 'Would you rather 1. Skincare, 2. Makeup', 'Would you rather 1. Superpower, 2. Magic', 'Would you rather 1. Autumn/winter, 2. Spring/summer', 'Would you rather 1. Always being late, 2. Always being early', 'Would you rather know 1. When you will die, 2. How you will die', 'Would you rather 1. To love, 2. To be loved', 'Would you rather 1. Cat person, 2. Dog person', 'Would you rather 1. Reincarnation, 2. Time Travel', 'Would you rather 1. Have unlimited friends but they all fake, 2. Have one friend who really care about you', 
#          'Would you rather 1. IQ, 2. Photographic memory', 'Would you rather 1. Talk with your future self, 2. Speak to your past self', 'Would you rather 1. Cant listen to your favourite music, 2. Cant read your favourite books', 'Would you rather 1. Travel everywhere you want, 2. Never visit your town again', 'Would you rather 1. Have a comfortable job, 2. Own a high ranking company but have no control over it', 'Would you rather 1. Love, 2. Money', 'Would you rather 1. Friends, 2. Family', 'Would you rather 1. Be yourself, 2. Be someone else', 'Would you rather 1. Warm colors, 2. Cool colors', 'Would you rather 1. SamSung, 2. Apple']

# def get_dimension_description(letter):
#     descriptions = {
#         'E': "Gains energy from social interactions",
#         'I': "Recharges through solitude",
#         'S': "Focuses on concrete facts and details",
#         'N': "Considers abstract concepts and possibilities",
#         'T': "Makes decisions based on logic and analysis",
#         'F': "Considers emotions and values in decision-making",
#         'J': "Prefers structure and planning",
#         'P': "Embraces flexibility and spontaneity"
#     }
#     return descriptions[letter]

# def get_personal_growth_advice(mbti_type):
#     growth_advice = {
#         'ISTJ': "Practice flexibility and consider alternative viewpoints.",
#         'ISFJ': "Assert your needs and avoid overcommitting yourself.",
#         'INFJ': "Set realistic expectations and learn to accept imperfection.",
#         'INTJ': "Develop emotional intelligence and practice patience with others.",
#         'ISTP': "Work on long-term planning and following through on commitments.",
#         'ISFP': "Develop assertiveness and work on setting clear goals.",
#         'INFP': "Focus on practical skills and learn to handle criticism constructively.",
#         'INTP': "Develop social skills and practice expressing emotions.",
#         'ESTP': "Work on patience and long-term planning.",
#         'ESFP': "Develop self-discipline and focus on long-term consequences.",
#         'ENFP': "Improve follow-through on projects and develop realistic expectations.",
#         'ENTP': "Practice patience and work on finishing what you start.",
#         'ESTJ': "Develop emotional awareness and practice flexibility.",
#         'ESFJ': "Learn to say no and focus on self-care.",
#         'ENFJ': "Set personal boundaries and learn to handle criticism.",
#         'ENTJ': "Develop patience and emotional sensitivity towards others."
#     }
#     return growth_advice.get(mbti_type, "Focus on self-reflection and continuous personal development.")

# quiz_data = {
#          "questions": [
#         {
#             "question": "Friday's here and the gang's rallying for a night out. What's your move?",
#             "choices": [
#                 "A. Home Hermit: \"Big nights out? Hard pass. I'm all about cozy evenings in.\"",
#                 "B. Maybe...: \"I'll see how I feel. Sometimes yes, but I need my downtime too.\"",
#                 "C. I'm Down!: \"Absolutely, I'm in! Hanging with friends is always a boost.\"",
#                 "D. LFG!!!!: \"Oh yes! Bring on the night - I'm here for all the fun and new faces!\""
#             ]
#         },
#         {
#             "question": "Friend-o-meter: What's your vibe in the wild?",
#             "choices": [
#                 "A. Stealth Mode: \"I'm wallpaper with eyes-great at observing, not so much at mingling.\"",
#                 "B. Deep Diver: \"I dive deep into chats that grab my interest, usually one-on-one or in small crews.\"",
#                 "C. People Presence: \"I soak up the crowd's vibe without needing to dive into the mix.\"",
#                 "D. Social Butterfly: \"I'm all about chatting up new faces — socializing is my sport!\""
#             ]
#         },
#         {
#             "question": "Big win alert! How are you celebrating?",
#             "choices": [
#                 "A. Solo mode activated: \"Quiet time for me — I savor wins solo style!\"",
#                 "B. Lowkey Vibes: \"Just the inner circle — small gatherings are my jam.\"",
#                 "C. Hit Up the 'Gram: \"Quick post to share the joy, then back to the grind!\"",
#                 "D. Full Send!: \"Big bash with everyone! If it's not shared, did it even happen?\""
#             ]
#         },
#         {
#             "question": "Thinking about the future... what's your pick?",
#             "choices": [
#                 "A. Team Blueprint: \"All about solid plans and proven paths. Realism is my guide.\"",
#                 "B. Remix Mode: \"I remix the old with new twists for cool, practical innovations.\"",
#                 "C. Hybrid Hustle: \"I mix practical steps with bold, new ideas. Always eyeing the next big thing.\"",
#                 "D. Dream Weaver: \"I dream big and ask 'what if?', pushing boundaries beyond the usual.\""
#             ]
#         },
#         {
#             "question": "You're at the park with friends and it suddenly rains! What's the first thought you have?",
#             "choices": [
#                 "A. Umbrella Check: \"Umbrella time? I quickly gauge the rain and seek shelter—always practical!\"",
#                 "B. Shirt Saver: \"Oh no, my white shirt! I'm on it — finding a dry spot ASAP.\"",
#                 "C. Idea Tsunami: \"Wow, this rain? Just like life's curveballs — always making me think on my feet.\"",
#                 "D. Connect-the-Dots Champ: \"Rainy days flood me with memories — each drop a reminder of past moments.\""
#             ]
#         },
#         {
#             "question": "You're playing a solo RPG game and you're facing the BOSS level now. How do you approach it?",
#             "choices": [
#                 "A. Study & Win: \"I hit the books and guides to master the game plan before I play.\"",
#                 "B. Inventory Review: \"I check my gear and past wins to strategize my next move.\"",
#                 "C. I have a feeling I know what should happen. \"I follow my gut, tweaking my plan with a mix of instinct and insight.\"",
#                 "D. Just Try First! \"I dive right in and figure it out on the fly — adapt and overcome!\""
#             ]
#         },
#         {
#             "question": "Now you're playing a board game with 3 friends. You're winning by far right now. What's on your mind?",
#             "choices": [
#                 "A. CRYING FOR YOU: \"Oops, I'm winning too much! Drinks on me later to make up for this game domination.\"",
#                 "B. Empathetic Opponent: \"I feel for my pals losing the game; I'm here cheering them on to boost their spirits!\"",
#                 "C. Diplomatic Sportsman: \"Still playing to win, but I'll ease up a bit — let's keep this game fun for everyone.\"",
#                 "D. Logic Lord: \"I'm just nailing this game. It's all in the strategy.\""
#             ]
#         },
#         {
#             "question": "Your Friend is rejected by a crush. Which unaired Friends episode do you show them?",
#             "choices": [
#                 "A. The One On Your Side: \"I reassure them of their worth, always on their team no matter what.\"",
#                 "B. The One With the Shoulder to Cry On: \"I'm here for a good cry and a big hug — let it all out.\"",
#                 "C. The One with the Sugar Coat: \"I gently remind them it's the other person's loss, not theirs.\"",
#                 "D. The One with the Truth Bomb: \"I lay out the facts and help them figure out what went wrong.\""
#             ]
#         },
#         {
#             "question": "Team Troubleshooting: What's Your Style?",
#             "choices": [
#                 "A. Emotions Coach: \"Team cheerleader, boosting spirits and keeping morale sky-high!\"",
#                 "B. Pep Talk Captain: \"We're all about inspiring talks! Motivation is our magic for victory.\"",
#                 "C. Balanced Player: \"I mix strategy with good vibes, planning for success while keeping the team happy.\"",
#                 "D. Strategy Coach: \"Game plan guru here! I design winning strategies and keep emotions off the field.\""
#             ]
#         },
#         {
#             "question": "We're turning your first date into a movie! What's the script?",
#             "choices": [
#                 "A. The Detailed Script: \"Scripted to perfection — every moment planned, every detail dialed in!\"",
#                 "B. Plan and Pivot: \"I plan key scenes but am ready to adjust based on how we vibe together.\"",
#                 "C. The Guided Journey: \"Starting point set, the rest is up for surprises!\"",
#                 "D. The Unplanned Adventure: \"Who needs plans? We're winging it for spontaneous thrills!\""
#             ]
#         },
#         {
#             "question": "Task Tackling: How do you handle it?",
#             "choices": [
#                 "A. Blueprint Boss: \"I draft every detail and follow my blueprint to the letter — precision is key!\"",
#                 "B. Flexi-Strategist: \"I mark key milestones and play with different paths to hit them — flexibility meets focus.\"",
#                 "C. Flow Rider: \"Goal in mind, I ride the wave of creativity and tweak the plan as inspiration strikes.\"",
#                 "D. Flyin' Free: \"No plans, no problem! I improvise and enjoy the journey as it unfolds.\""
#             ]
#         },
#         {
#             "question": "Tomorrow's your day off— yay! What will the day look like?",
#             "choices": [
#                 "A. Itinerary Expert: \"Every hour's booked — my day's as planned as it gets!\"",
#                 "B. Planned but Pliable: \"I've lined up some cool stuff, yet I'm all for last-minute changes.\"",
#                 "C. Flexible & Free: \"I've got ideas but no set plans — let's see where the day takes us!\"",
#                 "D. Go with the Flow: \"Plan? What plan? I make it up as I go!\""
#             ]
#         }
#     ]
#     }

# def register_commands():
#     url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

#     commands = [
#         {
#             "name": "hello",
#             "type": 1,
#             "description": "Get a friendly greeting from the bot"
#         },
#         {
#             "name": "wyr",
#             "type": 1,
#             "description": "Play a game of 'Would You Rather'"
#         },
#         {
#             "name": "mbti",
#             "type": 1,
#             "description": "Take your personalized MBTI (Myers-Briggs Type Indicator) test here!"
#         },
#         {
#             "name": "rules",
#             "type": 1,
#             "description": "Displays the server rules and an interactive button to agree"
#         }
#     ]

#     headers = {
#         "Authorization": f"Bot {TOKEN}",
#         "Content-Type": "application/json"
#     }

#     for command in commands:
#         response = requests.post(url, json=command, headers=headers)
#         if response.status_code == 200 or response.status_code == 201:
#             print(f"Command '{command['name']}' registered successfully")
#         else:
#             print(f"Failed to register command '{command['name']}'. Status code: {response.status_code}")
#             print(response.text)

# register_commands()

# async def handle_interaction(body_json: dict) -> dict:
#     interaction_type = body_json.get('type')

#     if interaction_type == 1:  # Ping
#         return success_response({'type': 1})
#     elif interaction_type == 2:  # Application Command
#         return await handle_application_command(body_json)
#     elif interaction_type == 3:  # Button Interaction
#         custom_id = body_json['data']['custom_id']
#         if custom_id.startswith('mbti_'):
#             return await handle_mbti_button_interaction(body_json)
#         elif custom_id.startswith('wyr_'):
#             return await handle_wyr_button_interaction(body_json)
#         elif custom_id.startswith('next_question_'):
#             question_id = '_'.join(custom_id.split('_')[2:])
#             return await handle_next_question_button_interaction(body_json, question_id)
#         else:
#             return error_response(400, 'Unrecognized button interaction.')
#     else:
#         return error_response(400, 'Interaction type not recognized')

# async def handle_next_question_button_interaction(body_json: dict, question_id: str) -> dict:
#     try:
#         conversation_id = body_json.get('channel_id', 'default_channel')

#         response = table.get_item(Key={
#             'conversationID': conversation_id,
#             'message_id': question_id
#         })

#         if 'Item' not in response:
#             return error_response(404, 'Question not found')

#         item = response['Item']
#         next_question_index = item['question_index'] + 1

#         return await present_question(conversation_id, next_question_index)

#     except KeyError as e:
#         return error_response(400, f'KeyError: {str(e)}')
#     except ClientError as e:
#         print(f'Error retrieving MBTI question from DynamoDB: {e}')
#         return error_response(500, 'Internal server error')
#     except Exception as e:
#         print(f'Error handling interaction: {e}')
#         return error_response(500, 'Internal server error')

#     except KeyError as e:
#         return error_response(400, f"KeyError: {str(e)}")
#     except ClientError as e:
#         print(f"Error retrieving MBTI question from DynamoDB: {e}")
#         return error_response(500, "Internal server error")
#     except Exception as e:
#         print(f"Error handling interaction: {e}")
#         return error_response(500, "Internal server error")

# def lambda_handler(event: dict, context) -> dict:
#     PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY')
#     if not PUBLIC_KEY:
#         return error_response(500, 'Server configuration error: Missing public key')

#     try:
#         verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
#     except ValueError:
#         return error_response(500, 'Server configuration error: Invalid public key format')

#     headers = event.get('headers', {})
#     signature = headers.get("x-signature-ed25519")
#     timestamp = headers.get("x-signature-timestamp")

#     if (not signature) or (not timestamp):
#         return error_response(401, 'Missing signature or timestamp')

#     body = get_request_body(event)

#     try:
#         verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
#     except (BadSignatureError, ValueError):
#         return error_response(401, 'Invalid request signature')

#     try:
#         body_json = json.loads(body)
#     except json.JSONDecodeError:
#         return error_response(400, 'Invalid JSON in request body')

#     try:
#         return asyncio.run(handle_interaction(body_json))
#     except Exception as e:
#         print(f"Error handling interaction: {e}")
#         return error_response(500, 'Internal server error')

# def get_request_body(event: dict) -> str:
#     if 'body' not in event:
#         return ''

#     body = event['body']
#     if event.get('isBase64Encoded', False):
#         return base64.b64decode(body).decode('utf-8')
#     elif isinstance(body, str):
#         return body
#     else:
#         return json.dumps(body)

# async def handle_application_command(body_json):
#     command_name = body_json.get('data', {}).get('name')
#     if command_name == 'hello':
#         user_name = body_json.get('member', {}).get('user', {}).get('username', 'there')
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': f"Hello, {user_name}! 👋 Welcome to our Discord bot.  Feel free to set up your unique Mootiez Profile at our official website https://www.mootiez.com/"
#             }
#         })
#     elif command_name == 'wyr':
#         return handle_wyr_command(body_json)
#     elif command_name == 'mbti':
#         return await handle_mbti_command(body_json)
#     else:
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': "I'm sorry, I don't recognize that command."
#             }
#         })

# def handle_wyr_command(body_json):
#     question = random.choice(Qlist)
#     question_id = f"wyr_{hash(question)}"
#     conversation_id = body_json.get('channel_id', 'default_channel')
    
#     try:
#         table.put_item(
#             Item={
#                 'conversationID': conversation_id,
#                 'message_id': question_id,
#                 'question': question,
#                 'option1_votes': 0,
#                 'option2_votes': 0,
#                 'user_votes': []
#             }
#         )
#     except ClientError as e:
#         print(f"Error storing question in DynamoDB: {e}")
#         return error_response(500, "Internal server error")
    
#     return success_response({
#         'type': 4,
#         'data': {
#             'content': f"**Would You Rather:**\n{question}",
#             'components': [
#                 {
#                     'type': 1,
#                     'components': [
#                         {'type': 2, 'style': 1, 'label': 'Option 1', 'custom_id': f'wyr_option1_{question_id}'},
#                         {'type': 2, 'style': 1, 'label': 'Option 2', 'custom_id': f'wyr_option2_{question_id}'},
#                         {'type': 2, 'style': 2, 'label': 'Show Results', 'custom_id': f'wyr_results_{question_id}'},
#                         {'type': 2, 'style': 2, 'label': 'Next Question', 'custom_id': 'wyr_next'}
#                     ]
#                 }
#             ]
#         }
#     })
    
# def calculate_mbti_type(responses):
#     # Initialize scores for each MBTI dimension
#     e_i_score = 0
#     s_n_score = 0
#     t_f_score = 0
#     j_p_score = 0

#     # Initialize a set to keep track of processed question indices
#     processed_indices = set()

#     # Process each response
#     for response in responses:
#         # Ensure the response contains votes for options A, B, C, D
#         if all(option in response for option in ['optionA_votes', 'optionB_votes', 'optionC_votes', 'optionD_votes']):
#             optionA_votes = int(response.get('optionA_votes', 0))
#             optionB_votes = int(response.get('optionB_votes', 0))
#             optionC_votes = int(response.get('optionC_votes', 0))
#             optionD_votes = int(response.get('optionD_votes', 0))

#             # Determine the normalized score based on the dominant vote
#             if optionC_votes + optionD_votes > optionA_votes + optionB_votes:
#                 normalized_score = -1
#             else:
#                 normalized_score = 1

#             # Get question index
#             question_index = response.get('question_index', -1)
            
#             if question_index == -1:
#                 print("Skipping response due to missing 'question_index'")
#                 continue

#             if question_index in processed_indices:
#                 print(f"Skipping duplicate response for question_index {question_index}")
#                 continue

#             processed_indices.add(question_index)

#             # Update the scores based on the question index
#             if 0 <= question_index < 3:  # E/I questions
#                 e_i_score += normalized_score
#                 print(f"Updated E/I score: {e_i_score}")
#             elif 3 <= question_index < 6:  # S/N questions
#                 s_n_score += normalized_score
#                 print(f"Updated S/N score: {s_n_score}")
#             elif 6 <= question_index < 9:  # T/F questions
#                 t_f_score += normalized_score
#                 print(f"Updated T/F score: {t_f_score}")
#             elif 9 <= question_index < 12:  # J/P questions
#                 j_p_score += normalized_score
#                 print(f"Updated J/P score: {j_p_score}")
#             else:
#                 print(f"Question index {question_index} out of range")

#             # Debugging output for cumulative scores after each response
#             print(f"Cumulative Scores after response {question_index}: E/I={e_i_score}, S/N={s_n_score}, T/F={t_f_score}, J/P={j_p_score}")

#     # Debugging output for final scores
#     print(f"Final Scores: E/I={e_i_score}, S/N={s_n_score}, T/F={t_f_score}, J/P={j_p_score}")

#     # Determine MBTI type based on scores
#     mbti_type = ''
#     mbti_type += 'E' if e_i_score >= 0 else 'I'
#     mbti_type += 'S' if s_n_score >= 0 else 'N'
#     mbti_type += 'T' if t_f_score >= 0 else 'F'
#     mbti_type += 'J' if j_p_score >= 0 else 'P'

#     return mbti_type

# async def send_mbti_report(conversation_id, mbti_type):
#     mbti_descriptions = {
#         "ISTJ": {
#             "name": "The Inspector",
#             "strengths": ["Honest", "Direct", "Strong-willed", "Dutiful", "Practical"],
#             "weaknesses": ["Stubborn", "Insensitive", "Always by the book", "Judgmental", "Overly focused on social status"],
#             "description": "ISTJs are serious, responsible, and dependable. They are committed to traditions and standards, and they strive for order and consistency in all areas of their lives."
#         },
#         "ISFJ": {
#             "name": "The Protector",
#             "strengths": ["Supportive", "Reliable", "Patient", "Imaginative", "Observant"],
#             "weaknesses": ["Overly shy", "Take things too personally", "Repress feelings", "Overload themselves", "Reluctant to change"],
#             "description": "ISFJs are warm, caring, and considerate individuals. They are loyal to their families and organizations and work hard to ensure the welfare of others."
#         },
#         "INFJ": {
#             "name": "The Counselor",
#             "strengths": ["Insightful", "Principled", "Passionate", "Altruistic", "Creative"],
#             "weaknesses": ["Perfectionist", "Overly sensitive", "Burnout-prone", "Overly private", "Difficulty with criticism"],
#             "description": "INFJs are empathetic and idealistic, with strong values and deep insights into others' motivations. They are dedicated to helping others and making the world a better place."
#         },
#         "INTJ": {
#             "name": "The Architect",
#             "strengths": ["Strategic", "Independent", "Innovative", "Analytical", "Determined"],
#             "weaknesses": ["Arrogant", "Overly critical", "Dismissive of emotions", "Crave control", "Socially clueless"],
#             "description": "INTJs are analytical and insightful thinkers. They have a strong sense of vision and strategy and excel in developing innovative solutions to complex problems."
#         },
#         "ISTP": {
#             "name": "The Craftsman",
#             "strengths": ["Optimistic", "Creative", "Practical", "Spontaneous", "Rational"],
#             "weaknesses": ["Stubborn", "Insensitive", "Private", "Easily bored", "Risk-prone"],
#             "description": "ISTPs are practical and action-oriented individuals who excel in analyzing and solving problems. They enjoy hands-on activities and exploring new opportunities."
#         },
#         "ISFP": {
#             "name": "The Composer",
#             "strengths": ["Charming", "Sensitive to others", "Imaginative", "Passionate", "Curious"],
#             "weaknesses": ["Fiercely independent", "Unpredictable", "Easily stressed", "Overly competitive", "Fluctuating self-esteem"],
#             "description": "ISFPs are gentle and compassionate artists with a deep appreciation for beauty and harmony. They are spontaneous and enjoy exploring their creativity in various forms."
#         },
#         "INFP": {
#             "name": "The Healer",
#             "strengths": ["Idealistic", "Empathetic", "Creative", "Open-minded", "Passionate"],
#             "weaknesses": ["Overly idealistic", "Impractical", "Self-isolating", "Unfocused", "Self-critical"],
#             "description": "INFPs are idealistic dreamers who are guided by strong inner values and a deep sense of compassion. They seek harmony and authenticity in all aspects of their lives."
#         },
#         "INTP": {
#             "name": "The Thinker",
#             "strengths": ["Analytical", "Original", "Open-minded", "Curious", "Objective"],
#             "weaknesses": ["Insensitive", "Absent-minded", "Condescending", "Loathe rules", "Second-guess themselves"],
#             "description": "INTPs are innovative thinkers who are constantly analyzing and questioning the world around them. They are independent and value intellectual autonomy and creativity."
#         },
#         "ESTP": {
#             "name": "The Dynamo",
#             "strengths": ["Energetic", "Rational", "Perceptive", "Sociable", "Spontaneous"],
#             "weaknesses": ["Impatient", "Risk-prone", "Unstructured", "Defiant", "Insensitive"],
#             "description": "ESTPs are energetic and action-oriented individuals who thrive on excitement and adventure. They are practical problem solvers who enjoy living in the moment."
#         },
#         "ESFP": {
#             "name": "The Performer",
#             "strengths": ["Bold", "Original", "Practical", "Observant", "Excellent people skills"],
#             "weaknesses": ["Sensitive", "Easily bored", "Poor long-term planners", "Conflict-averse", "Unfocused"],
#             "description": "ESFPs are spontaneous and outgoing performers who love to entertain and engage with others. They enjoy life and bring joy to those around them."
#         },
#         "ENFP": {
#             "name": "The Inspirer",
#             "strengths": ["Enthusiastic", "Creative", "Sociable", "Energetic", "Perceptive"],
#             "weaknesses": ["Poor practical skills", "Unfocused", "Overly optimistic", "Restless", "Overly accommodating"],
#             "description": "ENFPs are enthusiastic and imaginative individuals who are passionate about exploring new ideas and possibilities. They are empathetic and strive to inspire and motivate others."
#         },
#         "ENTP": {
#             "name": "The Visionary",
#             "strengths": ["Innovative", "Enthusiastic", "Strategic", "Charismatic", "Knowledgeable"],
#             "weaknesses": ["Argumentative", "Insensitive", "Intolerant", "Poor follow-through", "Unfocused"],
#             "description": "ENTPs are innovative and resourceful thinkers who enjoy exploring new concepts and possibilities. They are quick-witted and enjoy debating ideas with others."
#         },
#         "ESTJ": {
#             "name": "The Supervisor",
#             "strengths": ["Dedicated", "Strong-willed", "Direct", "Honest", "Loyal"],
#             "weaknesses": ["Inflexible", "Uncomfortable with unconventional situations", "Judgmental", "Too focused on social status", "Difficult relaxing"],
#             "description": "ESTJs are practical organizers who thrive on order and structure. They are dependable leaders who value tradition and loyalty in their personal and professional lives."
#         },
#         "ESFJ": {
#             "name": "The Provider",
#             "strengths": ["Caring", "Loyal", "Warm", "Organized", "Good at connecting"],
#             "weaknesses": ["Needy", "Inflexible", "Vulnerable to criticism", "Too selfless", "Prone to worry"],
#             "description": "ESFJs are warm-hearted and conscientious individuals who are committed to helping and supporting others. They are dependable and dedicated to creating harmony in their relationships."
#         },
#         "ENFJ": {
#             "name": "The Teacher",
#             "strengths": ["Charismatic", "Reliable", "Natural leaders", "Altruistic", "Empathetic"],
#             "weaknesses": ["Overly idealistic", "Too selfless", "Overly sensitive", "Fluctuating self-esteem", "Struggle with decisions"],
#             "description": "ENFJs are charismatic and inspiring leaders who are dedicated to bringing out the best in others. They are empathetic and compassionate, with a strong sense of social responsibility."
#         },
#         "ENTJ": {
#             "name": "The Commander",
#             "strengths": ["Efficient", "Energetic", "Self-confident", "Strong-willed", "Strategic"],
#             "weaknesses": ["Impatient", "Arrogant", "Intolerant", "Poor handling of emotions", "Cold and ruthless"],
#             "description": "ENTJs are assertive and ambitious leaders who are focused on achieving their goals. They are strategic and decisive, with a natural ability to lead and inspire others."
#         }
#     }

#     mbti_info = mbti_descriptions.get(mbti_type, {
#         "name": "Unknown Type",
#         "strengths": [],
#         "weaknesses": [],
#         "description": "Unfortunately, there is no description available for this MBTI type."
#     })

#     strengths_list = "\n".join(f"- {strength}" for strength in mbti_info["strengths"])
#     weaknesses_list = "\n".join(f"- {weakness}" for weakness in mbti_info["weaknesses"])

#     embed = {
#         'type': 4,
#         'data': {
#             'embeds': [
#                 {
#                     'title': f"MBTI Type: {mbti_info['name']} ({mbti_type})",
#                     'description': mbti_info['description'],
#                     'fields': [
#                         {'name': 'Strengths', 'value': strengths_list, 'inline': False},
#                         {'name': 'Weaknesses', 'value': weaknesses_list, 'inline': False}
#                     ]
#                 }
#             ]
#         }
#     }
#     return success_response(embed)

# async def handle_mbti_command(body_json):
#     conversation_id = body_json.get('channel_id', 'default_channel')
#     return await present_question(conversation_id, 0)

# async def present_question(conversation_id, question_index):
#     if isinstance(question_index, Decimal):
#         question_index = int(question_index)

#     if question_index >= len(quiz_data["questions"]):
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': "Quiz completed! Thank you for your responses."
#             }
#         })

#     question_data = quiz_data["questions"][question_index]
#     question = question_data["question"]
#     choices_text = "\n".join(question_data["choices"])

#     question_text = f"**{question}**\n{choices_text}"
#     question_id = f"mbti_{conversation_id}_{question_index}"

#     try:
#         table.put_item(
#             Item={
#                 'conversationID': conversation_id,
#                 'message_id': question_id,
#                 'question_index': question_index,
#                 'question': question,
#                 'optionA_votes': 0,
#                 'optionB_votes': 0,
#                 'optionC_votes': 0,
#                 'optionD_votes': 0,
#                 'user_votes': []
#             }
#         )
#     except ClientError as e:
#         print(f"Error storing MBTI question in DynamoDB: {e}")
#         return error_response(500, "Internal server error")

#     return success_response({
#         'type': 4,
#         'data': {
#             'content': question_text,
#             'components': [
#                 {
#                     'type': 1,
#                     'components': [
#                         {'type': 2, 'style': 1, 'label': 'A', 'custom_id': f'mbti_optionA_{question_id}'},
#                         {'type': 2, 'style': 1, 'label': 'B', 'custom_id': f'mbti_optionB_{question_id}'},
#                         {'type': 2, 'style': 1, 'label': 'C', 'custom_id': f'mbti_optionC_{question_id}'},
#                         {'type': 2, 'style': 1, 'label': 'D', 'custom_id': f'mbti_optionD_{question_id}'}
#                     ]
#                 }
#             ]
#         }
#     })

# async def handle_mbti_vote(body_json):
#     custom_id = body_json['data']['custom_id']
#     user_id = body_json['member']['user']['id']
#     conversation_id = body_json.get('channel_id', 'default_channel')
#     option = custom_id.split('_')[1]  # 'A', 'B', 'C', or 'D'
#     question_id = '_'.join(custom_id.split('_')[2:])  # Extract the question ID

#     # Ensure option is valid
#     if option not in ['optionA', 'optionB', 'optionC', 'optionD']:
#         return error_response(400, "Invalid option")

#     try:
#         # Retrieve the current state of the question from DynamoDB
#         response = table.get_item(Key={
#             'conversationID': conversation_id,
#             'message_id': question_id
#         })
#     except ClientError as e:
#         print(f"Error retrieving MBTI question from DynamoDB: {e}")
#         return error_response(500, "Internal server error")

#     if 'Item' not in response:
#         return error_response(404, "Question not found")

#     item = response['Item']
#     if user_id in item.get('user_votes', []):
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': "You have already voted for this question.",
#                 'flags': 64
#             }
#         })

#     vote_column = f'{option}_votes'  # Determine which vote column to increment
#     try:
#         # Update the vote count and add user_id to user_votes list
#         table.update_item(
#             Key={'conversationID': conversation_id, 'message_id': question_id},
#             UpdateExpression=f'SET {vote_column} = if_not_exists({vote_column}, :start) + :inc, user_votes = list_append(if_not_exists(user_votes, :empty_list), :user)',
#             ExpressionAttributeValues={
#                 ':inc': 1, 
#                 ':user': [user_id], 
#                 ':empty_list': [], 
#                 ':start': 0  # Initialize the vote column if it doesn't exist
#             }
#         )
#     except ClientError as e:
#         print(f"Error updating vote in DynamoDB: {e}")
#         return error_response(500, "Internal server error")

#     # Check if it's the last question
#     total_questions = len(quiz_data["questions"])
#     current_question_index = item['question_index']
#     if current_question_index + 1 >= total_questions:
#         # Retrieve all responses for the conversation
#         try:
#             response = table.scan(
#                 FilterExpression=boto3.dynamodb.conditions.Attr('conversationID').eq(conversation_id)
#             )
#             responses = response.get('Items', [])
#         except ClientError as e:
#             print(f"Error scanning responses from DynamoDB: {e}")
#             return error_response(500, "Internal server error")

#         # Calculate MBTI type based on user responses
#         mbti_type = calculate_mbti_type(responses)

#         # Send MBTI report
#         return await send_mbti_report(conversation_id, mbti_type)

#     # Otherwise, proceed to the next question
#     next_question_index = current_question_index + 1

#     return await present_question(conversation_id, next_question_index)

# async def handle_mbti_button_interaction(body_json):
#     custom_id = body_json['data']['custom_id']
#     if custom_id.startswith('mbti_option'):
#         return await handle_mbti_vote(body_json)
#     else:
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': "I'm sorry, I don't recognize that button."
#             }
#         })

# def handle_wyr_button(body_json):
#     custom_id = body_json['data']['custom_id']
#     user_id = body_json['member']['user']['id']
#     conversation_id = body_json.get('channel_id', 'default_channel')
    
#     if custom_id.startswith('wyr_option'):
#         option, question_id = custom_id.split('_')[1], '_'.join(custom_id.split('_')[2:])
#         return handle_vote(conversation_id, question_id, option, user_id)
#     elif custom_id.startswith('wyr_results'):
#         question_id = '_'.join(custom_id.split('_')[2:])
#         return show_wyr_results(conversation_id, question_id)
#     elif custom_id == 'wyr_next':
#         return handle_wyr_command(body_json)

# def handle_vote(conversation_id, question_id, option, user_id):
#     try:
#         response = table.get_item(Key={
#             'conversationID': conversation_id,
#             'message_id': question_id
#         })
#     except ClientError as e:
#         print(f"Error retrieving question from DynamoDB: {e}")
#         return error_response(500, "Internal server error")
    
#     if 'Item' not in response:
#         return error_response(404, "Question not found")
    
#     item = response['Item']
#     if user_id in item['user_votes']:
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': "You have already voted for this question.",
#                 'flags': 64
#             }
#         })
    
#     vote_column = f'option{option[-1]}_votes'
#     try:
#         table.update_item(
#             Key={'conversationID': conversation_id, 'message_id': question_id},
#             UpdateExpression=f'SET {vote_column} = {vote_column} + :inc, user_votes = list_append(user_votes, :user)',
#             ExpressionAttributeValues={':inc': 1, ':user': [user_id]}
#         )
#     except ClientError as e:
#         print(f"Error updating vote in DynamoDB: {e}")
#         return error_response(500, "Internal server error")
    
#     return success_response({
#         'type': 4,
#         'data': {
#             'content': f"You selected Option {option[-1]}!",
#             'flags': 64
#         }
#     })
    
# async def handle_wyr_button_interaction(body_json):
#     custom_id = body_json['data']['custom_id']
#     if custom_id.startswith('wyr_'):
#         return handle_wyr_button(body_json)
#     else:
#         return success_response({
#             'type': 4,
#             'data': {
#                 'content': "I'm sorry, I don't recognize that button."
#             }
#         })

# def show_wyr_results(conversation_id, question_id):
#     try:
#         response = table.get_item(Key={
#             'conversationID': conversation_id,
#             'message_id': question_id
#         })
#     except ClientError as e:
#         print(f"Error retrieving question from DynamoDB: {e}")
#         return error_response(500, "Internal server error")
    
#     if 'Item' not in response:
#         return error_response(404, "Question not found")
    
#     item = response['Item']
#     question = item['question']
#     option1_votes = item['option1_votes']
#     option2_votes = item['option2_votes']
#     total_votes = option1_votes + option2_votes

#     if total_votes == 0:
#         percentage1 = 0
#         percentage2 = 0
#     else:
#         percentage1 = (option1_votes / total_votes) * 100
#         percentage2 = (option2_votes / total_votes) * 100

#     return success_response({
#         'type': 4,
#         'data': {
#             'content': f"**Results for:**\n{question}\n\nOption 1: {percentage1:.1f}% ({option1_votes} votes)\nOption 2: {percentage2:.1f}% ({option2_votes} votes)\n\nTotal votes: {total_votes}",
#             'flags': 64
#         }
#     })

# def error_response(status_code, message):
#     return {
#         'statusCode': status_code,
#         'body': json.dumps({'error': message})
#     }

# def success_response(body):
#     return {
#         'statusCode': 200,
#         'body': json.dumps(body)
#     }

# def error_response(status, message):
#     return {
#         "statusCode": status,
#         "body": json.dumps({
#             "message": message
#         })
#     }

# def success_response(body):
#     return {
#         'statusCode': 200,
#         'headers': {
#             'Content-Type': 'application/json'
#         },
#         'body': json.dumps(body)
#     }