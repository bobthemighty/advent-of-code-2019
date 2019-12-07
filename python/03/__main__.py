from wire import Wire
import fileinput

def read():
     [line1, line2] = fileinput.input()
     return Wire(line1.split(',')), Wire(line2.split(','))

if __name__ == "__main__":
  a, b = read()
  print(a.closest_intersection(b).distance)
