AUTHOR = 'Nancy Ouyang'
SITENAME = 'Nancy Ouyang'
SITESUBTITLE = 'Harvard CS PhD \'23 · MIT MechE BS \'13 · Boston, MA'
SITEURL = ''

# Contact / social links shown in the header
EMAIL = 'nouyang AT alum DOT mit DOT edu'
GITHUB_URL = 'https://github.com/nro-bot'
LINKEDIN_URL = 'https://www.linkedin.com/in/nrobot'
BLOG_URL = 'https://orangenarwhals.com'
AVATAR = '/images/face.jpg'

PATH = 'content'
TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'

# URL structure matching original Hexo config: year/month/title/
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'

# Static asset directories — copy post asset folders alongside articles
STATIC_PATHS = ['images'] + [
    '18-Servo-Hexapod', 'Countertop-Vending-Machine',
    'DIY-Menstrual-Cup', 'EL-Wire-Workshop', 'Feminism-Hackathon-Hack4Fem',
    'Food-Fun', 'Hexapod-Conference-Hexacon', 'LED-Graduation-Cap',
    'MITERS-Seminar-Series', 'NarwhalEdu-Kickstarter', 'POV-yoyo',
    'Projects-I-didn-t-get-around-to-documenting',
    'Rideable-Hexapod', 'Sailboat-Repairs', 'Sailboat-Rudder',
    'Sailing-and-Other-Adventures', 'Sewing-and-Crafts',
    'Six-Axis-Force-Torque-Sensor', 'Staubli-Robot-Arm-Drawing',
    'Strobe-Lab-Schlieren-Technique', 'Swarmbuddies', 'Wifi-Enabled-Robots',
    # Newer articles
    'Digger-Finger', 'Throwdini', 'Inertia-Wheel-Pendulum',
    'PaperSignals', 'Credit-Communities', 'COVID-Activism',
    'PhD-Thesis', 'Path-Planning-Algorithms', 'Ocean-Buoy-Planning',
    'RoCo-Website-Redesign', 'EECS-Robot-Kit', 'Personal-Websites',
    'Laser-Pancakes', 'Translation-Apron', 'Robot-Arm-Assistant',
    'Waveshare-RP2040-LCD', 'Nyancake',
    'UR5-Hand-Tracking', 'Digger-Finger-Press', 'Awards', 'VA-SLUMS-NLP',
]

# Keep asset folders at the same relative path as the article
ARTICLE_EXCLUDES = []

THEME = 'theme'

# Feed generation — disable for local dev
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False

# Preserve extra metadata fields
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.meta': {},
        'markdown.extensions.extra': {},
        'markdown.extensions.codehilite': {'guess_lang': False},
    },
}
