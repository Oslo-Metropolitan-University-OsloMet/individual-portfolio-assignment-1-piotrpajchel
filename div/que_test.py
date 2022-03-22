import queue

q = queue.Queue()

a = "Hei test"

q.put(a)

b = q.get()
q.task_done()


print(b)
