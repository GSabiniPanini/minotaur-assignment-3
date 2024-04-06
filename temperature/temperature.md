In my program I am currently using a 9 threads approach. This is for a realistic testing environment so that i can make use of the cv.notify() to wake up the reporting thread.

If I were to make this program exactly according to specs, where the report thread is activated only at the top of every hour, then there is no need for my report_thread to exist, and i can just use the sleep() function instead of a with cv: wait() function.

to run just use:
```
python3 temperature.py
```

In regards to efficiency, i'd argue that the data updates are bound to start lagging as time goes on. In my eyes the data updating is working on more of a time faith based approach. Since the beginning threads were started before the compiler thread, and the runtime of each individual thread should be substantially lower than the compiler thread, each thread should be able to finish their "work" in the "1 second" timer that the compiler function is running on, effectively mimicing the 1 second report update. 

In reality, the worker threads should be updating slightly ahead of schedule, and may even double update before the next compiler update if any part of the processing slows down/speeds up enough.

