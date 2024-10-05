# Cosmetics Store Network Raffle System

This project is a comprehensive system that combines a backend service with a Telegram bot for conducting raffles among cosmetics store networks. The project is written in Python 3.12.5 and utilizes the FastAPI framework for the backend service. The Telegram bot functionality is provided by the aiogram library. User registration for Admin/Manager roles is implemented using the FastAPI_User library based on JWT tokens. All data for registered users, raffles, and their settings is stored in a PostgreSQL database consisting of 6 tables.

The project consists of a backend service and a Telegram bot. It provides full functionality for managing the raffle system. Admin/Manager roles have access to various management features on the website, while user registration and winner selection occur within the Telegram bot - @https://t.me/Raffle_cosmetics_bot.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [User Registration for Raffles](#user-registration-for-raffles)
- [Testing the Software](#testing-the-software)


## Installation

1. Clone the repository:

```bash
git clone https://github.com/Ilya-12345/raffle_bot.git
```

2. Set all dependencies:

```bash
cd /path_to_repository/
pip install -r requirements.txt
```

3. Download the latest revision of alembic

```bash
alembic upgrade head
```

4. Start the program execution and test!


## Features

The bot management and settings include:
- Viewing registered users of all draws -> Admin/Manager
- Viewing registered users by entered draw id -> Admin/Manager
- Viewing all available draws(active/completed) -> Admin/Managet
- Viewing draw information by entered id -> Admin/Manager
- View winners of each raffle -> Admin/Manager
- View all winners of a raffle by its id -> Admin/Manager
- Search for a user by his phone number -> Admin/Manager
- Create a new raffle -> Admin
- Update settings (time range of raffle activity/number of winners) for a raffle by entered id -> Admin


## User Registration for Raffles

How do users register for the drawing? 

1. User, when logged into the bot @https://t.me/Raffle_cosmetics_bot, must enter the command /start to start registration.
2. Then he will be offered 2 questions to which he can answer Yes/No to continue registration (if you answer No, the drawing will be canceled and will have to start again).
3. After answering the questions, the registration process will begin:
   3.1 Enter phone number format 375 XX YYYY-YYY-YY-YYY or 8 0XX YYYY-YYY-YY-YY'
   3.2 Enter full name
   3.3 Check number
4. After successful data entry, the user will be registered and will take part in the drawing
