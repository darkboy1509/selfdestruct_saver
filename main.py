import asyncio
import logging
from telethon import TelegramClient, events
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

api_id = 'API id' # Replace with your actual API ID
api_hash = 'HASH id'  # Replace with your actual API hash

async def main():
    try:
        async with TelegramClient('arshia', api_id, api_hash) as client:
            logger.info("Bot connected and running.")
            
            @client.on(events.NewMessage(func=lambda e: e.is_private and e.media_unread))
            async def intelligent_media_handler(event):
                try:
                    if event.photo or event.video:
                        logger.info(f"Processing media from {event.sender.first_name}...")
                        await asyncio.gather(process_media(event, client))
                        logger.info("Media processing complete.")
                except Exception as e:
                    logger.error(f"Error processing media: {e}")

            logger.info("Bot started processing events.")
            await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

async def process_media(event, client):
    try:
        logger.info(f"Downloading media from {event.sender.first_name}...")
        media = await event.download_media()
        sent_time = datetime.now()
        caption = f"Downloaded from {event.sender.first_name} at {sent_time}"
        
        logger.info("Sending media to 'me'...")
        start_time = datetime.now()
        await client.send_file("me", media, caption=caption)
        end_time = datetime.now()
        
        time_taken = end_time - start_time
        time_taken_seconds = time_taken.total_seconds()
        
        save_description = (
            f"Sent at: {sent_time}\n"
            f"Saved at: {end_time}\n"
            f"Time taken to save: {time_taken_seconds:.2f} seconds\n"
            f"Sender username: {event.sender.username}"  # Removed '@' symbol from here
        )
        
        logger.info("Media sent successfully.")
        await event.mark_read()
        logger.info("Event marked as read.")
        
        # Print or log the save_description
        logger.info(save_description)
    except Exception as e:
        logger.error(f"Error processing media: {e}")

if __name__ == "__main__":
    asyncio.run(main())
