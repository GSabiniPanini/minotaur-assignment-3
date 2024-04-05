import threading, random, time
import multiprocessing as mp

def temperature_sensor(sensor_id, shared_memory, shared_time, cv):
    # 60 times to add up to an hour since I hate forever loops
    count = 60
    while count > 0:
        temperature = round(random.uniform(-100, 70), 2)
        current_time = time.time()
        # Tell the compiler thread
        with cv:
            shared_time[sensor_id] = current_time
            shared_memory[sensor_id] = temperature
            cv.notify()

        count -= 1

        # Sleep for 1 minute divided by 60 for brevity
        time.sleep(1)  

def compile_report(shared_memory, shared_time, cv):
    total_max_interval = (0, 0)
    total_max_difference = 0
    top_5 = []
    lowest_5 = []

    # 472 times so it gathers data every minute excluding the 1st (8 * 59)
    count = 472
    while count > 0:
        # Wait for an hour divided by 60 for brevity
        with cv:
            cv.wait(timeout=60)

        # Grab temperatures and sort
        temperatures = shared_memory[:]
        temperatures.extend(top_5)
        temperatures.extend(lowest_5)
        temperatures.sort()

        top_5 = temperatures[-5:]
        lowest_5 = temperatures[:5]

        # Find the max difference
        max_difference = calculate_max_difference(temperatures)
        
        if max_difference > total_max_difference:
            total_max_difference = max_difference
            total_max_interval = find_max_difference_interval(temperatures)

        print(f'{"-" * 10} Report {"-" * 10}')
        print("Highest Temperatures: ", top_5)
        print("Lowest Temperatures: ", lowest_5)
        print(f'Total Max Interval: {total_max_interval}')

        count -= 1

def calculate_max_difference(list):
    return max(list) - min(list)

def find_max_difference_interval(list):
    max_temp = max(list)
    min_temp = min(list)
    return (min_temp, max_temp)

if __name__ == "__main__":
    shared_memory = mp.Array('d', [0.0] * 8)
    shared_time = mp.Array('d', [0] * 8)
    cv = threading.Condition()

    threads = []
    for i in range(8):
        sensor_thread = threading.Thread(target=temperature_sensor, args=(i, shared_memory, shared_time, cv))
        sensor_thread.start()
        threads.append(sensor_thread)

    report_thread = threading.Thread(target=compile_report, args=(shared_memory, shared_time, cv))
    report_thread.start()
