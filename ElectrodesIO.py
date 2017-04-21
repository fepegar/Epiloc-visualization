import csv
import xml.etree.ElementTree as ET

import numpy as np

from Electrode import Electrode
from EpilepsyPlot import EpilepsyPlot

class ElectrodesReader:

    def getElectrodesFromXML(self, xmlPath):
        electrodes = []
        tree = ET.parse(xmlPath)
        root = tree.getroot()
        for electrodeNode in root:
            name = electrodeNode.get('procedure')
            color = electrodeNode.find('Color').get('rgb')
            plotsNode = electrodeNode.find('Plots')
            plots = []
            for plotNode in plotsNode:
                plotNumber = plotNode.get('number')
                center = np.array([float(plotNode.get(coord)) for coord in ['x', 'y', 'z']])
                plots.append(EpilepsyPlot(center=center, number=plotNumber))
            electrodes.append(Electrode(name, colorString=color, plots=plots))
        return electrodes


    def getElectrodesFromLocalizationsCSV(self, csvPath):
        electrodes = []
        with open(csvPath) as f:
            lines = f.readlines()
            for line in lines:
                row = line.split(';')
                if len(row) == 1:
                    if row[0].strip() and row[0] != 'Procedure':
                        name = row[0].rstrip('\r\n')
                        plots = []
                        electrode = Electrode(name, plots=plots)
                        electrodes.append(electrode)
                else:
                    if row[1].strip() and row[1] != 'Plot number':
                        plotNumber = int(row[1])
                        plot = EpilepsyPlot(number=plotNumber)
                        talairachLabels = [label.rstrip('\r\n') for label in row[27:32]]
                        plot.talairachLabels = talairachLabels
                        electrode.plots.append(plot)
                        mniCenter = np.array([float(n) for n in row[3:6]])
                        plot.mniCenter = mniCenter
        return electrodes


    def getTalairachLabelFromCSV(self, name, plotNumber, csvPath):
        electrodes = self.getElectrodesFromLocalizationsCSV(csvPath)
        for electrode in electrodes:
            if electrode.name == name:
                for plot in electrode.plots:
                    if plot.number == plotNumber:
                        return plot.talairachLabels


if __name__ == '__main__':
    reader = ElectrodesReader()
    p = '/home/fernando/epiloc2015/patients/pat_02033_0465/pat_02033_0465_anatomical_localizations.csv'
    labels = reader.getTalairachLabelFromCSV('TPa', 4, p)
