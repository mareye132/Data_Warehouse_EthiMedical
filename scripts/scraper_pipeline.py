from telethon import TelegramClient
import csv
import os
import logging
import asyncio

# Define API ID and API hash directly in the code
API_ID = 21138037
API_HASH = 'f62291f2ec7170893596772793ead07e'

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title  # Extract the channel's title

        async for message in client.iter_messages(entity, limit=10000):
            media_path = None

            # Download media if it exists and is a photo
            if message.media and hasattr(message.media, 'photo'):
                filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)
                logging.info(f"Downloaded media from {channel_title}: {media_path}")

            # Write the channel title along with other data
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])
            logging.info(f"Scraped message ID {message.id} from {channel_title}")

    except Exception as e:
        logging.error(f"Error scraping {channel_username}: {str(e)}")

async def main():
    # Prompt for your phone number
    phone = input("Please enter your phone (or bot token): ")
    
    # Initialize the client without a session file
    client = TelegramClient('anon', API_ID, API_HASH)

    await client.start(phone)  # This will prompt for a phone number and log in

    # Create a directory for media files
    media_dir = 'photos'
    os.makedirs(media_dir, exist_ok=True)

    # Open the CSV file and prepare the writer
    with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header
        
        # List of channels to scrape
        channels = [
            'DoctorsET',
            'Chemed Telegram Channel',
            'lobelia4cosmetics',
            'yetenaweg',
            'EAHCI',
            
        ]
        
        # Iterate over channels and scrape data into the single CSV file
        for channel in channels:
            await scrape_channel(client, channel, writer, media_dir)
            logging.info(f"Scraped data from {channel}")

if __name__ == "__main__":
    asyncio.run(main())
