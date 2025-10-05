class Constants:
    ## FILES AND FOLDERS
    GAME_FOLDER = "game"
    PROGRESS_FOLDER = "progress"
    CKPT_FILE_PREFIX = "ckpt_"
    FILE_EXTENSION = ".json"

    ## KEYBOARD CONTROLS
    SAVE_KEY = 'z'

    ## LAYOUTS
    WALL = '#'
    FLOOR = '.'
    DOOR = '+'
    STAIRS_DOWN = '>'
    STAIRS_UP = '<'

    ## JSON DATA KEYS
    X = 'x'
    Y = 'y'
    WIDTH = 'width'
    HEIGHT = 'height'
    TILES = 'tiles'
    ROOMS = 'rooms'
    FLOORS_COORD = 'floors_coord'
    DOORS_COORD = 'doors_coord'
    STAIRS_DOWN_COORD = 'stairs_down_coord'
    STAIRS_UP_COORD = 'stairs_up_coord'

    ## EQUIPMENTS
    MAIN_HAND = 'main_hand'
    OFF_HAND = 'off_hand'
    CHEST = 'chest'

    ## TEXTS FOR GAMES - TODO: CAN SUPPORT LOCALIZATION
    START_NEW_TEXT = "Start New Game"
    PLAY_EXISTING_TEXT = "Play Existing Game"
    SELECT_FILE_TEXT = "Select Previous Game"
    CHOOSE_GAME_TEXT = "Choose a Previously Played Game"
    SELECTED_FILE_TEXT = "Loading Game Played On: "
    LOADING_GAME_TEXT = "Loading game..."
    DATA_COLLECTION_TEXT = 'Collecting Data to Save Progress...'
    SAVE_PROCESSING_TEXT = "Processing..."
    SAVE_TEXT = "Saving..."

    ## GAME MODES
    START_NEW_MODE = 1
    PLAY_EXISTING_MODE = 2

    ## TIMESTAMP FORMATS
    TS_FORMAT = "%Y%m%d_%H%M%S"
    TS_DISPLAY_FORMAT = "%Y-%m-%d %H:%M:%S"
