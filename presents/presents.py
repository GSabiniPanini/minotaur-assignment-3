import threading, time, random

# Basic Linked List classes
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class ConcurrentLinkedList:
    def __init__(self):
        self.head = None
        self.length = 0
        self.lock = threading.Lock()

    # Add nodes to Linked list in order
    # Not used
    def add_present(self, present):
        new_node = Node(present)
        with self.lock:
            if not self.head or present < self.head.data:
                new_node.next = self.head
                self.head = new_node
                self.length += 1
            else:
                current = self.head
                while current.next and current.next.data < present:
                    current = current.next
                new_node.next = current.next
                current.next = new_node
                self.length += 1

    # Add the top node from the present bag
    def add_present_from_bag(self):
        with self.lock:
            value = present_bag.pop()
            new_node = Node(value)
            if not self.head or value < self.head.data:
                new_node.next = self.head
                self.head = new_node
                self.length += 1
            else:
                current = self.head
                while current.next and current.next.data < value:
                    current = current.next
                new_node.next = current.next
                current.next = new_node
                self.length += 1


    # Remove nodes while keeping ascending order 
    # Not used
    def remove_present(self, tag):
        with self.lock:
            if self.head and self.head.data == tag:
                self.head = self.head.next
                self.length -= 1
            else:
                current = self.head
                while current.next and current.next.data != tag:
                    current = current.next
                if current.next:
                    current.next = current.next.next
                    self.length -= 1

    # Remove a node randomly from the current list
    def remove_present_rand(self):
        if not self.head:
            return None
        
        counter = 0
        with self.lock:
            current = self.head
            rand_index = random.randint(0, self.length - 1)    
            
            if rand_index == counter:
                self.head = current.next
                self.length -= 1
            else:
                while rand_index > counter + 1:
                    counter += 1
                    current = current.next
                current.next = current.next.next
                self.length -= 1
            

    # A simple search function
    def search_present(self, tag):
        with self.lock:
            current = self.head
            while current:
                if current.data == tag:
                    return True
                current = current.next
            return False


def servant_task(servant_id, presents_range):
    for i in range(presents_range[0], presents_range[1]):
        # Simulate adding presents in order
        linked_list.add_present_from_bag()
        # Simulate writing thank you card randomly
        linked_list.remove_present_rand()
        
        # Simulate random searches, 1% chance
        if random.random() < 0.01:
            random_index = random.randint(0, num_presents)
            present_found = linked_list.search_present(random_index)
            if present_found:
                print(f'Servant {servant_id} has found gift {random_index}!!! This is exceptionally rare')
            else:
                print(f'Servant {servant_id} gift not found.')

    print(f'{"-" * 5} Servant {servant_id}: {presents_range[0]} - {presents_range[1] + 1} Done {"-" * 5}')

if __name__ == "__main__":
    num_presents = 500000
    num_servants = 4
    present_bag = list(range(num_presents))

    # Un-order the bag
    random.shuffle(present_bag)

    # Calculate presents range for each servant
    presents_per_servant = num_presents // num_servants
    present_ranges = [(i * presents_per_servant, (i + 1) * presents_per_servant) for i in range(num_servants)]
    present_ranges[-1] = (present_ranges[-1][0], num_presents)

    linked_list = ConcurrentLinkedList()

    # Create threads for each servant
    threads = []
    start_time = time.time()
    for i in range(num_servants):
        t = threading.Thread(target=servant_task, args=(i + 1, present_ranges[i]))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()
    elapsed_time = time.time() - start_time

    print(f'All presents sorted and Thank you cards written in {elapsed_time:.2f} seconds')
