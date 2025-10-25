import colorgram
import turtle as t
import random as r

# rgb_colors = []
# colors = colorgram.extract("Hirstspotpainting.jpeg", 64)
# for color in colors:
#     rgb_colors.append((color.rgb.r, color.rgb.g, color.rgb.b))

def draw_row(n):
    for _ in range(n):
        tim.dot(40, r.choice(rgb_colors))
        tim.forward(dx)

def draw_table(n):
    for i in range(n):
        draw_row(10)
        tim.setposition(dx/2-w/2, 1.5*dy-h/2+i*dy)


rgb_colors = [(144, 76, 50), (188, 165, 117), (248, 244, 246), (166, 153, 36), (14, 46, 85), (139, 185, 176), (146, 56, 81), (42, 110, 136), (59, 120, 99), (145, 170, 177), (87, 35, 30), (64, 152, 169), (220, 209, 93), (110, 37, 31), (100, 145, 111), (165, 99, 131), (91, 122, 172), (158, 138, 158), (177, 104, 82), (55, 52, 85), (206, 182, 195), (68, 48, 63), (73, 51, 71), (173, 201, 194), (175, 198, 201), (213, 182, 176), (37, 47, 45), (14, 101, 109), (188, 190, 201), (11, 112, 104), (65, 66, 58)]
t.colormode(255)
tim = t.Turtle()
screen = t.Screen()
w=screen.window_width()
h=screen.window_height()
dx = w/10
dy = h/10
tim.hideturtle()
tim.penup()
tim.speed("fastest")
tim.setposition(dx/2-w/2, dy/2-h/2)
draw_table(10)

screen.exitonclick()