import random as r
import functools

class Person:
    def __init__(self, size):
        self.size = size

        def __str__(self):
            return "Person of size %s" % self.size

class MakePeople:
    def __init__(self, random_func):
        self.random_func = random_func

    def make_them(self, count):
        return [Person(self.random_func()) for i in range(count)]

#people_maker = MakePeople(functools.partial(r.gauss, 100, 2))
people_maker = MakePeople(123)
persons = people_maker.make_them(100)
for person in persons:
    print(person.size)



