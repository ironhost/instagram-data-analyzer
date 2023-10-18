from instagrapi import Client
import time
import jdatetime
from datetime import datetime
import pytz

def get_instagram_data(username, cl):
    user = cl.user_info_by_username(username)
    
    print(f"\nAnalysis for: {username}")
    print(f"Followers Count: {user.follower_count}")
    print(f"Post Count: {user.media_count}")
    
    stories = cl.user_stories(user.pk)
    print(f"Active Stories Count: {len(stories) if stories else 0}")

    # Retrieve the recent media for the user and limit to the desired number
    medias = cl.user_medias(user.pk)[:5]
    post_num = user.media_count  # Start with the total post count

    for media in medias:
        # Convert to Tehran timezone
        tehran = pytz.timezone('Asia/Tehran')
        dt_object_tehran = media.taken_at.astimezone(tehran)
        
        # Convert date and time to Shamsi (Jalali)
        jalali_date = jdatetime.datetime.fromgregorian(datetime=dt_object_tehran)

        print(f"\nPost #{post_num}")
        print(f"Date and Time: {jalali_date.strftime('%Y-%m-%d %H:%M:%S')}, Likes: {media.like_count}, Comments: {media.comment_count}")
        if media.media_type == 2:  # Video type
            if media.play_count is not None:
                print(f"Video Play Count: {media.play_count}")
            else:
                print("Video Play Count is not available")

        post_num -= 1  # Decrement the post number

if __name__ == "__main__":
    cl = Client()
    cl.login("YOUR_USERNAME", "YOUR_PASSWORD")
    
    usernames = ["PAGEID"]

    for username in usernames:
        get_instagram_data(username, cl)
        time.sleep(10)  # Wait for 10 seconds between requests to avoid rate limits
