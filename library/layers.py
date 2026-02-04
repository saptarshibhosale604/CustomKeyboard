# layers.py
# --------------------------------------------------
# Layer 01, short pressed, Base layer
# --------------------------------------------------

L1_SHORT = [
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L','SEMICOLON'],
    ['Z','X','C','V','B','N','M','COMMA','PERIOD','SLASH'],
    ['ESC','SPACE','LAYER_UP','','','LAYER_DOWN','ENTER','BACKSPACE','','']
]

L1_LONG = [
    ['1','2','3','4','5','6','7','8','9','0'],
    ['LEFT_GUI','LEFT_ALT','LEFT_CTRL','LEFT_SHIFT','TAB','TAB',
     'RIGHT_SHIFT','RIGHT_CTRL','RIGHT_ALT','RIGHT_GUI'],
    ['FUNCTION_UNDO','FUNCTION_CUT','FUNCTION_COPY','FUNCTION_PASTE',
     'GRAVE','QUOTE','MINUS','EQUAL','LEFT_BRACKET','RIGHT_BRACKET'],
    ['ESC','SPACE','LAYER_TEMP_LAYER_UP_01','','',
     # 'LAYER_TEMP_LAYER_UP_02','FUNCTION_ENTER','DEL','','']
     'LAYER_CHANGE_LAYER','FUNCTION_ENTER','DEL','','']
]

# --------------------------------------------------
# Layer 02, Navigation layer
# --------------------------------------------------

L2_SHORT = [
    ['SPECIAL_TEST','','PAGE_UP','','','','','','',''],
    ['','HOME','PAGE_DOWN','END','','LEFT','DOWN','UP','RIGHT',''],
    ['','FUNCTION_CLOSE','SPECIAL_CAPSLOCK','','','','FUNCTION_ZOOM_OUT','FUNCTION_ZOOM_IN','',''],
    ['ESC','SPACE','LAYER_UP','','','LAYER_DOWN','ENTER','BACKSPACE','','']
]

L2_LONG = [
    ['','','','','','','','','',''],
    ['LEFT_GUI','LEFT_ALT','LEFT_CTRL','LEFT_SHIFT','TAB','TAB',
     'RIGHT_SHIFT','RIGHT_CTRL','RIGHT_ALT','RIGHT_GUI'],
    ['','','','','','','BACKSLASH','PRINT_LEFT_ARROW','PRINT_RIGHT_ARROW',''],
    ['ESC','SPACE','LAYER_TEMP_LAYER_UP_01','','',
     'LAYER_CHANGE_LAYER','FUNCTION_ENTER','DEL','','']
]

# --------------------------------------------------
# Layer 03, FX, media layer
# --------------------------------------------------

L3_SHORT = [
    ['F1','F2','F3','F4','F5','F6','F7','F8','F9','F10'],
    ['F11','F12','','','','MEDIA_PREV_TRACK','MEDIA_PLAY_PAUSE','MEDIA_MUTE','MEDIA_NEXT_TRACK',''],
    ['','','','','','BRIGHTNESS_UP','VOLUME_UP','VOLUME_DOWN','BRIGHTNESS_DOWN',''],
    ['ESC','SPACE','LAYER_UP','','','LAYER_DOWN','ENTER','BACKSPACE','','']
]

L3_LONG = [
    ['','','','','','','','','',''],
    ['LEFT_GUI','LEFT_ALT','LEFT_CTRL','LEFT_SHIFT','TAB','TAB',
     'RIGHT_SHIFT','RIGHT_CTRL','RIGHT_ALT','RIGHT_GUI'],
    ['','','','','','','','','',''],
    ['ESC','SPACE','LAYER_TEMP_LAYER_UP_01','','',
     'LAYER_CHANGE_LAYER','FUNCTION_ENTER','DEL','','']
]

# --------------------------------------------------
# Layer 04, Mouse layer
# --------------------------------------------------

L4_SHORT = [
    ['','','MOUSE_MOVE_UP','','','','','','',''],
    ['','MOUSE_MOVE_LEFT','MOUSE_MOVE_DOWN','MOUSE_MOVE_RIGHT','','','MOUSE_CLICK_LEFT','MOUSE_CLICK_RIGHT','',''],
    # ['','','','','','','MOUSE_SPEED_01','MOUSE_SPEED_02','MOUSE_SPEED_03','MOUSE_SPEED_04'],
    ['','','','','','','MOUSE_SPEED_01','MOUSE_SPEED_04','',''],
    ['ESC','SPACE','LAYER_UP','','','LAYER_DOWN','ENTER','BACKSPACE','','']
]

L4_LONG = [
    ['','','','','','','','','',''],
    ['LEFT_GUI','LEFT_ALT','LEFT_CTRL','LEFT_SHIFT','TAB','TAB',
     'RIGHT_SHIFT','RIGHT_CTRL','RIGHT_ALT','RIGHT_GUI'],
    ['','','','','','','','','',''],
    ['ESC','SPACE','LAYER_TEMP_LAYER_UP_01','','',
     'LAYER_CHANGE_LAYER','FUNCTION_ENTER','DEL','','']
]

# --------------------------------------------------
# Layer 05, Numpad layer
# --------------------------------------------------

L5_SHORT = [
    ['','','','','','7','8','9','0'],
    ['','','','','','4','5','6','0'],
    ['','','','','','1','2','3','0'],
    ['ESC','SPACE','LAYER_UP','','','LAYER_DOWN','ENTER','BACKSPACE','','']
]

L5_LONG = [
    ['','','','','','','','','',''],
    ['LEFT_GUI','LEFT_ALT','LEFT_CTRL','LEFT_SHIFT','TAB','TAB',
     'RIGHT_SHIFT','RIGHT_CTRL','RIGHT_ALT','RIGHT_GUI'],
    ['','','','','','','','','',''],
    ['ESC','SPACE','LAYER_TEMP_LAYER_UP_01','','',
     'LAYER_CHANGE_LAYER','FUNCTION_ENTER','DEL','','']
]
# --------------------------------------------------
# Gaming Layer
# --------------------------------------------------

gamingLayerNumber = 6

# KEY_MATRIX_LAYER_10 = [
L6_SHORT_GAME_01 = [
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L','SEMICOLON'],
    ['Z','X','C','V','B','N','M','COMMA','PERIOD','SLASH'],
    ['ESC','SPACE','LAYER_UP','','','LAYER_DOWN','ENTER','BACKSPACE','','']
]

# --------------------------------------------------
# Layer Change Layer
# --------------------------------------------------

layerChangeLayerNumber = 7

L7_SHORT = [
    ['LAYER_CHANGE_1','LAYER_CHANGE_2','LAYER_CHANGE_3','LAYER_CHANGE_4',
     'LAYER_CHANGE_5','LAYER_CHANGE_6','LAYER_CHANGE_7','LAYER_CHANGE_8',
     'LAYER_CHANGE_9','SPECIAL_QUIT_KEYBOARD'],
    ['','','','','','','LAYER_CHANGE_BASE','LAYER_CHANGE_GAMING','',''],
    ['','','','','','','','','',''],
    ['ESC','SPACE','LAYER_UP','','','LAYER_DOWN','ENTER','BACKSPACE','','']
]

L7_LONG = [
    ['','','','ACTION_REBOOT','','','','','',''],
    ['LEFT_GUI','LEFT_ALT','LEFT_CTRL','LEFT_SHIFT','TAB','TAB',
     'RIGHT_SHIFT','RIGHT_CTRL','RIGHT_ALT','RIGHT_GUI'],
    ['','ACTION_SHUTDOWN','','','','','','','',''],
    ['ESC','SPACE','LAYER_TEMP_LAYER_UP_01','','',
     'LAYER_CHANGE_LAYER','FUNCTION_ENTER','DEL','','']
]

maxLayer = 7

# --------------------------------------------------
# Layer maps (IMPORTANT)
# --------------------------------------------------

LAYER_SHORT_MAP = {
    1: {
        "name": "Primary layer",
        "description": "Default typing layer",
        "layout": L1_SHORT,
    },
    2: {
        "name": "Navigation layer",
        "description": "Page navigation, arrow keys, function keys, caps lock",
        "layout": L2_SHORT,
    },
    3: {
        "name": "FX, media layer",
        "description": "Function keys, Media keys",
        "layout": L3_SHORT,
    },
    4: {
        "name": "Mouse layer",
        "description": "Mouse direction keys, mouse speed keys",
        "layout": L4_SHORT,
    },
    5: {
        "name": "Numpad layer",
        "description": "number pad",
        "layout": L5_SHORT,
    },
    6: {
        "name": "Game Mode 01 layer",
        "description": "Game mode for single player games",
        "layout": L6_SHORT_GAME_01,
    },
    7: {
        "name": "Layer change layer",
        "description": "Layer switching, Global variable change",
        "layout": L7_SHORT,
    },
}

LAYER_LONG_MAP = {
    1: {
        "name": "Secondary layer",
        "description": "Mod keys, number, symbol, functions",
        "layout": L1_LONG,
    },
    2: {
        "name": "",
        "description": "mod keys, symbol, print functions",
        "layout": L2_LONG,
    },
    3: {
        "name": "",
        "description": "",
        "layout": L3_LONG,
    },
    4: {
        "name": "",
        "description": "",
        "layout": L4_LONG,
    },
    5: {
        "name": "",
        "description": "",
        "layout": L5_LONG,
    },
    6: {
        "name": "Game Mode 01 layer",
        "description": "Game mode for single player games",
        "layout": L6_SHORT_GAME_01,  # keeping exactly what you had
    },
    7: {
        "name": "Layer change layer",
        "description": "Actions",
        "layout": L7_LONG,
    },
}

