import pandas as pd
import numpy as np


class StringsFinder:
    def __init__(self):
        self.frame_rules = [10, 12]
        self.df = pd.read_csv("azwel_frame_data.csv")
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
        
        
    def preprocess(self):
        self.df.fillna(value={"hit_type" : "none"}, inplace=True)
        self.df.fillna(value={"attack_type" : "none"}, inplace=True)



    def validateCost(self, f, cost, command_a, command_b):
        if cost <= 0:
            if command_a[self.hit_type] == "KND" or command_a[self.hit_type] == "STN" and command_a[self.sleep] == 1:
                return True
                #self.strings_list.append([str(f) +"F:", command_a[self.command], command_b[self.command]])
                #if verpose:
                #    print(str(cost)+"F", command_a[self.command], command_b[self.command])
            else:
                return False
            
                
        elif cost < f:
            return True
                #self.strings_list.append([str(cost)+"F", command_a[self.command], command_b[self.command]])
                #if verpose:
                #    print(command_a[self.command], command_b[self.command])

        else:
            return False
                
        
    def generateString(self, command_a, command_b, verpose=False):
        for f in self.frame_rules:
            for t in self.frame_checks:
                if type(command_b[t]) == str:
                    frame_candidates = [int(tp) for tp in command_b[t].split(",")]
                    for candidate in frame_candidates:
                        cost = command_a[self.startup] + candidate
                        if self.validateCost(f, cost, command_a, candidate):
                            self.strings_list.append([str(cost)+"F:",command_a[self.command], command_b[self.command]])
                            if verpose:
                                print(str(cost)+"F " +  command_a[self.required_state].required_state + " "+ self.columns[t], command_a[self.command], command_b[self.command])
                    continue
                                
                cost = command_a[self.startup] + command_b[t] + self.stancesCost(command_a, command_b)
                
                if self.validateCost(f, cost, command_a, command_b):
                    self.strings_list.append([str(cost) +"F:", command_a[self.command], command_b[self.command]])
                    if verpose:
                        print(str(cost)+"F " + command_a[self.required_state].required_state + " " + self.columns[t], command_a[self.command], command_b[self.command])
                                            
                    
        
    def stancesCost(self, command_a, command_b, SC=False):
        stances_cost = 0

        #print(command_a[self.required_state].required_state)
        #print(command_b[self.end_state].end_state)
        #print(type(command_a[self.required_state]))

        if command_a[self.required_state].required_state is "SC" and not SC:
            stances_cost += np.inf
            
        
        elif command_a[self.required_state].required_state != command_b[self.end_state].end_state:
            if command_a[self.required_state].required_state in self.stances:
                stances_cost += 20
            elif command_b[self.end_state].end_state in self.stances:
                stances_cost += 40
            if command_a[self.required_state].required_state in self.weapon_mode and command_b[self.end_state].end_state != "AM" and not SC:
                stances_cost += np.inf

        elif command_a[self.first] is not command_b[self.end] and command_b[self.end] is not "AM":
            #print(command_a[self.first], command_b[self.end])
            stances_cost += 8
            #if command_a[self.end_state].end_state in self.weapon_mode and 

        return stances_cost
                
    def search(self):
        for i in range(len(self.df)):
            for j in range(len(self.df)):
                self.generateString(self.df.loc[j], self.df.loc[i], verpose=True)
    


if __name__ == "__main__":
    stringFinder = StringsFinder()
    stringFinder.preprocess()
    stringFinder.search()
    print(len(stringFinder.strings_list))
    
