from .models import *
from datetime import datetime, timedelta


def update_holder():
    time_threshold = datetime.now() - timedelta(days=3)
    timeouts = CurrentHolder.objects.filter(date_time__lt=time_threshold)

    for booking in timeouts:
        print('----------------------------------------------')
        print(booking.holder.student_id + ' holding to ' + booking.product.book.name)
        serial = Serial.objects.get(product=booking.product, user=booking.holder)
        print('deleting.. ' + str(serial))
        # booking.delete()
        # serial.delete()

        print('notifying...')
        notif = Notification(user=booking.holder, product=booking.product, type='TH')
        notif.title='Rejected Booking due to Timeout'
        notif.text='You failed to collect book within 3 days. Click to try again.'
        # notif.save()


        print('----------------------------------------------')