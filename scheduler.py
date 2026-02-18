from apscheduler.schedulers.background import BackgroundScheduler
import time

def send_reminder():
    print("Reminder: Don't forget to complete your habits today!")

scheduler = BackgroundScheduler()
scheduler.add_job(send_reminder, 'interval', hours=24)
scheduler.start()