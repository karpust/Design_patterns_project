def draw_sprite(arg1, arg2, arg3):
    pass
"""
использовать константы вместо чисел-позиционных аргументов
что бы было понятно где что
"""

draw_sprite(53, 320, 240)


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_X_CENTER = SCREEN_WIDTH / 2
SCREEN_Y_CENTER = SCREEN_HEIGHT / 2
SPRITE_CROSSHAIR = 53

draw_sprite(SPRITE_CROSSHAIR, SCREEN_X_CENTER, SCREEN_Y_CENTER)
