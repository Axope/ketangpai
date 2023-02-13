from datetime import datetime

t = datetime.now().strftime("%Y-%m-%d")
f = open(f'log/{t}.log', 'w', encoding='utf-8')
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s,%(lineno)d]:%(message)s',
    stream=f
)
