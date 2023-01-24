from App.Contracts import JobContract


class TestJob(JobContract):
    a: int
    b: str

    def __init__(self, a: int, b: str):
        self.a = a
        self.b = b

    def handle(self):
        print(self.a, self.b)
