# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from schedule import execute

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(execute, "interval", hours=12)

scheduler.start()