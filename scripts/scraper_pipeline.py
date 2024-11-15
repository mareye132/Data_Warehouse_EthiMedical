from telethon import TelegramClient, errors
import csv
import os
import logging
import asyncio
import re
from dotenv import load_dotenv

# Load environment variables from a .env file for security
load_dotenv()

# Load API credentials securely
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

# Check that credentials are set
if not API_ID or not API_HASH:
    raise ValueError("API_ID and API_HASH must be set in the .env file.")

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to sanitize file names by replacing invalid characters
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title  # Extract the channel's title

        async for message in client.iter_messages(entity, limit=10000):
            media_path = None
            print(f"Processing message ID {message.id}")  # Debug print

            # Download media if it exists and is a photo
            if message.media and hasattr(message.media, 'photo'):
                # Sanitize the filename to avoid errors
                safe_channel_name = sanitize_filename(channel_username)
                filename = f"{safe_channel_name}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)
                logging.info(f"Downloaded media from {channel_title}: {media_path}")

            # Write the channel title along with other data
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])
            logging.info(f"Scraped message ID {message.id} from {channel_title}")

    except errors.FloodWaitError as e:
        logging.warning(f"Rate limited. Need to wait for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logging.error(f"Error scraping {channel_username}: {str(e)}")
        print(f"Error scraping {channel_username}: {e}")  # Debug print

async def main():
    # Prompt for your phone number or bot token
    phone = input("Please enter your phone (or bot token): ")
    
    # Initialize the client with a unique session name to store session details
    client = TelegramClient('telegram_scraper_session', API_ID, API_HASH)

    await client.start(phone)  # This will prompt for a phone number and log in

    # Create a directory for media files
    media_dir = 'C:/Users/user/Desktop/Github/Data_Warehouse_ForEthioMedical/photos'
    os.makedirs(media_dir, exist_ok=True)

    # Open the CSV file and prepare the writer
    with open('C:/Users/user/Desktop/Github/Data_Warehouse_ForEthioMedical/telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])
        
        # List of channels to scrape
        channels = [
            '@DoctorsET',
            '@lobelia4cosmetics',
            '@yetenaweg',
            '@EAHCI'
            # Add more channels as needed
        ]
        
        # Iterate over channels and scrape data
        for channel in channels:
            await scrape_channel(client, channel, writer, media_dir)
            logging.info(f"Scraped data from {channel}")

if __name__ == "__main__":
    asyncio.run(main())
