from importlib import __import__
from support import load_config
# game setup
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'invisible': 0}

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 64
UI_FONT = '../fonts/helvetica_regular.otf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#1e7cb8'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#c0c0c0'
TEXT_COLOR = '#EEEEEE'

# ui colors
COLOR_FONT = 'white'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

PATH_ANIMATIONS = "../graphics/images/animations"
PATH_ICONS = "../graphics/images/icons"
PATH_SPRITES = "../graphics/images/sprites"
#music
translation = {'health': 'Здоровье', 'energy': 'Энергия',
                    'intelligence': 'Интеллект', 'body_type': 'Телосложение',
                    'power': 'Сила', 'dexterity': 'Ловкость'
    		, 'attack': 'Физический урон', 'magic': 'Магический урон', 'speed': 'Скорость'}


sittings = load_config()

__import__('config',globals=sittings)