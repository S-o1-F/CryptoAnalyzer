import sys
import os

#za crypto-analyzer-services
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

#za crypto-analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../crypto-analyzer')))

#selenium
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'tests/selenium_tests')))