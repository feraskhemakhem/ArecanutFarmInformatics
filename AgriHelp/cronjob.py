# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from schedule import execute

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()

"""
The scheduler allows us to create a cronjob which can run every 12 hrs
Hence every 12 hrs, we check the frequency of irrigation timings of the plots
and send the email alerts accordingly
"""
scheduler.add_job(execute, "interval", hours=12)

scheduler.start()