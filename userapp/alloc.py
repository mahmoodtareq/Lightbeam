from .models import *
from datetime import datetime, timedelta


def update_holder():
    print('############################################')
    print('##########  Periodic Checking ##############')
    print('############################################')
    time_threshold = datetime.now() - timedelta(days=3)
    timeouts = CurrentHolder.objects.filter(date_time__lt=time_threshold)

    for booking in timeouts:
        print('----------------------------------------------')
        print(booking.holder.student_id + ' holding to ' + booking.product.book.name)
        serial = Serial.objects.get(product=booking.product, user=booking.holder)
        print('deleting.. ' + str(serial))
        # booking.delete()
        # serial.delete()

        print('notifying... ' + booking.holder.student_id)
        reject_notif = Notification(user=booking.holder, product=booking.product, type='TH')
        reject_notif.title = 'Booking Timeout - ' + booking.product.book.name
        reject_notif.text = 'You failed to collect book within 3 days. Click to try again.'
        # reject_notif.save()

        next_serial = Serial.objects.filter(serial_no__gt=serial.serial_no).order_by('serial_no').first()
        if next_serial:
            print('next in serial ' + str(next_serial))

            next_holder = CurrentHolder(product=booking.product, holder=next_serial.user)
            # next_holder.save()

            print('notifying... ' + next_serial.user.student_id)
            collect_date = datetime.now() + timedelta(days=3)
            alloc_notif = Notification(user=next_serial.user, product=booking.product, type='CH')
            alloc_notif.title = 'Collect Book - ' + booking.product.book.name
            alloc_notif.text = 'You are next in line. Collect book within ' + str(collect_date)
            # alloc_notif.save()
        print('----------------------------------------------')
