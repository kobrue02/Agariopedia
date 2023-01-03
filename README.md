# Agariopedia: a multiplayer online game encyclopedia
![image](https://user-images.githubusercontent.com/98605019/210316695-f91b30f5-1d3b-483d-87d2-6f6782d08845.png)
## Building a (missing) database for one of the most popular online games of the decade
Agar.io is a free-to-play multiplayer online game, in which players control a cell (or groups of players, also called “clans”) and play against each other:

Players control one or more circular cells in a map representing a Petri dish. The goal is to gain as much mass as possible by eating agar and cells smaller than the player’s cell while avoiding larger ones which can eat the player’s cells. Each player starts with one cell, but players can split a cell into two once it reaches a sufficient mass, allowing them to control multiple cells.

Wikipedia.com
![image](https://user-images.githubusercontent.com/98605019/210316725-f4da1d54-50fb-4298-81f8-4dd57da87b34.png)
Following its release, the game quickly became a global sensation. Popular streamers and youtubers around the world started playing the game, boosting the numbers of new players. The simplicity and the strategic dimension of agar.io appealed universally and the browser version was ranked by Alexa as one of the 1,000 most visited websites in August 2015. The mobile version was equally successful as the application was downloaded 113 million times as of December 2016.

At the time of the project, there was no official ranking of the players or even a list with their names. We decided to take it upon us to create an interactive database for the highest performing players and clans using Google spreadsheets, Python3 and Discord API.

Watching countless hours of gameplay and researching in forums related to the game, we created a database of over 2000 players and 100 clans, as well as tournaments that took place in the game from 2015 to 2021.

Finally, we coded a Discord bot that made the database accessible to anyone, using simple commands on a dedicated Discord server. To this day, there have been around 1000 individual users, making more than 32.000 interactions with the bot, which is running 24/7 on a linux-based web hosting service. The feedback from users has been overwhelmingly positive.
## Creating an interactive database using Discord API and Python 3
The project started in late 2020 when we first began to collect data about as many players as possible. Not only did we collect their nicknames, but also did we store their nationality and clans in the database. When the database reached a content of 1000 players, we began implementing the Discord application, while simultaneously still growing the database.
![gif](https://miro.medium.com/max/828/1*GHigpeCxi0yNhkFVPHnmSQ.gif)
Using the clan command, users can quickly access key information about a clan such as its region, its main country, its foundation date, its founder, trophies it won and a list of its members.

Using the discord API, and various Python3 modules such as numpy and pandas, we coded a tool that searches for certain data in the spreadsheets (specified by the user) and then outputs it as a Discord embed message. To our knowledge, this is the first Discord application of this kind. After releasing the project to the public, we added multiple new features, such as a command that allows user to submit new players to the database, a donation feature and more.
![gif](https://miro.medium.com/max/828/1*jM2DmgvIc00v1Q26g0Y_Xg.gif)
The tournament command is one of the most popular one and allows users to retrace the history of the most famous tournaments that were organized in the game.
## Leaving a legacy
As other more important projects entered our lives, we soon lacked the spare time to continue updating and further developing the project. However, the bot is still running and being used hundreds of times every day by a vast number of people. The discord server also progressively became a place for the community of the game to reunite, even after the game becoming less active.

A project by Clément Bret and Konrad Brüggemann.

