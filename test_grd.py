import unittest
import pandas as pd
from azwel_frame import StringsFinder

class TestGrd(unittest.TestCase):

    def test_grd(self):
        FrameTest = StringsFinder("azwel_frame_data.csv")
        columns_ = ["command", "required_state", "end_state", "first", "end", "startup", "Grd", "NH", "CH", "DMG", "GC","direction","height", "sleep", "hit_type", "attack_type"]
        f = 12
        excepted = False
        B = 14
        A = 0
        twoA = 8
        
        command_b = FrameTest.df.loc[A]
        command_a = FrameTest.df.loc[twoA]
        print(command_b["command"])
        print(command_a["command"])
        
        cost = FrameTest.calculateCost(command_a, command_b, command_b[columns_.index("Grd")])
        #print("cost : ", cost)
        actual = FrameTest.validateCost(f, cost,command_a, command_b)

        
        actual_cost = command_a[columns_.index("startup")] - command_b[columns_.index("Grd")]

        print(cost)
        print(actual_cost)
        

        excepted_stances = 0
        actual_stances = FrameTest.stancesCost(command_a, command_b)
        #print(actual_stances)
        

        FrameTest.generateString(command_a, command_b)
        print(FrameTest.strings_list)
        
        self.assertEqual(excepted, actual)
        self.assertEqual(actual_cost, cost)
        self.assertEqual(excepted_stances, actual_stances)

if __name__ == "__main__":
    unittest.main()
