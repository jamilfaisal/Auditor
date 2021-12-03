import pandas as pd
from AuditorBot import AuditorBot
from config import settings


df = pd.read_json('course_data/2021-2022.json').T

AuditorBot.run(settings.auditor_bot_token)
