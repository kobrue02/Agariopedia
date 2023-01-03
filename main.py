import random
import discord
import pandas as pd

from discord.ext import commands
from collections import Counter

from fixer_functions import *
from dataframes import *
from dicts_and_lists import *

# Discord Bot Setup

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='?', help_command=None, intents=intents)


# COMMANDS

# bot gets online
@client.event
async def on_ready():
    """ sends a message letting users know its online """
    general_channel = client.get_channel(819688696172642384)
    await general_channel.send('Agariopedia is now online! Use Prefix "?" to use me.')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('type ?help'))


# bot disconnects
@client.event
async def on_disconnect():
    """ sends a message when disconnecting """
    general_channel = client.get_channel(819688696172642384)
    await general_channel.send('I am now offline.')


# Commands

# Outputs the current version
@client.command(name='version')
async def version(context):
    """ sends some information on the current version of the bot """
    versionEmbed = discord.Embed(title="Current Version", description="The bot is in Version 2.2.0",
                                 color=0x7930a1)
    versionEmbed.add_field(name="Version Code:", value="v2.2.0", inline=False)
    versionEmbed.add_field(name="Date released:", value="10.03.2021", inline=False)
    versionEmbed.set_author(name="Agariopedia")
    await context.message.channel.send(embed=versionEmbed)


# Outputs the best players
@client.command(name='best')
async def best(context):
    """ outputs the two best players """
    bestEmbed = discord.Embed(title="Agariopedia", description="The best Agario Players are:", color=0x7930a1)
    bestEmbed.add_field(name="Hot Doge", value=Dict_Flags.get("France"))
    bestEmbed.add_field(name='Mugge', value=Dict_Flags.get("Germany"))
    await context.message.channel.send(embed=bestEmbed)


# Outputs a link to Agariopedia
@client.command(name='link')
async def link(context):
    """ links the spreadsheet """
    await context.message.channel.send(
        "Here's a link to Agariopedia:\n"
        "https://docs.google.com/spreadsheets/d/1UbGiZALJJW9jPbBr55x4OWhufO7-VYe1eEioqOyfJLU/edit#gid=1280618526")


# DMs the User a list of commands
@client.command(name='help')
async def help(context):
    helpEmbed = discord.Embed(title="Help Menu", description="Here's a list of currently supported commands.",
                              color=0x7930a1)
    helpEmbed.add_field(name='?player',
                        value='searches for a player in the agariopedia and outputs his country and clan association ',
                        inline=False)
    helpEmbed.add_field(name='?clan',
                        value='looks up a clan in the agariopedia and lists its members, '
                              'founders, region and other infos.'
                              ' for a list of all clans and their shortcuts use ?clans',
                        inline=False)
    helpEmbed.add_field(name='?country',
                        value='lists all players from a given country',
                        inline=False)
    helpEmbed.add_field(name='?tourney',
                        value='outputs information for a specified tournament. '
                              'use ?tourneys for a list of all the tournaments in our database.')
    helpEmbed.add_field(name='?skin',
                        value='needs either a clan or "random" as an argument. '
                              'for example "?skin supreme" outputs an album with supreme skins',
                        inline=False)
    helpEmbed.add_field(name='?vid', value='Randomly links a (good) Agar video from YouTube.', inline=False)
    helpEmbed.add_field(name='?donate', value='Sends a link to our Paypal MoneyPool.', inline=False)
    helpEmbed.add_field(name="?version", value="outputs the current version of the bot", inline=False)
    helpEmbed.add_field(name='?link', value="links the official Agariopedia Docs.", inline=False)
    helpEmbed.add_field(name="?best", value="outputs the 2 best Agario Players in history.", inline=False)

    helpEmbed.set_author(name='"' + random.choice(quotes) + '"')
    await context.message.author.send(embed=helpEmbed)


def get_clan(player):
    clan = player_data[player_data['Name'] == player]['Clan'].values[0]
    return clan


def get_flag(p):
    flag = Dict_Flags[p]
    return flag


# List all players from given country
@client.command(name='country')
async def country(context, *, index: str):
    index = index.title()
    country_list = list(player_data[player_data['Country'] == index]['Name'])
    country_players = list(country_list)
    countryEmbed = discord.Embed(title=index.upper(), description='Players:', color=0x7930a1)

    j = 0
    if not player_data[player_data['Country'].values == index].empty:
        for player in country_players:
            j += 1
            if j % 25 != 0 and j < 25:
                countryEmbed.add_field(name=get_flag(index) + ' ' + name_fix(player), value=get_clan(player), inline=True)
            else:
                if j % 25 == 0:
                    await context.message.channel.send(embed=countryEmbed)
                    countryEmbed = discord.Embed(color=0x7930a1)
            if j > 25 and (j % 25 != 0):
                countryEmbed.add_field(name=get_flag(index) + ' ' + name_fix(player), value=get_clan(player), inline=True)
        await context.message.channel.send(embed=countryEmbed)
    else:
        await context.message.channel.send("Sorry, I couldn't find any players from '" + index + "'. Check spelling.")


# Output Clan Panel

@client.command(name='clan')
async def clan(context, *, index: str):
    if index.lower() not in leaderboard:
        leaderboard[index.lower()] = 1
    else:
        leaderboard[index.lower()] += 1
    try:
        clan_name = Dict_Clans.get(index.lower())
        clan_region = clan_data[clan_data['Name'] == clan_name]['Main Region'].values[0]
        clan_main_country = clan_data[clan_data['Name'] == clan_name]['Main Country'].values[0]
        clan_country_emoji = Dict_Flags.get(clan_main_country)
        clan_foundation_date = clan_data[clan_data['Name'] == clan_name]['Foundation Date'].values[0]
        clan_founders = clan_data[clan_data['Name'] == clan_name]['Founders'].values[0]
        clan_importance = clan_data[clan_data['Name'] == clan_name]['Importance'].values[0]
        clan_trophies = clan_data[clan_data['Name'] == clan_name][':Trophy:'].values[0]
        clan_trophies = clan_trophies.replace(",", " :trophy:, ")
        clan_trophies = clan_trophies + ' :trophy:'

        clanEmbed = discord.Embed(title=clan_name, description='Importance: ' + clan_importance, color=0x7930a1)
        clanEmbed.add_field(name='Region', value=clan_region, inline=False)
        clanEmbed.add_field(name='Main Country', value=clan_main_country + ' ' + clan_country_emoji, inline=False)
        clanEmbed.add_field(name='Foundation Date', value=int(clan_foundation_date), inline=False)
        clanEmbed.add_field(name='Founder(s)', value=clan_founders, inline=False)
        clanEmbed.add_field(name='Trophies', value=clan_trophies)


    except:
        await context.message.channel.send("Sorry, I couldn't find the clan you were looking for.")
    else:
        await context.message.channel.send(embed=clanEmbed)
        current_clan_name = Dict_Clans.get(index.lower())
        current_clan = list(player_data[player_data['Clan'].str.contains(clan_fix(current_clan_name), na=True)]['Name'])
        current_clan_members = list(current_clan)
        membersEmbed = discord.Embed(title=current_clan_name, description='Members:', color=0x7930a1)
        j = 0
        for member in current_clan_members:
            j += 1
            player_country = player_data[player_data['Name'] == member]['Country'].values[0]
            player_country_emoji = Dict_Flags.get(player_country)
            if j % 25 != 0 and j < 25:
                membersEmbed.add_field(name=name_fix(member), value=player_country_emoji, inline=False)
            else:
                if j % 25 == 0:
                    await context.message.channel.send(embed=membersEmbed)
                    membersEmbed = discord.Embed(color=0x7930a1)
            if j > 25 and (j % 25 != 0):
                membersEmbed.add_field(name=name_fix(member), value=player_country_emoji, inline=False)

        await context.message.channel.send(embed=membersEmbed)


# Clan Leaderboard
@client.command(name="clanlb")
async def clanlb(context):
    lb = Counter(leaderboard)
    LeaderboardEmbed = discord.Embed(title="Clan Leaderboard",
                                     description="Which clans have been getting the most requests?",
                                     color=0x7930a1)
    for clan, val in lb.most_common(5):
        clan_name = Dict_Clans.get(clan)
        LeaderboardEmbed.add_field(name=clan_name, value=val, inline=False)

    await context.message.channel.send(embed=LeaderboardEmbed)


# Output full info for a given player
@client.command(name='player')
async def player(context, *, args: str):
    try:
        player_country = \
            player_data[player_data['Name'].str.lower() == args.lower()]['Country'].values[0]
        player_clan = player_data[player_data['Name'].str.lower() == args.lower()]['Clan'].values[0]
        player_name = player_data[player_data['Name'].str.lower() == args.lower()]['Name'].values[0]
        country_emoji = Dict_Flags.get(player_country)

        if args in supporters:
            playerEmbed = discord.Embed(title=name_fix(player_name), description=country_emoji,
                                        color=0x7930a1)
            playerEmbed.add_field(name="Country", value=player_country, inline=False)
            playerEmbed.add_field(name="Clan", value=player_clan, inline=False)
            playerEmbed.add_field(name="Description", value=supporters[args.lower()], inline=False)
            playerEmbed.set_author(name="Agariopedia")
        else:
            playerEmbed = discord.Embed(title=name_fix(player_name), description=country_emoji,
                                        color=0x7930a1)
            playerEmbed.add_field(name="Country", value=player_country, inline=False)
            playerEmbed.add_field(name="Clan", value=player_clan, inline=False)
            playerEmbed.set_author(name="Agariopedia")

    except:
        if args in Dict_MultipleNames:
            fixed_name = Dict_MultipleNames.get(args)
            player_country = player_data[player_data['Name'].str.lower() == fixed_name.lower()]['Country'].values[0]
            player_clan = player_data[player_data['Name'].str.lower() == fixed_name.lower()]['Clan'].values[0]
            player_name = player_data[player_data['Name'].str.lower() == fixed_name.lower()]['Name'].values[0]
            country_emoji = Dict_Flags.get(player_country)
            playerEmbed = discord.Embed(title=name_fix(player_name), description=country_emoji,
                                        color=0x7930a1)
            playerEmbed.add_field(name="Country", value=player_country, inline=False)
            playerEmbed.add_field(name="Clan", value=player_clan, inline=False)
            playerEmbed.set_author(name="Agariopedia")
            await context.message.channel.send(embed=playerEmbed)
        else:
            if args.lower() in duplicates:
                name_list = duplicates[args.lower()]
                for name in name_list:
                    if name.lower() in supporters:
                        player_country = \
                            player_data[player_data['Name'].str.lower() == name.lower()][
                                'Country'].values[0]
                        player_clan = \
                            player_data[player_data['Name'].str.lower() == name.lower()]['Clan'].values[0]
                        player_name = player_data[player_data['Name'].str.lower() == name.lower()]['Name'].values[0]
                        country_emoji = Dict_Flags.get(player_country)
                        playerEmbed = discord.Embed(title=name_fix(player_name), description=country_emoji,
                                                    color=0x7930a1)
                        playerEmbed.add_field(name="Country", value=player_country, inline=False)
                        playerEmbed.add_field(name="Clan", value=player_clan, inline=False)
                        playerEmbed.add_field(name="Description", value=supporters[name.lower()], inline=False)
                        playerEmbed.set_author(name="Agariopedia")
                    else:
                        player_country = \
                            player_data[player_data['Name'].str.lower() == name.lower()][
                                'Country'].values[0]
                        player_clan = \
                            player_data[player_data['Name'].str.lower() == name.lower()]['Clan'].values[0]
                        player_name = player_data[player_data['Name'].str.lower() == name.lower()]['Name'].values[0]
                        country_emoji = Dict_Flags.get(player_country)
                        playerEmbed = discord.Embed(title=name_fix(player_name), description=country_emoji,
                                                    color=0x7930a1)
                        playerEmbed.add_field(name="Country", value=player_country, inline=False)
                        playerEmbed.add_field(name="Clan", value=player_clan, inline=False)
                        playerEmbed.set_author(name="Agariopedia")
                    await context.message.channel.send(embed=playerEmbed)


            else:
                await context.message.channel.send(
                    'I couldnt find "' + args + '" in our Database. Perhaps you just misspelled their name?')
    else:
        await context.message.channel.send(embed=playerEmbed)


def get_winner(tourney):
    winner = tourney_data[tourney_data['Tournaments Name'] == tourney]['Winner'].values[0]
    return winner


def get_region(tourney):
    region = tourney_data[tourney_data['Tournaments Name'] == tourney]['Region'].values[0]
    if region == 'America':
        region_emoji = ':earth_americas:'
    elif region == 'Europe':
        region_emoji = ':earth_africa:'
    elif region == 'Worldwide':
        region_emoji = ':map:'
    elif region == 'Asia':
        region_emoji = ':earth_asia:'
    return region_emoji


def get_year(tourney):
    year = tourney_data[tourney_data['Tournaments Name'] == tourney]['Year'].values[0]
    return year


def get_key(val):
    for key, value in Dict_Clans.items():
        if value == val:
            return key

    return "no shortcut"


# find info on given tournament
@client.command(name='tourney')
async def tourney(context, *, index: str):
    try:
        tournament = index
        tournament_winner = tourney_data[tourney_data['Tournaments Name'] == tournament]['Winner'].values[0]
        tournament_challonge = tourney_data[tourney_data['Tournaments Name'] == tournament]['Challonge'].values[0]
        tournament_year = tourney_data[tourney_data['Tournaments Name'] == tournament]['Year'].values[0]
        tournament_region = tourney_data[tourney_data['Tournaments Name'] == tournament]['Region'].values[0]
        tournament_winner_players = tourney_data[tourney_data['Tournaments Name'] == tournament]['Players'].values[0]
        tournament_video = tourney_data[tourney_data['Tournaments Name'] == tournament]['Related Video'].values[0]

        TourneyEmbed = discord.Embed(title=':trophy: ' + tournament, description=tournament_challonge, color=0x7930a1)
        TourneyEmbed.add_field(name='Winner:', value=tournament_winner)
        TourneyEmbed.add_field(name='Year:', value=tournament_year)
        TourneyEmbed.add_field(name='Region:', value=tournament_region + ' ' + get_region(tournament_region))
        TourneyEmbed.add_field(name='Members:', value=tournament_winner_players, inline=False)
        TourneyEmbed.add_field(name='Video:', value=tournament_video, inline=False)
    except:
        await context.message.channel.send("Sorry, I couldn't find that Tournament in our Database.")
    else:
        await context.message.channel.send(embed=TourneyEmbed)


# submission of new players
@client.command(name='submit')
async def submit(context, args1: str, args2: str, args3: str):
    text_file = open("Submissions.txt", "a")
    text_file.write("\nPlayer: " + args1 + " \nCountry: " + args2 + " \nClan: " + args3 + '\n\n')
    await context.message.channel.send('Thanks for your submission. It will shortly be reviewed by Agariopedia Staff.')


@client.command(name='help_submit')
async def help_submit(context):
    submitEmbed = discord.Embed(title='Submissions', description='Using the Submit command you can suggest new Players '
                                                                 'you would like to see added to Agariopedia. '
                                                                 'Please make sure that when submitting a player, '
                                                                 'you follow the template:\n ?submit Name Country Clan',
                                color=0x7930a1)

    await context.message.channel.send(embed=submitEmbed)


# outputs a random skin or clan skin
@client.command(name='skin')
async def skin(context, *args: str):
    channel = client.get_channel(819178564854218762)
    if context.channel == channel:
        if len(args) != 0:
            args = '{}'.join(args)
            if args == 'random':
                random_skin = random.choice(skins)
                await context.message.channel.send(random_skin)
            else:
                try:
                    clan_album = clan_skins.get(args)
                    await context.message.channel.send('Here you go: ' + clan_album)
                except:
                    await context.message.channel.send("Sorry, I couldn't find Skins of that Clan.")
                    print(args)
        else:
            await context.message.channel.send('You need to clarify what skin you are looking for. If you want to '
                                               'generate a random skin, type "?skin random".')
    else:
        await context.message.channel.send('Please go to <#819178564854218762> to use this command.')


# List of all clans and their shortcuts
@client.command(name='clans')
async def clans(context):
    channel = client.get_channel(819989483310284831)
    if context.channel == channel:

        clans_list = clan_data['Name'].to_list()
        ClansEmbed = discord.Embed(title='Clans',
                                   description='Below you can find a list of all clans that are currently '
                                               'in the Agariopedia ClanBase, as well as their shortcut you '
                                               'need in order to find more information on the clan using '
                                               'the ?clan command.', color=0x7930a1)
        j = 0

        for x in clans_list:

            j += 1
            if j % 25 != 0 and j < 25:

                ClansEmbed.add_field(name=x, value=get_key(x), inline=True)
            else:
                if j % 25 == 0:
                    await context.message.channel.send(embed=ClansEmbed)
                    ClansEmbed = discord.Embed(color=0x7930a1)
            if j > 25 and (j % 25 != 0):
                ClansEmbed.add_field(name=x, value=get_key(x), inline=True)

        await context.message.channel.send(embed=ClansEmbed)
    else:
        await context.message.channel.send('You can see the entire list of clans in <#819989483310284831>.')


# Tourneys in given year
@client.command(name='year')
async def year(context, *, index: int):
    tourney_list = tourney_data['Tournaments Name'].to_list()
    TourneysEmbed = discord.Embed(title=index, description="Here's a list of all the tournaments that took "
                                                           "place.", color=0x7930a1)
    j = 0
    for tourney in tourney_list:
        if get_year(tourney) == index:
            j += 1
            if j % 25 != 0 and j < 25:
                TourneysEmbed.add_field(name=tourney, value=get_winner(tourney), inline=True)
            else:
                if j % 25 == 0:
                    await context.message.channel.send(embed=TourneysEmbed)
                    TourneysEmbed = discord.Embed(color=0x7930a1)
            if j > 25 and (j % 25 != 0):
                TourneysEmbed.add_field(name=tourney, value=get_winner(tourney), inline=True)
        else:
            pass
    await context.message.channel.send(embed=TourneysEmbed)


# LIst of all Tourneys
@client.command(name='tourneys')
async def tourneys(context):
    channel = client.get_channel(820007485259644988)
    if context.channel == channel:
        tourney_list = tourney_data['Tournaments Name'].to_list()
        TourneysEmbed = discord.Embed(title='Tournaments :trophy:',
                                      description='Below you can see a list of all the tournaments '
                                                  'that are currently in our Database. To find more '
                                                  'info on a tournament, such as its Challonge link, '
                                                  'winning team and region, simply type ?tourney and '
                                                  'add the name of the tournament as seen in the '
                                                  'list.', color=0x7930a1)
        j = 0

        for tourney in tourney_list:

            j += 1
            if j % 25 != 0 and j < 25:

                TourneysEmbed.add_field(name=tourney + ' ' + get_region(tourney), value=get_winner(tourney),
                                        inline=True)
            else:
                if j % 25 == 0:
                    await context.message.channel.send(embed=TourneysEmbed)
                    TourneysEmbed = discord.Embed(color=0x7930a1)
            if j > 25 and (j % 25 != 0):
                TourneysEmbed.add_field(name=tourney + ' ' + get_region(tourney), value=get_winner(tourney),
                                        inline=True)

        await context.message.channel.send(embed=TourneysEmbed)
    else:
        await context.message.channel.send('See <#820007485259644988> for the list of tournaments.')


@client.command(name='vid')
async def vid(context):
    channel = client.get_channel(818911119489368078)
    if context.channel == channel:
        random_video = random.choice(videos)
        await channel.send(random_video)
    else:
        await context.message.channel.send("Please use this command in <#818911119489368078> only!")


@client.command(name='donate')
async def donate(context):
    await context.message.channel.send(
        "Thank you for being interested in donating money. "
        "Here's a link to our MoneyPool:\n"
        "https://paypal.me/pools/c/8xzTD3obMb")


@client.command(name='ping')
async def ping(context):
    if round(client.latency * 1000) <= 50:
        embed = discord.Embed(title="PING",
                              description=f":ping_pong: Pingpingpingpingping! "
                                          f"The pin is **{round(client.latency * 1000)}** milliseconds!",
                              color=0x44ff44)
    elif round(client.latency * 1000) <= 100:
        embed = discord.Embed(title="PING",
                              description=f":ping_pong: Pingpingpingpingping! "
                                          f"The ping is **{round(client.latency * 1000)}** milliseconds!",
                              color=0xffd000)
    elif round(client.latency * 1000) <= 200:
        embed = discord.Embed(title="PING",
                              description=f":ping_pong: Pingpingpingpingping! "
                                          f"The ping is **{round(client.latency * 1000)}** milliseconds!",
                              color=0xff6600)
    else:
        embed = discord.Embed(title="PING",
                              description=f":ping_pong: Pingpingpingpingping! "
                                          f"The ping is **{round(client.latency * 1000)}** milliseconds!",
                              color=0x990000)
    await context.message.channel.send(embed=embed)


@client.command(name='specialhelp')
async def specialhelp(context):
    help2Embed = discord.Embed(title="Help Menu", description="Here's a list of currently supported commands.",
                               color=0x7930a1)
    help2Embed.add_field(name='?player',
                         value='searches for a player in the agariopedia and outputs his country and clan association ',
                         inline=False)
    help2Embed.add_field(name='?clan',
                         value='looks up a clan in the agariopedia and lists its members, founders, region and other infos. for a list of all clans and their shortcuts use ?clans',
                         inline=False)
    help2Embed.add_field(name='?country',
                         value='lists all players from a given country',
                         inline=False)
    help2Embed.add_field(name='?tourney',
                         value='outputs information for a specified tournament. use ?tourneys for a list of all the tournaments in our database.')
    help2Embed.add_field(name='?skin',
                         value='needs either a clan or "random" as an argument. for example "?skin supreme" outputs an album with supreme skins',
                         inline=False)
    help2Embed.add_field(name='?vid', value='Randomly links a (good) Agar video from YouTube.', inline=False)
    help2Embed.add_field(name='?donate', value='Sends a link to our Paypal MoneyPool.', inline=False)
    help2Embed.add_field(name="?version", value="outputs the current version of the bot", inline=False)
    help2Embed.add_field(name='?link', value="links the official Agariopedia Docs.", inline=False)
    help2Embed.add_field(name="?best", value="outputs the 2 best Agario Players in history.", inline=False)

    help2Embed.set_author(name='"' + random.choice(quotes) + '"')
    await context.message.channel.send(embed=help2Embed)


@client.command(name='faq')
async def faq(context):
    faqEmbed = discord.Embed(title='FAQ', description='Frequently Asked Questions', color=0x7930a1)
    faqEmbed.add_field(name='What is Agariopedia and who created it?',
                       value="Agariopedia is an interactive Database designed to collect and display Data on Agar.io "
                             "Players, Clans and Tournaments. It was founded by Hot Doge and Mugge. The majority of "
                             "all the data was collected by Hot Doge, whereas Mugge developed the Discord Bot.",
                       inline=False)
    faqEmbed.add_field(name='My Name is not in the Database. ☹',
                       value='Feel free to submit yourself to our Database '
                             'by using the “?submit” command. Further '
                             'Information can be found in the help section.', inline=False)
    faqEmbed.add_field(name='Why is my Clan not in the Database?',
                       value="This is mostly because we simply don’t (or "
                             "didn’t) know about your clan. The ClanBase "
                             "is actively expanding, and your clan will "
                             "soon be part of it, if you let us know "
                             "about it.", inline=False)
    faqEmbed.add_field(name='My Clan won tournaments but none of them are indicated.',
                       value="Help expanding the list "
                             "of tournaments! If "
                             "enough data exists on a "
                             "tournament, we will add "
                             "it to the Database and "
                             "assign the victory to "
                             "your Clan.", inline=False)
    faqEmbed.add_field(name="Why is my Clan’s Importance Rating a B when it should be Legendary?",
                       value="Importance Ratings are subjective and are not meant to intrigue any kind of drama. Each "
                             "Clan is rated individually by the Agariopedia Team and Ratings will not be changed.",
                       inline=False)
    faqEmbed.add_field(name='Can I support the team somehow?',
                       value="Yes! We have a PayPal MoneyPool at "
                             "https://www.paypal.com/pools/c/8xzTD3obMb", inline=False)
    await context.message.channel.send(embed=faqEmbed)


# Run the client on the server
client.run('ODE4NDUzMjAzMDc0NDE2NjQx.GeNmfI.LX091fbLuoWXFKrfIw5PyEIdd9jDFLO8PcC49o')
