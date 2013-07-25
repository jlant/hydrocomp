# -*- coding: utf-8 -*-
"""
:Module: hydrocompgui.py

:Author: Jeremiah Lant
 
:Email: jlant@usgs.gov

:Purpose: 
Compare timeseries output from a model (i.e. discharge, gage height,
sediment concentration, etc.) with an observed timeseries (i.e. USGS NWIS)
Statistics such as Nash-Sutcliffe, percent errors, relative errors, etc. are
computed and plotted. main() prompts user for observed and model files. Processes 
each file, prints information, and plots data and statistics. Information is 
printed to the screen. An interactive plot of the observed and modeled data 
comparison is created alongwith a plot of the relative error. User can interact 
with the plots via a SpanSelector mouse widget. A toggle key event handler exists 
for the matplotlib SpanSelector widget. A keypress of 'A' or 'a' actives the 
slider and a keypress of 'Q' or 'q' de-activates the slider.

"""

#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import Tkinter, tkFileDialog
import matplotlib.dates as mdates
import datetime

# my modules
import hydrocomp
import nwispy
import water
import statistics
import helpers

def onselect(xmin, xmax):
    """ 
    A select event handler for the matplotlib SpanSelector widget.
    Selects a min/max range of the x or y axes for a matplotlib Axes.
    """ 
    # convert matplotlib float dates to a datetime format
    date_min = mdates.num2date(xmin)
    date_max = mdates.num2date(xmax) 
    
    # put the xmin and xmax in datetime format to compare
    date_min = datetime.datetime(date_min.year, date_min.month, date_min.day, date_min.hour, date_min.minute)    
    date_max = datetime.datetime(date_max.year, date_max.month, date_max.day, date_max.hour, date_max.minute)
    
    # find the indices that were selected    
    indices = np.where((comp_data['dates'] >= date_min) & (comp_data['dates'] <= date_max))
    indices = indices[0]
    
    # set the data in ax2 plot
    plot2a.set_data(comp_data['dates'][indices], comp_data['observed_parameter'][indices])
    plot2b.set_data(comp_data['dates'][indices], comp_data['modeled_parameter'][indices])
        
    # calculate updated stats 
    updated_r_squared_coeff = statistics.r_squared(modeled = comp_data['modeled_parameter'][indices], observed = comp_data['observed_parameter'][indices])
    updated_nash_sutcliffe_coeff = statistics.nash_sutcliffe(modeled = comp_data['modeled_parameter'][indices], observed = comp_data['observed_parameter'][indices])
    
    ax2.set_xlim(comp_data['dates'][indices][0], comp_data['dates'][indices][-1])
    param_max = np.max((comp_data['observed_parameter'][indices], comp_data['modeled_parameter'][indices]))
    param_min = np.min((comp_data['observed_parameter'][indices], comp_data['modeled_parameter'][indices]))
    ax2.set_ylim(param_min, param_max)
    
    # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
    text2 = 'R_squared = %.2f\nNash sutcliffe = %.2f' % (updated_r_squared_coeff, updated_nash_sutcliffe_coeff)
                   
    ax2_text.set_text(text2)
    
    # set the data in ax4 plot
    plot4a.set_data(comp_data['dates'][indices], comp_data['stats']['relative_error'][indices])
    plot4b.set_data(comp_data['dates'][indices], comp_data['stats']['relative_error'][indices])
    
    # calculate updated mean, max, min for stats data
    stat_mean = np.mean(comp_data['stats']['relative_error'][indices])
    stat_max = np.max(comp_data['stats']['relative_error'][indices])
    stat_min = np.min(comp_data['stats']['relative_error'][indices])
    
    ax4.set_xlim(comp_data['dates'][indices][0], comp_data['dates'][indices][-1])
    ax4.set_ylim(stat_min, stat_max)
    
    # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
    text4 = 'Mean = %.2f\nMax = %.2f\nMin = %.2f' % (stat_mean, stat_max, stat_min)
                   
    ax4_text.set_text(text4)    
    
    fig.canvas.draw()

def toggle_selector(event):
    """ 
    A toggle key event handler for the matplotlib SpanSelector widget.
    A or a actives the slider; Q or q de-activates the slider.
    """ 
    if event.key in ['Q', 'q'] and span.visible:
        print '**SpanSelector deactivated.**'
        span.visible = False
    if event.key in ['A', 'a'] and not span.visible:
        print '**SpanSelector activated.**'
        span.visible = True

    
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
          
        comp_data = hydrocomp.compare(**compare_kwargs)

        # print results
        hydrocomp.print_comp_data(comp_data = comp_data)

        
        # plot 
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows = 2, ncols= 2, figsize = (20, 12))

        # ax1 plot
        ax1.grid(True)
        
        ax1.set_title(comp_data['model_name'] + ' vs. ' + comp_data['observed_name'] + ' (' + comp_data['timestep'].__str__() +')')
        ax1.set_xlabel('date')
        ax1.set_ylabel(comp_data['parameter_name'])
    
        plot1a, = ax1.plot(comp_data['dates'], comp_data['observed_parameter'], color = 'b', marker = 'o', label = comp_data['observed_name'])
        plot1b, = ax1.plot(comp_data['dates'], comp_data['modeled_parameter'], color = 'g', marker = 'o', label = comp_data['model_name'])
        
        # rotate and align the tick labels so they look better   
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation = 30)
        
        # use a more precise date string for the x axis locations in the
        # toolbar
        ax1.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
         
        # legend; make it transparent    
        handles, labels = ax1.get_legend_handles_labels()
        legend = ax1.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)
        
        # show text on graph; use matplotlib.patch.Patch properies and bbox
        text1 = 'R_squared = %.2f\nNash-Sutcliffe = %.2f' % (comp_data['stats']['r_squared_coeff'], comp_data['stats']['nash_sutcliffe_coeff'])
        patch_properties = {'boxstyle': 'round',
                            'facecolor': 'wheat',
                            'alpha': 0.5
                            }
                       
        ax1.text(0.05, 0.95, text1, transform = ax1.transAxes, fontsize = 14, 
                verticalalignment = 'top', horizontalalignment = 'left', bbox = patch_properties)
        
        # ax2 plot
        ax2.grid(True)
        ax2.set_title(comp_data['model_name'] + ' vs. ' + comp_data['observed_name'] + ' (' + comp_data['timestep'].__str__() +')')
        ax2.set_xlabel('date')
        ax2.set_ylabel(comp_data['parameter_name'])
    
        plot2a, = ax2.plot(comp_data['dates'], comp_data['observed_parameter'], color = 'b', marker = 'o', label = comp_data['observed_name'])
        plot2b, = ax2.plot(comp_data['dates'], comp_data['modeled_parameter'], color = 'g', marker = 'o', label = comp_data['model_name'])
        
        # rotate and align the tick labels so they look better 
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation = 30)
        
        # use a more precise date string for the x axis locations in the
        # toolbar
        ax2.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
         
        # legend; make it transparent    
        handles, labels = ax2.get_legend_handles_labels()
        legend = ax2.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)
        
        # show text on graph; use matplotlib.patch.Patch properies and bbox
        text2 = 'R_squared = %.2f\nNash-Sutcliffe = %.2f' % (comp_data['stats']['r_squared_coeff'], comp_data['stats']['nash_sutcliffe_coeff'])
        patch_properties = {'boxstyle': 'round',
                            'facecolor': 'wheat',
                            'alpha': 0.5
                            }
                       
        ax2_text = ax2.text(0.05, 0.95, text2, transform = ax2.transAxes, fontsize = 14, 
                            verticalalignment = 'top', horizontalalignment = 'left', bbox = patch_properties)
        
        
        # plot the stats in ax3 and ax4       
        ax3.grid(True)
        ax3.set_title(comp_data['model_name'] + ' vs. ' + comp_data['observed_name'] + ' (' + comp_data['timestep'].__str__() +')')
        ax3.set_xlabel('date')
        ax3.set_ylabel('relative error')
    
        plot3a, = ax3.plot(comp_data['dates'], np.zeros(len(comp_data['dates'])), color = 'k', linestyle = '--', label = 'reference line')
        plot3b, = ax3.plot(comp_data['dates'], comp_data['stats']['relative_error'], color = 'r', label = 'relative error')
        
        # rotate and align the tick labels so they look better 
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation = 30)
        
        # use a more precise date string for the x axis locations in the
        # toolbar
        ax3.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
         
        # legend; make it transparent    
        handles, labels = ax3.get_legend_handles_labels()
        legend = ax3.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)
        
        # show text on graph; use matplotlib.patch.Patch properies and bbox
        text3 = 'Mean = %.2f\nMax = %.2f\nMin = %.2f' % (np.mean(comp_data['stats']['relative_error']), np.max(comp_data['stats']['relative_error']), np.min(comp_data['stats']['relative_error']))
        patch_properties = {'boxstyle': 'round',
                            'facecolor': 'wheat',
                            'alpha': 0.5
                            }
                       
        ax3_text = ax3.text(0.05, 0.95, text3, transform = ax3.transAxes, fontsize = 14, 
                            verticalalignment = 'top', horizontalalignment = 'left', bbox = patch_properties)
        
        # ax4 plot
        ax4.grid(True)
        ax4.set_title(comp_data['model_name'] + ' vs. ' + comp_data['observed_name'] + ' (' + comp_data['timestep'].__str__() +')')
        ax4.set_xlabel('date')
        ax4.set_ylabel('relative error')
    
        plot4a, = ax4.plot(comp_data['dates'], np.zeros(len(comp_data['dates'])), color = 'k', linestyle = '--', label = 'reference line')
        plot4b, = ax4.plot(comp_data['dates'], comp_data['stats']['relative_error'], color = 'r', label = 'relative error')
        
        # rotate and align the tick labels so they look better 
        plt.setp(ax4.xaxis.get_majorticklabels(), rotation = 30)
        
        # use a more precise date string for the x axis locations in the
        # toolbar
        ax4.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
         
        # legend; make it transparent    
        handles, labels = ax4.get_legend_handles_labels()
        legend = ax4.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)
        
        # show text on graph; use matplotlib.patch.Patch properies and bbox
        text4 = 'Mean = %.2f\nMax = %.2f\nMin = %.2f' % (np.mean(comp_data['stats']['relative_error']), np.max(comp_data['stats']['relative_error']), np.min(comp_data['stats']['relative_error']))
        patch_properties = {'boxstyle': 'round',
                            'facecolor': 'wheat',
                            'alpha': 0.5
                            }
                       
        ax4_text = ax4.text(0.05, 0.95, text4, transform = ax4.transAxes, fontsize = 14, 
                            verticalalignment = 'top', horizontalalignment = 'left', bbox = patch_properties)        
        
        
        # make a splan selector and have it turned off initially until user 
        # presses 'q' or 'a' on the key board via toggle_selector
        span = SpanSelector(ax1, onselect, 'horizontal', useblit=True,
                            rectprops=dict(alpha=0.5, facecolor='red'))
        span.visible = False
                
        # connect span with the toggle selector in order to toggle span selector on and off
        span.connect_event('key_press_event', toggle_selector)        
        
        # make sure that the layout of the subplots do not overlap
        plt.tight_layout()
        plt.show()
                
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
 