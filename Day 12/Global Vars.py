enemies = 1

def increase_enemies():
    global enemies #to modify global
    enemies += 1
    print(enemies)

print(enemies)
increase_enemies()
print(enemies)
