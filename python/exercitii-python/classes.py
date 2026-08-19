class Point:
    def move(self):
        print("move")

    def draw(self):
        print("draw")


point1 = Point()
point1.x = 10
point1.y = 20
print(point1.x, point1.y)
point1.draw()

point2 = Point()
point2.x = 10
point2.y = 20
print(point2.x, point2.y)