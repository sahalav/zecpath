from celery import shared_task


@shared_task
def send_notification():

    print("Notification Sent")

    return "Success"


@shared_task
def test_task():

    print("Celery Working Successfully")

    return "Success"
