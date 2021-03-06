import json

# TESTING WITH BOKEH:
####################
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, BoxAnnotation, Label, Legend, LegendItem, LabelSet
from bokeh.models.tools import HoverTool

import pandas as pd
import datetime as dt


def get_treatment_factors(some_element):
    treat = ""
    for j in range(len(some_element['factorValues'])):
        if j < len(some_element['factorValues']) - 1:
            if 'unit' in some_element['factorValues'][j]['factor'].keys():
                treat = treat + some_element['factorValues'][j]['factor']['name'].lower() + ": " \
                        + str(some_element['factorValues'][j]['value']) + ", " \
                        + str(some_element['factorValues'][j]['unit']) + ", "
            else:
                treat = treat + some_element['factorValues'][j]['factor']['name'].lower() + ": " \
                        + str(some_element['factorValues'][j]['value']) + ","
        else:
            if 'unit' in some_element['factorValues'][j]['factor'].keys():
                treat = treat + some_element['factorValues'][j]['factor']['name'].lower() + ": " \
                        + str(some_element['factorValues'][j]['value']) + ", " \
                        + str(some_element['factorValues'][j]['unit'])
            else:
                treat = treat + some_element['factorValues'][j]['factor']['name'].lower() + ": " \
                        + str(some_element['factorValues'][j]['value'])

    return treat

output_file('Bokeh-GanttChart.html')

try:
    # path = '/Users/Philippe/Documents/git/isa-api/tests/data/json/create/crossover-test.json'
    # path = '/Users/philippe/Documents/git/ISAdatasets/json/create/study-design-with-two-arms-multi-element-cells.json'
    path = '/Users/philippe/Documents/git/ISAdatasets/json/create/study-design-with-three-arms-single-element-cells.json'

    with open(path, 'r') as f:

        design = json.load(f)
        frames = []
        Items = []
        # element_colors = {
        #     "biological intervention": "rgb(255, 255, 0)",
        #     "chemical intervention": "rgb(255, 173, 47)",
        #     "washout": "rgb(192, 192, 192)",
        #     "screen": "rgb(64, 224,208)",
        #     "follow-up": "rgb(173, 216, 230)",
        #     "concomittant treatment": "rgb(107, 127, 135)"}

        # alternative color pallet
        element_colors = {"biological intervention": "rgb(253,232,37)",
                          "radiological intervention": "rgb(53, 155, 8)",
                          "dietary intervention": "rgb(53, 155, 8)",
                          "chemical intervention": "rgb(69, 13, 83)",
                          "washout": "rgb(45, 62, 120)",
                          "screen": "rgb(33, 144, 140)",
                          "run in": "rgb(43, 144, 180)",
                          "follow-up": "rgb(88, 189, 94)",
                          "concomitant treatment": "rgb(255, 255, 0)"}

        for key in design["studyArms"].keys():
            DF = pd.DataFrame(columns=['Arm', 'Cell', 'Type', 'Start_date', 'End_date', 'Treatment', 'Color'])
            arm_name = key
            # print("arm: ", arm_name)
            size = design["studyArms"][key]["groupSize"]
            size_annotation = "n=" + str(size)

            cells_per_arm = design["studyArms"][key]["cells"]
            cell_counter = 0
            for cell in cells_per_arm:
                cell_name = cell['name']
                elements_per_cell = cell['elements']

                for element in elements_per_cell:
                    treat = ""
                    element_counter = 0
                    # print(element['type'])

                    # for j in range(len(element['factorValues'])):
                    #     if j < len(element['factorValues'])-1:
                    #         if 'unit' in element['factorValues'][j]['factor'].keys():
                    #             treat = treat + element['factorValues'][j]['factor']['name'].lower() + ": " \
                    #                 + str(element['factorValues'][j]['value']) + ", " \
                    #                 + str(element['factorValues'][j]['unit']) + ", "
                    #         else:
                    #             treat = treat + element['factorValues'][j]['factor']['name'].lower() + ": " \
                    #                 + str(element['factorValues'][j]['value']) + ","
                    #     else:
                    #         if 'unit' in element['factorValues'][j]['factor'].keys():
                    #             treat = treat + element['factorValues'][j]['factor']['name'].lower() + ": " \
                    #                 + str(element['factorValues'][j]['value']) + ", " \
                    #                 + str(element['factorValues'][j]['unit'])
                    #         else:
                    #             treat = treat + element['factorValues'][j]['factor']['name'].lower() + ": " \
                    #                 + str(element['factorValues'][j]['value'])
                    if 'concomitantTreatments' in element.keys():
                        element_counter = element_counter + 1
                        treatments = []
                        for item in element['concomitantTreatments']:
                            print("ITEM:", item)
                            treatment = get_treatment_factors(item)

                            treatments.append(treatment)
                        print("Treatments:", treatments)
                        concomitant = ','.join(treatments[0:-1])
                        concomitant = concomitant + ' and ' + treatments[-1]
                        array = [arm_name, cell_name, arm_name + ": [" + concomitant + "]_concomitant_" + str(cell_counter),
                             dt.datetime(cell_counter + 1970, 1, 1), dt.datetime(cell_counter + 1970 + 1, 1, 1),
                             # str(element['factorValues']),
                             concomitant,
                             element_colors["concomitant treatment"]]
                        Items.append(array)

                    elif 'type' in element.keys():

                        treatments = get_treatment_factors(element)
                        element_counter = element_counter + 1
                        array = [arm_name, cell_name, arm_name + ": [" + str(element['type']) + "]_" + str(cell_counter),
                                 dt.datetime((cell_counter + 1970), 1, 1), dt.datetime((cell_counter + 1970 + 1), 1, 1),
                                 # str(element['factorValues']),
                                 str(treat),
                                 element_colors[element['type']]]
                        Items.append(array)

                    cell_counter = cell_counter + 1

        for i, Dat in enumerate(Items):
            DF.loc[i] = Dat
            print("setting:", DF.loc[i])

        # providing the canvas for the figure
        print("THESE ARE THE TYPES_: ", DF.Type.tolist())
        fig = figure(title='Study Design Treatment Plan',
                     width=800,
                     height=400,
                     y_range=DF.Type.tolist(),
                     x_range=Range1d(DF.Start_date.min(), DF.End_date.max()),
                     tools='save')

        # adding a tool tip
        hover = HoverTool(tooltips="Task: @Type<br>\
        Start: @Start_date<br>\
        Cell_Name: @Cell<br>\
        Treatment: @Treatment")
        fig.add_tools(hover)

        DF['ID'] = DF.index+0.8
        # print("ID: ", DF['ID'])
        DF['ID1'] = DF.index+1.2
        # print("ID1: ", DF['ID1'])
        CDS = ColumnDataSource(DF)
        # , legend=str(size_annotation)
        r = fig.quad(left='Start_date', right='End_date', bottom='ID', top='ID1', source=CDS, color="Color")
        fig.xaxis.axis_label = 'Time'
        fig.yaxis.axis_label = 'study arms'
        # fig.legend.location = 'bottom_right'

        # working at providing a background color change for every arm in the study design
        counts = DF['Arm'].value_counts().tolist()
        print("total number of study arms:", len(counts), "| number of phases per arm:", counts)
        # box = []
        # for i, this_element in enumerate(DF['Arm']):
        #     if i==0:
        #         box[i] = BoxAnnotation(bottom=0,
        #                              top=DF['Arm'].value_counts().tolist()[0],
        #                              fill_color="blue")
        #     elif i % 2 == 0:
        #         box[i] = BoxAnnotation(bottom=DF['Arm'].value_counts().tolist()[0],
        #                              top=DF['Arm'].value_counts().tolist()[0],
        #                              fill_color="silver")
        #     else:
        #         box[i] = BoxAnnotation(bottom=DF['Arm'].value_counts().tolist()[0],
        #                              top=DF['Arm'].value_counts().tolist()[0] + DF['Arm'].value_counts().tolist()[1],
        #                              fill_color="grey",
        #                              fill_alpha=0.1)
        # # adding the background color for each arm:
        # for element in box:
        #     fig.add_layout(element)
        # # fig.add_layout(box2)
        # # fig.add_layout(legend,'right')

        caption1 = Legend(items=[(str(size_annotation), [r])])
        fig.add_layout(caption1, 'right')
        # caption2 = Legend(items=[(str(size_annotation), [r])])
        # fig.add_layout(caption2, 'below')

        # labels = LabelSet(x='ID', y='ID1', text='Type', level='glyph',
        #                   x_offset=5, y_offset=5, source=CDS, render_mode='canvas')

        citation = Label(x=10, y=-80, x_units='screen', y_units='screen',
                         text='crossover design layout - isa-api 10.5', render_mode='css',
                         border_line_color='gray', border_line_alpha=0.4,
                         background_fill_color='white', background_fill_alpha=1.0)

        # fig.add_layout(labels)
        fig.add_layout(citation)

        show(fig)

except IOError as e:
    print("problem reading the file:", e)
