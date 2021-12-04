import discord
import logging
import pandas as pd
from CourseDataCollector import CourseDataCollector
from utils import get_relevant_time_information, filter_database, filter_courses

logging.basicConfig(level=logging.INFO)


class AuditorBot(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: Make the following line dynamic
        self.df = pd.read_json('course_data/2021-2022.json')

    async def on_ready(self):
        print("Logged on as {}".format(self.user))

    @staticmethod
    async def on_guild_join(guild):
        g_channel = discord.utils.find(lambda x: x.name == 'general', guild.text_channels)
        if g_channel and g_channel.permissions_for(guild.me).send_messages:
            await g_channel.send("Hello!")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!check'):
            await self.check(message)
        elif message.content.startswith("!update"):
            await self.update(message)

    @staticmethod
    async def update(message):
        course_data = CourseDataCollector()
        course_data.get_data()
        await message.channel.send("Update Done!")

    async def check(self, message):
        # 1. Get information
        weekday, section, hour = get_relevant_time_information()
        # 2. Filter all valid rows
        filtered_df = filter_database(self.df, weekday, section.value, hour)
        # 3. Instantiate database rows as Course objects
        courses = filter_courses(filtered_df, weekday, hour)
        # 4. Send message to discord channel with course information
        if len(courses) == 0:
            await message.channel.send("No lectures found...")
        for course in courses:
            await message.channel.send(course.format_course())


# TODO: Fill Bot description
bot_description = ""
intents = discord.Intents.default()
auditorBot = AuditorBot(command_prefix='!', description=bot_description, intents=intents)
