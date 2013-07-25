# -*- coding: utf-8 -*-
"""
:Module: statistics.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Read, process, plot, and print information about an output file created 
by the WATER application.

"""

import numpy as np
import datetime
import Tkinter, tkFileDialog
import matplotlib.pyplot as plt  

def read_water(water_file):
    """
    Read data from a WATER output file.
    
    *Parameters:*
        water_file : path to text file from WATER application
    
    *Return:*
        water_data : dictionary holding all data from a WATER file
        
        water_data = {
            'date': dateObj,    
            'discharge': discharge,
            'subsurface flow': subsurfaceFlow,
            'impervious flow': imperviousFlow,
            'infiltration excess': infiltrationExcess,
            'initial abstracted flow': initialAbstractedFlow,
            'overland flow': overlandFlow,
            'pet': pet,
            'aet': aet,
            'average soil root zone': averageSoilRootZone,
            'average soil upper zone': averageSoilUpperZone,
            'snow pack': snowPack,
            'precipitation': precipitation
        }
        
    ** The following are the data *Parameters:* from a WATER file:
        Date                          
        Discharge                             
        Subsurface Flow                       
        Impervious Flow                        
        Infiltration Excess                    
        Initial Abstracted Flow                 
        Overland Flow                        
        PET                                  
        AET                                    
        Average Soil Root Zone               
        Average Soil Upperzone              
        Snow Pack                         
        Precipitation                          
    
    """
    
    # Open file
    f = open(water_file,'r')
    
    # Read all data 
    dataFile = f.readlines()                       
    
    # Close file
    f.close()
    
    # WATER parameter names
    date_code = 'Date'    
    discharge_code = 'Discharge (cfs)'
    subsurfaceFlow_code = 'Subsurface Flow (cfs)'
    imperviousFlow_code = 'Impervious Flow (mm)'
    infiltrationExcess_code = 'Infiltration Excess (mm)'    
    initialAbstractedFlow_code = 'Initial Abstracted Flow (mm)'
    overlandFlow_code = 'Overland Flow (mm)'
    pet_code = 'PET (mm)'
    aet_code = 'AET(mm)'
    averageSoilRootZone_code = 'Average Soil Root zone (mm)'
    averageSoilUpperZone_code = 'Average Soil Upperzone (mm)'
    snowPack_code = 'Snow Pack (mm)'
    precipitation_code = 'Precipitation (mm)'
        
    # Find data using idx as an iterator; assign iterator to index once search
    # word is found
    searchword = date_code
    k = 0
    for line in dataFile:
        if searchword == line.split('\t')[0]:
            idx = k
        else:
            k = k + 1        
    
    # read parameter row and strip any new line characters
    parameterRow = dataFile[idx].split('\t')
    dataCols = []
    for param in parameterRow: 
        dataCols.append(param.strip())
    
    # Assign each parameter index variable to None to make sure that each parameter has data
    date_idx = None
    discharge_idx = None
    subsurfaceFlow_idx = None
    imperviousFlow_idx = None
    infiltrationExcess_idx = None
    initialAbstractedFlow_idx = None
    overlandFlow_idx = None
    pet_idx = None
    aet_idx = None
    averageSoilRootZone_idx = None
    averageSoilUpperZone_idx = None
    snowPack_idx = None
    precipitation_idx = None
    
    # Find index for each parameter in dataCols list
    date_idx = dataCols.index(date_code)
    discharge_idx = dataCols.index(discharge_code)
    subsurfaceFlow_idx = dataCols.index(subsurfaceFlow_code)
    imperviousFlow_idx = dataCols.index(imperviousFlow_code)
    infiltrationExcess_idx = dataCols.index(infiltrationExcess_code)
    initialAbstractedFlow_idx = dataCols.index(initialAbstractedFlow_code)
    overlandFlow_idx = dataCols.index(overlandFlow_code)
    pet_idx = dataCols.index(pet_code)
    aet_idx = dataCols.index(aet_code)
    averageSoilRootZone_idx = dataCols.index(averageSoilRootZone_code)
    averageSoilUpperZone_idx = dataCols.index(averageSoilUpperZone_code)
    snowPack_idx = dataCols.index(snowPack_code)
    precipitation_idx = dataCols.index(precipitation_code)
        
    # Skip next line to get to data of interest by increasing index
    idx = idx + 1
    
    # Get data of interest
    date = []
    discharge = []
    subsurfaceFlow = []
    imperviousFlow = []
    infiltrationExcess = []
    initialAbstractedFlow = []
    overlandFlow = []
    pet = []
    aet = []
    averageSoilRootZone = []
    averageSoilUpperZone = []
    snowPack = []
    precipitation = []
    for row in dataFile[idx:]:
        try:
            if date_idx is not None:
                date.append(row.split('\t')[date_idx])
            if discharge_idx  is not None:
                discharge.append(float(row.split('\t')[discharge_idx]))
            if subsurfaceFlow_idx  is not None:
                subsurfaceFlow.append(float(row.split('\t')[subsurfaceFlow_idx]))
            if imperviousFlow_idx  is not None:
                imperviousFlow.append(float(row.split('\t')[imperviousFlow_idx]))
            if infiltrationExcess_idx  is not None:
                infiltrationExcess.append(float(row.split('\t')[infiltrationExcess_idx]))
            if initialAbstractedFlow_idx  is not None:
                initialAbstractedFlow.append(float(row.split('\t')[initialAbstractedFlow_idx]))
            if overlandFlow_idx  is not None:
                overlandFlow.append(float(row.split('\t')[overlandFlow_idx]))
            if pet_idx  is not None:
                pet.append(float(row.split('\t')[pet_idx]))
            if aet_idx  is not None:
                aet.append(float(row.split('\t')[aet_idx]))
            if averageSoilRootZone_idx  is not None:
                averageSoilRootZone.append(float(row.split('\t')[averageSoilRootZone_idx]))
            if averageSoilUpperZone_idx  is not None:
                averageSoilUpperZone.append(float(row.split('\t')[averageSoilUpperZone_idx]))
            if snowPack_idx  is not None:
                snowPack.append(float(row.split('\t')[snowPack_idx]))
            if precipitation_idx  is not None:
                precipitation.append(float(row.split('\t')[precipitation_idx]))
        except:
            print 'Missing data after date and time %s' %date[-1]
    

    # Convert date and times to a data object
    dateObj = []
    for val in date:
        
        # Get date values from each date
        month = val.split('/')[0]
        day = val.split('/')[1]
        year = val.split('/')[2]
            
        # Assign date values to a datetime object
        d = datetime.datetime(int(year),int(month),int(day))

        # Append data to dataObj list
        dateObj.append(d)
        
    # Convert data parameters to numpy arrays.
    dateObj = np.array(dateObj)  
    discharge = np.array(discharge)
    subsurfaceFlow = np.array(subsurfaceFlow)
    imperviousFlow = np.array(imperviousFlow)
    infiltrationExcess = np.array(infiltrationExcess)
    initialAbstractedFlow = np.array(initialAbstractedFlow)
    overlandFlow = np.array(overlandFlow)
    pet = np.array(pet)
    aet = np.array(aet)
    averageSoilRootZone = np.array(averageSoilRootZone)
    averageSoilUpperZone = np.array(averageSoilUpperZone)
    snowPack = np.array(snowPack)
    precipitation = np.array(precipitation)
    
    # put data into a single dictionary
    water_data = {
            'date': dateObj,    
            'discharge': discharge,
            'subsurface flow': subsurfaceFlow,
            'impervious flow': imperviousFlow,
            'infiltration excess': infiltrationExcess,
            'initial abstracted flow': initialAbstractedFlow,
            'overland flow': overlandFlow,
            'pet': pet,
            'aet': aet,
            'average soil root zone': averageSoilRootZone,
            'average soil upper zone': averageSoilUpperZone,
            'snow pack': snowPack,
            'precipitation': precipitation
    }
    
    # Return WATER output variables
    return water_data

def print_water(water_data):
    """ 
    Print keys available from a WATER output file.
    
    *Parameters:*
        water_data : dictionary holding all data from a WATER file

    
    *Return:*
        no return

    """
    # print each key (parameter)
    for key in water_data.keys():
        print key


def main():  
    """
    Run module as script. Read, process, plot, and print information about an output 
    file created by the WATER application.    
        
    """
    # prompt user to get WATER output file
    fileFormat = [('Text file','*.txt')]

    # create a root object     
    root = Tkinter.Tk()
   
    # present a tkFileDialog module
    water_file = tkFileDialog.askopenfilename(title = 'Select WATER Output File', filetypes = fileFormat)

    # if user selects files and does not click "Cancel", then continue
    if water_file != '':    
    
        # process file    
        water_data = read_water(water_file)
            
        root.destroy()     
    
    else:
        root.destroy()

    # print available water parameters
    print '** The following are the parameters in the WATER output file **'
    print '' 
    for key in water_data:
        print key
    
    print '' 

    # ask user to select a water parameter
    parameter = raw_input('Which WATER output parameter would you like to print and plot: ')  

    print ''    
    print '**Printing**'
    print parameter
    print water_data[parameter]
    
    # plot parameter
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('WATER Output')
    ax.set_xlabel('date')
    ax.set_ylabel(parameter)
    ax.plot(water_data['date'], water_data[parameter], color = 'b', label = 'water ' + parameter)
    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles, labels)
    legend.draggable(state=True)
    plt.show()    

if __name__ == "__main__":
    
    # call main
    main()
