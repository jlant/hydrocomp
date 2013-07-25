# -*- coding: utf-8 -*-
"""
:Module: hydrocomp.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: Compare timeseries output from a model (i.e. discharge, gage height,
sediment concentration, etc.) with an observed timeseries (i.e. USGS NWIS)
Statistics such as Nash-Sutcliffe, percent errors, relative errors, etc. are
computed and plotted.

main() prompts user for observed and model files. Processes each file, prints 
information, and plots data and statistics. Information is printed to the screen.  
Plots are saved to a directory called 'figs' which is created in the same directory 
as the data file. A log file called 'nwis_error.log' is created if any errors are 
found in the data file.
"""

#!/usr/bin/env python
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import Tkinter, tkFileDialog
import logging

# my modules
import nwispy
import water
import statistics
import helpers


def compare(parameter_name, model_name, observed_name, modeled_parameter, observed_parameter, dates):
    """    
    Collect information about and compute comparision statistics between param1 and param2
            
    *Parameters:*
        parameter_name : string of the parameter being compared
        
        model_name : string of the model name
        
        observed_name : string of the observed name
        
        modeled_parameter : array of data; i.e. discharge, stage, sediment concentration, etc.
        
        observed_parameter : array of data; i.e. discharge, stage, sediment concentration, etc.
        
        dates :  array of datetime objects
    
    *Return:*
        comp_data : dictionary holding information, data, and statistics
        
        comp_data = {
            'parameter_name': parameter_name,
            
            'modeled_name': modeled_name,
            
            'observed_name': observed_name,
            
            'modeled_parameter': modeled_parameter,
            
            'observed_parameter': observed_parameter,
            
            'dates': dates,
            
            'timestep': timestep,
            
            'stats': stats
        }        
        
        stats = {
            'relative_error': relative_error_array,
            
            'percent_error': percent_error_array,
            
            'percent_difference': percent_difference_error_array,
            
            'mean_squared_error': mean_squared_error,
            
            'r_squared_coeff': r_squared_coeff,
            
            'nash_sutcliffe_coeff': nash_sutcliffe_coeff
        }

    """
    if len(modeled_parameter) != len(observed_parameter):
        raise ValueError("Lengths of modeled and observed are not equal!")
    
    else:
        # create a dictionary to hold data, information, and stats
        comp_data = {
            'parameter_name': parameter_name,
            'model_name': model_name,
            'observed_name': observed_name,
            'modeled_parameter': modeled_parameter,
            'observed_parameter': observed_parameter,
            'dates': dates,
            'timestep': dates[1] - dates[0],
            'stats': None
        }   
        
        # create a dictionary to hold stats
        stats = {
            'relative_error': None,
            'percent_error': None,
            'percent_difference': None,
            'r_squared_coeff': None,
            'nash_sutcliffe_coeff': None
        }    
        
        # compute stats on data
        stats['relative_error'] = statistics.relative_error(x = modeled_parameter, x_true = observed_parameter)
        stats['percent_error'] = statistics.percent_error(x = modeled_parameter, x_true = observed_parameter)
        stats['percent_difference'] = statistics.percent_difference(x = modeled_parameter, x_true = observed_parameter)
        stats['mean_squared_error'] = statistics.mean_squared_error(x = modeled_parameter, x_true = observed_parameter)

        stats['r_squared_coeff'] = statistics.r_squared(modeled = modeled_parameter, observed = observed_parameter)
        stats['nash_sutcliffe_coeff'] = statistics.nash_sutcliffe(modeled = modeled_parameter, observed = observed_parameter)
    
        comp_data['stats'] = stats
    
        return comp_data

def print_comp_data(comp_data):
    """    
    Print relevant information about the parameter being compared and the 
    comparision statistics 
    
    *Parameters:*
        comp_data : dictionary holding information, data, and statistics
        
    *Return:*
        no return 
    """   
    
    # print information and statistics
    print 'Parameter Name: ', comp_data['parameter_name']
    print 'Model Name: ', comp_data['model_name']
    print 'Observed Name: ', comp_data['observed_name']
    print 'Timestep: ', comp_data['timestep']    
    
    print 'Mean Squared Error: %.2f' % comp_data['stats']['mean_squared_error']
    print 'R-Squared: %.2f' % comp_data['stats']['r_squared_coeff']
    print 'Nash-Sutcliffe: %.2f' % comp_data['stats']['nash_sutcliffe_coeff']
        
def plot_comp_data(comp_data, is_visible = True, save_path = None):
    """   
    Plot information about the parameter being compared and the comparision statistics 
    
    *Parameters:*
        comp_data : dictionary holding information, data, and statistics
        
    *Return:*
        no returns
    """ 
    # plot parameter
    fig = plt.figure(figsize=(12,10))

    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title(comp_data['model_name'] + ' vs. ' + comp_data['observed_name'] + ' (' + comp_data['timestep'].__str__() +')')
    ax.set_xlabel('date')
    ax.set_ylabel(comp_data['parameter_name'])

    plt.plot(comp_data['dates'], comp_data['observed_parameter'], color = 'b', marker = 'o', label = comp_data['observed_name'])
    plt.plot(comp_data['dates'], comp_data['modeled_parameter'], color = 'g', marker = 'o', label = comp_data['model_name'])
    
    # rotate and align the tick labels so they look better   
    plt.setp(ax.xaxis.get_majorticklabels(), rotation = 30)
    
    # use a more precise date string for the x axis locations in the toolbar
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
     
    # legend; make it transparent    
    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles, labels, fancybox = True)
    legend.get_frame().set_alpha(0.5)
    legend.draggable(state=True)
    
    # show text on graph; use matplotlib.patch.Patch properies and bbox
    text = 'R_squared = %.2f\nNash-Sutcliffe = %.2f' % (comp_data['stats']['r_squared_coeff'], comp_data['stats']['nash_sutcliffe_coeff'])
    patch_properties = {'boxstyle': 'round',
                        'facecolor': 'wheat',
                        'alpha': 0.5
                        }
                   
    ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14, 
            verticalalignment = 'top', horizontalalignment = 'left', bbox = patch_properties)

    # save plots
    if save_path:        
        # set the size of the figure to be saved
        curr_fig = plt.gcf()
        curr_fig.set_size_inches(12, 10)
        plt.savefig(save_path + '/' + comp_data['model_name'] + ' vs. ' + comp_data['observed_name'] + '.png', dpi = 100)
        
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()

    # plot each statistic
    includes = ['relative_error', 'percent_error', 'percent_difference']
    for key, values in comp_data['stats'].iteritems():
        if key in includes:
            # plot stat
            fig = plt.figure(figsize=(12,10))
        
            ax = fig.add_subplot(111)
            ax.grid(True)
            ax.set_title(comp_data['model_name'] + ' vs. ' + comp_data['observed_name'] + ' (' + comp_data['timestep'].__str__() +')')
            ax.set_xlabel('date')
            ax.set_ylabel(key.replace('_'," "))
        
            plt.plot(comp_data['dates'], np.zeros(len(comp_data['dates'])), color = 'k', linestyle = '--', label = 'reference line')
            plt.plot(comp_data['dates'], values, color = 'r', label = key.replace('_'," "))
            
            # rotate and align the tick labels so they look better   
            plt.setp(ax.xaxis.get_majorticklabels(), rotation = 30)
            
            # use a more precise date string for the x axis locations in the
            # toolbar
            ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
             
            # legend; make it transparent    
            handles, labels = ax.get_legend_handles_labels()
            legend = ax.legend(handles, labels, fancybox = True)
            legend.get_frame().set_alpha(0.5)
            legend.draggable(state=True)
            
            # show text on graph; use matplotlib.patch.Patch properies and bbox
            text = 'Mean = %.2f\nMax = %.2f\nMin = %.2f' % (np.mean(values), np.max(values), np.min(values))
            patch_properties = {'boxstyle': 'round',
                                'facecolor': 'wheat',
                                'alpha': 0.5
                                }
                           
            ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14, 
                    verticalalignment = 'top', horizontalalignment = 'left', bbox = patch_properties)
        
            # save plots
            if save_path:        
                # set the size of the figure to be saved
                curr_fig = plt.gcf()
                curr_fig.set_size_inches(12, 10)
                plt.savefig(save_path + '/' + key + '.png', dpi = 100)
                
            # show plots
            if is_visible:
                plt.show()
            else:
                plt.close()
        else:
            pass
    
        
def main():
    """
    Run as script. Prompt user for observed and model file. Process each file, print information, 
    and plot data. Information is printed to the screen.  Plots are saved to a directory 
    called 'figs' which is created in the same directory as the data file. A
    log file called 'nwis_error.log' is created if any errors are found in the 
    data file.
    """ 
    
    # get user input about which parameter to compare
    print ''
    print '** User Input **'
    observed_name = raw_input('What is a descriptive name for the *OBSERVED* data? ')
            
    # get observed file    
    root = Tkinter.Tk() 
    file_format = [('Text file','*.txt')]  
    nwis_file = tkFileDialog.askopenfilename(title = 'Select *OBSERVED* File', filetypes = file_format)
    root.destroy()
    
    # get user input about which parameter to compare
    print ''
    print '** User Input **'
    model_name = raw_input('What is a descriptive name for the *MODEL* data file? ')
            
    # get modeled file    
    root = Tkinter.Tk() 
    file_format = [('Text file','*.txt')]  
    water_file = tkFileDialog.askopenfilename(title = 'Select *MODEL* output File', filetypes = file_format)
    root.destroy()
    
    if nwis_file and water_file:
        
        try:
            # get directory and filename from data file
            dirname, filename = os.path.split(os.path.abspath(nwis_file))
            
            # make a directory called figs to hold the plots            
            figs_path = dirname + '/figs'
            if not os.path.exists(figs_path):
                os.makedirs(figs_path)            
            
            # log any errors or warnings found in file; save to data file directory
            logging.basicConfig(filename = dirname + '/nwis_error.log', filemode = 'w', level=logging.DEBUG)
            
            # process observed file  
            print ''
            print '** Processing Observed Data **'
            print nwis_file
            nwis_data = nwispy.read_nwis(nwis_file)
            
            # print observed information
            print ''
            print '** Observed File Information **'
            nwispy.print_nwis(nwis_data = nwis_data)
            
            # process modeled file
            print ''
            print '** Processing Modeled Data **'
            print water_file
            water_data = water.read_water(water_file)
            
            # print modeled information
            print ''
            print '** Modeled File Information **'
            water.print_water(water_data = water_data)
            
            # get user input about which parameter to compare
            print ''
            print '** User Input **'
            user_parameter = raw_input('What common parameter would you like to compare? ')            
            
            # print the parameter being compared
            print ''
            print '** Parameter Being Compared **'
            print user_parameter            
            
            # get parameter from observed file        
            for parameter in nwis_data['parameters']:
                if user_parameter in parameter['description'].lower():
                    nwis_parameter = parameter['data']                
                else:
                    print user_parameter + ' parameter does not exist in observed file'            
            
            # get parameter from modeled file
            if user_parameter in water_data.keys():
                water_parameter = water_data[user_parameter]
            else:
                print user_parameter + ' parameter does not exist in model file'  
            
            # subset modeled data and the observed data by finding common date range
            # find common start date and end date between the data sets
            start_date, end_date = helpers.find_start_end_dates(model_dates = water_data['date'], observed_dates = nwis_data['dates'])
            
            # subset the water data to match the range of the nwis data
            subset_kwargs = {
                'dates': water_data['date'],
                'data': water_parameter,
                'start_date': start_date,
                'end_date': end_date
                }
                
            water_data_subset = helpers.subset_data(**subset_kwargs)    
            
            # subset the water data to match the range of the nwis data
            subset_kwargs = {
                'dates': nwis_data['dates'],
                'data': nwis_parameter,
                'start_date': start_date,
                'end_date': end_date
                }
                
            nwis_data_subset = helpers.subset_data(**subset_kwargs) 

            # compare parameters and compute stats           
            compare_kwargs = {
                'parameter_name': user_parameter,
                'model_name': model_name,
                'observed_name': observed_name,
                'modeled_parameter': water_data_subset['data'],
                'observed_parameter': nwis_data_subset['data'],
                'dates': nwis_data_subset['dates']
                }
              
            comp_data = compare(**compare_kwargs)

            # print results
            print_comp_data(comp_data = comp_data)

            # plot results
            print ''
            print '** Plotting **'
            print 'Plots are being saved to same directory as NWIS data file.'
            plot_comp_data(comp_data, is_visible = True, save_path = figs_path)
            
            # shutdown the logging system
            logging.shutdown()            
            
        except IOError as error:
            print 'cannot read file' + error.filename
            print error.message

        except IndexError as error:
            print 'Cannot read file! Bad file!'
            print error.message
        
        except ValueError as error:
            print error.message
            
    else:
        print '** Canceled **'

if __name__ == "__main__":
    
    # read files, print results, and plot 
    main() 