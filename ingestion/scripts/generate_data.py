import csv
import random
import datetime
from faker import Faker
import os

fake = Faker()

# Configuration
NUM_USERS = 100
NUM_ORDERS = 500
NUM_PAGE_VIEWS = 2000
OUTPUT_DIR = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_users(filename):
    print(f"Generating {NUM_USERS} users...")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'email', 'first_name', 'last_name', 'created_at', 'updated_at'])
        
        for i in range(1, NUM_USERS + 1):
            created_at = fake.date_time_between(start_date='-2y', end_date='now')
            updated_at = fake.date_time_between(start_date=created_at, end_date='now')
            writer.writerow([
                i,
                fake.email(),
                fake.first_name(),
                fake.last_name(),
                created_at,
                updated_at
            ])

def generate_orders(filename):
    print(f"Generating {NUM_ORDERS} orders...")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'user_id', 'status', 'order_date', 'amount'])
        
        for i in range(1, NUM_ORDERS + 1):
            user_id = random.randint(1, NUM_USERS)
            status = random.choice(['pending', 'shipped', 'delivered', 'cancelled', 'returned'])
            order_date = fake.date_time_between(start_date='-2y', end_date='now')
            amount = round(random.uniform(10.0, 500.0), 2)
            writer.writerow([
                i,
                user_id,
                status,
                order_date,
                amount
            ])

def generate_page_views(filename):
    print(f"Generating {NUM_PAGE_VIEWS} page views...")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['event_id', 'user_id', 'session_id', 'page_url', 'event_timestamp', 'device_type'])
        
        for i in range(1, NUM_PAGE_VIEWS + 1):
            user_id = random.randint(1, NUM_USERS) if random.random() > 0.3 else '' # Some anonymous traffic
            session_id = fake.uuid4()
            page = random.choice(['/', '/products', '/cart', '/checkout', '/account'])
            timestamp = fake.date_time_between(start_date='-1y', end_date='now')
            device = random.choice(['desktop', 'mobile', 'tablet'])
            
            writer.writerow([
                fake.uuid4(),
                user_id,
                session_id,
                page,
                timestamp,
                device
            ])

if __name__ == "__main__":
    generate_users(os.path.join(OUTPUT_DIR, "users.csv"))
    generate_orders(os.path.join(OUTPUT_DIR, "orders.csv"))
    generate_page_views(os.path.join(OUTPUT_DIR, "page_views.csv"))
    print("Data generation complete.")
