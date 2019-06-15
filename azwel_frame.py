# -*- coding : utf-8 -*-

__author__  = "Isekai Tensei"
__status__  = "alpha"
__version__ = "0.0.1"
__date__    = "15 June 2019"


import pandas as pd
import numpy as np





class StringsFinder:
    """
    A Class for finding attack strings
    """ 
    def __init__(self, path):
        self.frame_rules = [10, 12]
        self.df = pd.read_csv(path)
        self.columns = list(self.df.columns)
        self.frame_checks = [self.columns.index("Grd"), self.columns.index("NH"), self.columns.index("CH")]
        self.required_state = [self.columns.index("required_state")]
        self.end_state = [self.columns.index("end_state")]
        self.stances = ["BoB", "ToW", "CoE"]
        self.weapon_mode = ["sword", "axe", "spear"]
        self.startup = self.columns.index("startup")
        self.command = self.columns.index("command")
        self.first  = self.columns.index("first")
        self.end = self.columns.index("end")
        self.sleep = self.columns.index("sleep")
        self.hit_type = self.columns.index("hit_type")
        self.strings_list = []
        self.preprocess()
        
    def preprocess(self):
        """
        Preprocessing Data
        """
        self.df.fillna(value={"hit_type" : "none"}, inplace=True)
        self.df.fillna(value={"attack_type" : "none"}, inplace=True)        


    def validateCost(self, f, cost, command_a, command_b):
        """
        Cost validation method. When in combo status and attack strings
        """
        
        if cost <= 0:
            if command_b[self.hit_type] == "KND" or command_b[self.hit_type] == "STN":
                if command_a[self.sleep] == 1:
                    return True
                else:
                    return False
        else:
            rule = cost < f
            return rule
                
        
    def generateString(self, command_a, command_b, verpose=False):
        """
        Strings generator method.
        """
        
        for f in self.frame_rules:
            for t in self.frame_checks:
                candidates = [int(i) for i in  command_b[t].split(",")] if isinstance(command_b[t], str) else [command_b[t]]
                for candidate in candidates:
                    cost = command_a[self.startup] + candidate + self.stancesCost(command_a, command_b)
                    if self.validateCost(f, cost, command_a, command_b):
                        self.strings_list.append([str(cost)+"F:",command_a[self.command], command_b[self.command]])
                        if verpose:
                            print(str(cost)+"F " +  command_a[self.required_state].required_state + " "+ self.columns[t], command_a[self.command], command_b[self.command])
                continue
                                                                            
                    
        
    def stancesCost(self, command_a, command_b, SC=False):
        """
        Calculating stances cost.
        """
        
        stances_cost = 0


        #print(command_a[self.required_state])
        if command_a[self.required_state].required_state == "SC" and not SC:
            stances_cost += np.inf
            
        
        elif command_a[self.required_state].required_state != command_b[self.end_state].end_state:
            if command_a[self.required_state].required_state in self.stances:
                stances_cost += 20
            elif command_b[self.end_state].end_state in self.stances:
                stances_cost += 40
            if command_a[self.required_state].required_state in self.weapon_mode and command_b[self.end_state].end_state != "AM" and not SC:
                stances_cost += np.inf

        elif command_a[self.first] is not command_b[self.end] and command_b[self.end] is not "AM" and not SC:
            stances_cost += 8

        return stances_cost
                
    def search(self):
        """
        A method to search attack strings.
        """
        for i in range(len(self.df)):
            for j in range(len(self.df)):
                self.generateString(self.df.loc[j], self.df.loc[i], verpose=True)
    


if __name__ == "__main__":
    stringFinder = StringsFinder("azwel_frame_data.csv")
    stringFinder.search()
    print(len(stringFinder.strings_list))
    
