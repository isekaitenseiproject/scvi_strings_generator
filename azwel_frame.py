0# -*- coding : utf-8 -*-

__author__  = "Isekai Tensei"
__status__  = "alpha"
__version__ = "0.0.1"
__date__    = "15 June 2019"


import pandas as pd
import numpy as np
from tqdm import tqdm




class StringsFinder:
    """
    A Class for finding attack strings
    """ 
    def __init__(self, path):
        self.frame_rules = [10, 12]
        self.df = pd.DataFrame()
        self.df_sorted = pd.DataFrame()
        
        self.loadData(pd.read_csv(path))

        
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
        self.strings_list = pd.DataFrame([], columns=["command", "state", "startup", "DMG" ,"GC", "direction", "height"])
        self.direction = self.columns.index("direction")
        self.height = self.columns.index("height")
        self.DMG = self.columns.index("DMG")
        self.GC = self.columns.index("GC")

        self.preprocess()

    def loadData(self, data):
        self.df = data
        
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

    def addStrings(self, command_a, command_b, cost, frame_type):
        dmg = 0
        gc = 0
        direction = command_b[self.direction] + "," + command_a[self.direction]
        height = command_b[self.height] +"," + command_a[self.height]
        command = command_b[self.command] + "," + command_a[self.command]
        state = self.columns[self.frame_checks[frame_type]]
        #print(command, direction, height)
        
        if self.columns[self.frame_checks[frame_type]] == "Grd":
            gc += command_b[self.GC]
        else:
            dmg += command_b[self.DMG]
        
        
            
        row = pd.DataFrame([[command, state, cost, dmg, gc, direction, height]],
                           columns=["command", "state", "startup", "DMG" ,"GC", "direction", "height"])

        #print(row)
        self.strings_list = pd.concat([self.strings_list, row])
        #print(self.strings_list)
                
        
    def generateString(self, command_b, verpose=False):
        """
        Strings generator method.
        """
        f = 12
        command_b_frame =  command_b[self.frame_checks[0]:self.frame_checks[len(self.frame_checks)-1] +1]        
        candidates = np.array([[int(i) for i in frame.split(",")] if type(frame) == str else [frame] for frame in command_b_frame])
        value = candidates + f
        
        indexs = list(map(lambda x:list(map(lambda y :abs(self.df_sorted['startup'] - y).idxmin(),x)),value))
        

        command_a = np.array(list(
            map(lambda index : list(map(lambda idx : self.df_sorted.loc[idx], index))
                ,indexs)
        ))
            
        filter_index = list(range(len(command_a)))
        #filter_index = filter(lambda comman : , command_a)
        
        

        notfindBelow = value < self.df_sorted.loc[index]["startup"]
            
        while value < self.df_sorted.loc[index]["startup"] and index >= 0:
            print("hello")
            notfindBelow = value < self.df_sorted.loc[index]["startup"]
            index -= 1


                    
        if notfindBelow:
            pass
            #continue

            
            #check stances cost(linear search)
            while index > 0:
                command_a = self.df_sorted.loc[index]
                cost = self.calculateCost(command_a, command_b, candidates[i])
                is1st = False
                is2nd = False
                is1st = self.validateCost(f, cost[0], command_a, command_b)
                if len(cost) > 1:
                    is2nd = self.validateCost(f, cost[1], command_a, command_b)
            
                if is1st:
                    self.addStrings(command_a, command_b, cost[0], i)
                    if verpose:
                        print(str(cost[0])+"F " +  command_a[self.required_state].required_state + " "+ self.columns[t], command_b[self.command], command_a[self.command])
                if is2nd:        
                    self.addStrings(command_a, command_b, cost[1], i)
                    if verpose:
                        print(str(cost[1])+"F " +  command_a[self.required_state].required_state + " "+ self.columns[t], command_b[self.command], command_a[self.command])

                            
                            

    def calculateCost(self, command_a, command_b, command_b_cost):
        cost = command_a[self.startup] - command_b_cost + self.stancesCost(command_a, command_b)
        return cost
        
        
                            
    def stancesCost(self, command_a, command_b, SC=False):
        """
        Calculating stances cost.
        """
        stances_cost = 0


        
        if command_a[self.required_state].required_state == "SC" and not SC:
            #print("adding inf")
            stances_cost += np.inf

        if command_b[self.required_state].required_state == "SC" and not SC:
            stances_cost += np.inf
            
        elif command_a[self.required_state].required_state != command_b[self.end_state].end_state:
            if command_a[self.required_state].required_state in self.stances:
                #print("cost 20")
                stances_cost += 20
            elif command_b[self.end_state].end_state in self.stances:
                #print("cost 40")
                stances_cost += 40
            else:
                ifWeaponMode = command_a[self.required_state].required_state in self.weapon_mode
                ifAM = command_b[self.end_state].end_state != "AM"
                ifnotSC = not SC
                if ifWeaponMode and ifAM and ifnotSC:
                    #print("no weapon equiped")
                    stances_cost += np.inf


        
        else:
            weaponDifferent= command_a[self.first] != command_b[self.end]
            isnotAM = command_b[self.end] != "AM"
            isnotSC = not SC
            if weaponDifferent and isnotAM and isnotSC:
                stances_cost += 8

        return stances_cost


    def sort(self):
        self.df_sorted = self.df
        required_state_rules = ["normal", "sword", "axe", "spear", "AM", "BoB", "ToW", "CoE", "SC"]
        weapon_mode_rules = ["none", "sword", "axe", "spear", "AM"]

        self.df_sorted["required_state"] = pd.Categorical(self.df_sorted.required_state, ordered=True, categories=required_state_rules)
        self.df_sorted["first"] = pd.Categorical(self.df_sorted["first"], ordered=True, categories=weapon_mode_rules)
        #self.df_sorted["required_state"].cat.reorder_levels(required_state_rules)
        #self.df_sorted["first"].cat.reorder_levels(weapon_mode_rules)
        self.df_sorted = self.df.sort_values(by=["startup", "required_state", "first"], ascending=True)

        print(self.df_sorted)
        #print(self.df_sorted["required_state"].dtypes)
        

        
        
    
    def search(self):
        """
        A method to search attack strings.
        """

        #1. sort startup value
        self.sort()

        f  = 12

        for i in tqdm(range(len(self.df))):
            self.generateString(self.df.loc[i], verpose=True)
            

            
        #    for j in range(len(self.df)):
        #        self.generateString(self.df.loc[j], self.df.loc[i], verpose=False)
        self.strings_list.to_csv("azwel_strings.csv")


                

if __name__ == "__main__":
    stringFinder = StringsFinder("azwel_frame_data.csv")
    stringFinder.search()
    print(len(stringFinder.strings_list))
    
