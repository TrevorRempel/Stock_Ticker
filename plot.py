import pandas as pd 
from bokeh.plotting import figure
from bokeh.palettes import Spectral4


def produce_plot(data):
    
    figs = []
    TOOLS = "crosshair,box_zoom,reset,box_select,save"
    
    #Only loop over the variables that are not 
    for ticker, df in data.iteritems(): 
        num_lines = df.shape[1]
        colors = Spectral4[0:num_lines]
        p = figure(title = "{}".format(ticker), x_axis_label = None, y_axis_label = "Price (USD)",\
                 x_axis_type = "datetime", tools = TOOLS, width = 800, height = 400)

        for i, name in enumerate(df.columns):
            p.line(df.index, df[name], color = colors[i], legend = name, line_width = 2, line_alpha = 0.85)
            
        p.background_fill_color = 'darkslateblue'
        p.background_fill_alpha = 0.15
        
        p.legend.background_fill_color = 'darkslateblue'
        p.legend.background_fill_alpha = 0.001
        p.legend.border_line_width = 0.1
        p.legend.border_line_color = "darkslateblue"
        p.legend.border_line_alpha = 0.001
        p.legend.location = "top_left"
        
        p.xgrid.grid_line_width = 2
        p.ygrid.grid_line_width = 2
        p.xgrid.grid_line_color = 'white'
        p.ygrid.grid_line_color = 'white'
        figs.append(p)
    return figs