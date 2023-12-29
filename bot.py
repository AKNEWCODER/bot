from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION_FILE = "session.txt"  # File to save the session string

# Check if the session file exists
try:
    with open(SESSION_FILE) as file:
        SESSION = file.read().strip()
except FileNotFoundError:
    print(f"Session file '{SESSION_FILE}' not found. Generating a new session...")

    # Basics
    phone_number = input("Enter your phone number (with country code, e.g., +1234567890): ")
    BotzHubUser = TelegramClient(StringSession(), APP_ID, API_HASH)

    async def create_session():
        await BotzHubUser.connect()
        if not await BotzHubUser.is_user_authorized():
            await BotzHubUser.send_code_request(phone_number)
            client_session = await BotzHubUser.sign_in(phone_number, input("Enter the code: "))
        else:
            client_session = await BotzHubUser.get_me()

        session_string = BotzHubUser.session.save()  # Use save directly on the client's session
        with open(SESSION_FILE, "w") as file:
            file.write(session_string)
        return session_string

    SESSION = BotzHubUser.loop.run_until_complete(create_session())
    print(f"New session created and saved to '{SESSION_FILE}'.")

# Continue with the rest of your code...

FROM_ = config("FROM_CHANNEL")
TO_ = config("TO_CHANNEL")

FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

@BotzHubUser.on(events.NewMessage(incoming=True, chats=FROM))
async def sender_bH(event):
    for i in TO:
        try:
            await BotzHubUser.send_message(
                i,
                event.message
            )
        except Exception as e:
            print(e)

print("Bot has started.")
BotzHubUser.run_until_disconnected()
