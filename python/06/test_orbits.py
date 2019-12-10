import fileinput

class Universe:

    def __init__(self):
        self.objects = {}

    def add(self, child, parent):
        self[parent].append(self[child])

    def __getitem__(self, name):
        obj = self.objects.get(name)
        if obj is None:
            obj = Mass(name)
            self.objects[name] = obj
        return obj

    @property
    def total_orbits(self):
        return sum(o.orbits for o in self.objects.values())

    def transfer_distance(self, origin, dest):
        origin_to = self[origin].ancestors
        dest_to = self[dest].ancestors
        return min( (origin_to[k] + dest_to[k]) for k in origin_to if k in dest_to )


class Mass:

    def __init__(self, name):
        self.name = name
        self.parent = None

    def append(self, child):
        child.parent = self

    @property
    def orbits(self):
        if self.parent is None:
            return 0
        return 1 + self.parent.orbits

    @property
    def ancestors(self):
        parent = self.parent
        dist = 0
        ancestors = {}
        while parent is not None:
            ancestors[parent.name] = dist
            dist += 1
            parent = parent.parent
        return ancestors


def test_centre():
    obj = Mass('com')
    assert obj.orbits == 0

def test_child():
    com = Mass('com')

    a = Mass('a')
    b = Mass('b')

    a.append(b)
    com.append(a)

    assert a.orbits == 1
    assert b.orbits == 2


def test_total_orbits():

    universe = Universe()
    universe.add('b', 'a')
    universe.add('a', 'com')

    assert universe.total_orbits == 3

def test_acceptance():
    universe = Universe()
    universe.add('b', 'com')
    universe.add('c', 'b')
    universe.add('d', 'c')
    universe.add('e', 'd')
    universe.add('f', 'e')
    universe.add('g', 'b')
    universe.add('h', 'g')
    universe.add('i', 'd')
    universe.add('j', 'e')
    universe.add('k', 'j')
    universe.add('l', 'k')

    assert universe.total_orbits == 42

def test_transfers():
    universe = Universe()
    universe.add('b', 'com')
    universe.add('c', 'b')
    universe.add('d', 'c')
    universe.add('e', 'd')
    universe.add('f', 'e')
    universe.add('g', 'b')
    universe.add('h', 'g')
    universe.add('i', 'd')
    universe.add('j', 'e')
    universe.add('k', 'j')
    universe.add('l', 'k')
    universe.add('you', 'k')
    universe.add('san', 'i')

    assert universe.transfer_distance('you', 'san') == 4

if __name__ == "__main__":
    universe = Universe()
    for parent, child in (line.split(')') for line in fileinput.input()):
        universe.add(child.strip(), parent.strip())

    print(universe.total_orbits)
    print(universe.transfer_distance('YOU', 'SAN'))
