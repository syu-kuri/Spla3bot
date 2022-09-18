import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('spla3_token')
prefix = os.getenv('prefix')
test_guilds = os.getenv('test_guilds')