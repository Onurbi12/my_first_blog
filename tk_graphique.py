import sys
import Tkinter as tk
import time
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector


class MainWindow:
    def __init__(self, window):
        # Create a container
        self.window = window
        window.title("graphique")
        window.geometry("900x300+400+150")

        self.video_fig = Figure()
        self.mlp_canvas = FigureCanvasTkAgg(self.video_fig, master=window)
        self.mlp_canvas.get_tk_widget().grid(
            row=0, column=0, columnspan=4, padx=10, pady=5
        )

        self.zoom_fig = Figure()
        self.zoom_canvas = FigureCanvasTkAgg(self.zoom_fig, master=window)
        self.zoom_canvas.get_tk_widget().grid(
            row=0, column=400, columnspan=4, padx=10, pady=5
        )

        self.graphique()
        self.mlp_canvas.mpl_connect("key_press_event", self.span)

    def graphique(self):
        self.x = np.linspace(0, 50, 1000)
        self.y = np.cos(self.x)
        self.ax1 = self.video_fig.add_subplot(111)
        self.ax1.plot(self.x, self.y)
        self.ax2 = self.zoom_fig.add_subplot(111)
        (self.line2,) = self.ax2.plot(self.x, self.y)
        self.span = SpanSelector(
            self.ax1,
            self.onselect,
            "horizontal",
            useblit=True,
            rectprops=dict(alpha=0.5, facecolor="darkgreen"),
        )
        self.video_fig.canvas.draw()
    def onselect(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.x, (xmin, xmax))
        indmax = min(len(self.x) - 1, indmax)

        thisx = self.x[indmin:indmax]
        thisy = self.y[indmin:indmax]
        self.line2.set_data(thisx, thisy)
        self.ax2.set_xlim(thisx[0], thisx[-1])
        self.ax2.set_ylim(thisy.min(), thisy.max())

        self.zoom_fig.canvas.draw()


def main():
    #
    root = tk.Tk()
    mywindow = MainWindow(root)
    root.mainloop()


if (
    __name__ == "__main__"
):  # if we're running file directly and not importing it
    main()  # run the main function
