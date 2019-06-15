import unittest
import pandas as pd
from azwel_frame import StringsFinder

class TestGrd(unittest.TestCase):
    def test_guard(self):
        columns_ = ["command", "required_state", "end_state", "first", "end", "startup", "Grd", "NH", "CH", "DMG", "GC","direction","height", "sleep", "hit_type", "attack_type"]

        f = 12
        excepted = False

        FrameTest = StringsFinder("azwel_frame_data.csv")
        command_b = FrameTest.df.loc[14]
        command_a = FrameTest.df.loc[0]
        print(command_b)
        print(command_a)
        
        cost = FrameTest.calculateCost(command_a, command_b, command_b[columns_.index("Grd")])
        #print("cost : ", cost)
        actual = FrameTest.validateCost(f, cost,command_a, command_b)

        
        actual_cost = command_a[columns_.index("startup")] - command_b[columns_.index("Grd")]


        excepted_stances = 0
        actual_stances = FrameTest.stancesCost(command_a, command_b)
        print(actual_stances)
        
        
        self.assertEqual(excepted, actual)
        self.assertEqual(actual_cost, cost)
        self.assertEqual(excepted_stances, actual_stances)

if __name__ == "__main__":
    unittest.main()
