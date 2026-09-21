import sys
import:.dirname(__file__), '..', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mangum import Mangum
from main import app

handler = Mangum(app, lifespan="off")
