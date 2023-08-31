#------------------------------------------------------------------------------------------------------------------------------------
#
# Cura PostProcessing Script
# Author:   5axes
# Date:     February 28, 2023
#
# Description:  postprocessing script to easily define a MaxFlowTest
#
#------------------------------------------------------------------------------------------------------------------------------------
#
#   Version 1.0 28/02/2023
#
#------------------------------------------------------------------------------------------------------------------------------------

from ..Script import Script
from UM.Application import Application
from UM.Logger import Logger
import re #To perform the search

__version__ = '1.0'

class MaxFlow(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "MaxFlow",
            "key": "MaxFlow",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "startValue":
                {
                    "label": "Start value",
                    "description": "The percentage start value of the Test.",
                    "type": "int",
                    "unit": "%",
                    "default_value": 50
                },
                "valueChange":
                {
                    "label": "Value Increment",
                    "description": "The percentage value change of each block, can be positive or negative. I you want 50 and then 40, you need to set this to -10.",
                    "type": "int",
                    "unit": "%",
                    "default_value": 10
                },
                "changelayer":
                {
                    "label": "Change Layer",
                    "description": "How many layers needs to be printed before the value should be changed.",
                    "type": "int",
                    "default_value": 8,
                    "minimum_value": 1,
                    "maximum_value": 1000,
                    "maximum_value_warning": 100
                },                
                "changelayeroffset":
                {
                    "label": "Change Layer Offset",
                    "description": "If the print has a base, indicate the number of layers from which to start the changes.",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0,
                    "maximum_value": 1000,
                    "maximum_value_warning": 100
                },
                "lcdfeedback":
                {
                    "label": "Display details on LCD",
                    "description": "This setting will insert M117 gcode instructions, to display current modification in the G-Code is being used.",
                    "type": "bool",
                    "default_value": true
                }                
            }
        }"""

    def execute(self, data):

        UseLcd = self.getSettingValueByKey("lcdfeedback")
        StartValue = int(self.getSettingValueByKey("startValue"))
        ValueChange = int(self.getSettingValueByKey("valueChange"))
        ChangeLayer = int(self.getSettingValueByKey("changelayer"))
        ChangeLayerOffset = int(self.getSettingValueByKey("changelayeroffset"))
        ChangeLayerOffset += 2  # Modification to take into account the numbering offset in Gcode
                                # layer_index = 0 for initial Block 1= Start Gcode normaly first layer = 0 

        CurrentValue = StartValue
        Command=""
        max_layer=9999
        
        for layer in data:
            layer_index = data.index(layer)
            
            lines = layer.split("\n")
            for line in lines:                  
                if line.startswith(";LAYER_COUNT:"):
                    max_layer = int(line.split(":")[1])   # Recuperation Nb Layer Maxi
                    # ValueChange = int((EndValue-StartValue)/(max_layer-ChangeLayerOffset))
                    Logger.log('d', 'Max_layer : {}'.format(max_layer))
                    Logger.log('d', 'ValueChange : {}'.format(ValueChange))
                    
                if line.startswith(";LAYER:"):
                    line_index = lines.index(line)
                    # Logger.log('d', 'layer_index : {}'.format(layer_index))
                    # Logger.log('d', 'ChangeLayerOffset : {}'.format(ChangeLayerOffset))

                    if (layer_index==ChangeLayerOffset):
                        Command = "M220 S{:d}".format(int(CurrentValue))
                        lcd_gcode = "M117 Speed S{:d}".format(int(CurrentValue))  
                            
                        lines.insert(line_index + 1, ";TYPE:CUSTOM LAYER")
                        lines.insert(line_index + 2, Command)
                        if UseLcd == True :               
                            lines.insert(line_index + 3, lcd_gcode)
                    elif ((layer_index-ChangeLayerOffset) % ChangeLayer == 0) and ((layer_index-ChangeLayerOffset)>0):
                            CurrentValue += ValueChange
                            Command = "M220 S{:d}".format(int(CurrentValue))
                            lcd_gcode = "M117 Speed S{:d}".format(int(CurrentValue))
                                
                            lines.insert(line_index + 1, ";TYPE:CUSTOM VALUE")
                            lines.insert(line_index + 2, Command)
                            if UseLcd == True :               
                               lines.insert(line_index + 3, lcd_gcode)                                              
            
            # Logger.log('d', 'layer_index : {}'.format(layer_index))
            if  layer_index==(max_layer+1) :
                line_index = len(lines)
                # Logger.log('d', 'line_index : {}'.format(line_index))
                lines.insert(line_index, "M220 S100\n")
                
            result = "\n".join(lines)
            data[layer_index] = result
        
        return data
