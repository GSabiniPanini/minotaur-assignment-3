In my program I am currently using a 9 threads approach. This is for a realistic testing environment so that i can make use of the cv.notify() to wake up the reporting thread.

If I were to make this program exactly according to specs, where the report thread is activated only at the top of every hour, then there is no need for my report_thread to exist, and i can just use the sleep() function instead of a with cv: wait() function.

