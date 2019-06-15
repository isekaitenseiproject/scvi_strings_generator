import unittest
import pandas as pd
from azwel_frame import FrameReader

class TestGrd(unittest.TestCase):
    def test_guard(self):
        value1 = pd.DataFrame([])
        value2 = pd.DataFrame([])
        value3 = 0
