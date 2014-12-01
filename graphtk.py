import Tkinter as tk
from commonsgraph import commonsgraph
from datetime import datetime, timedelta
class GraphGui(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="white")
        self.pack(fill=tk.BOTH, expand=1)

        for x in xrange(1,4):
            self.columnconfigure(x, weight=1)
        for y in xrange(0,3):
            self.rowconfigure(y, weight=1)

        self.cg = commonsgraph()
        self.parent = parent
        self.curr_sys = None
        self.curr_subsys = None
        self.curr_col = None
        self.curr_idx = None
        self.series = []
        self.idxs = {}
        self.initUI()

    def sys_onclick(self, val):
        sender = val.widget
        value = sender.get(sender.curselection())
        self.curr_sys = value
        self.curr_subsys = None
        self.curr_col = None
        self.curr_idx = None

        subsize = self.subsyslist.size()
        self.subsyslist.delete(0, last=subsize-1)
        self.subsyslist.insert(tk.END, *self.cg.system_map[self.curr_sys])

        idxsize = self.idxlist.size()
        self.idxlist.delete(0, last=idxsize-1)

        colsize = self.colslist.size()
        self.colslist.delete(0, last=colsize-1)

    def subsys_onclick(self, val):
        sender = val.widget
        curr_subsys = sender.get(sender.curselection())
        idxlist = self.idxlist
        colslist = self.colslist

        self.curr_idx = None
        self.curr_col = None
        self.curr_subsys = curr_subsys
        service_dict = self.cg.ret_service_dict(self.curr_sys, curr_subsys)

        colsize = colslist.size()
        colslist.delete(0, last=colsize-1)
        self.cols = {y: x for x, y in service_dict['numeric']}
        colslist.insert(tk.END, *self.cols.iterkeys())

        idxsize = idxlist.size()
        idxlist.delete(0, last=idxsize-1)
        idxs = service_dict["indexes"]
        if idxs:
            self.idxs = {name: key for key, name in idxs}
            idxlist.insert(tk.END, *self.idxs.iterkeys())
        else:
            idxlist.insert(tk.END, "None")

    def cols_onclick(self, val):
        sender = val.widget
        item = sender.get(sender.curselection())
        self.curr_col = item

    def idx_onclick(self, val):
        sender = val.widget
        item = sender.get(sender.curselection())
        self.curr_idx = item

    def pass_graph(self):
        start_date = self.startdate.get()
        end_date = self.enddate.get()
        if self.series:
            self.cg.graph_one(start_date, end_date, self.series)
        else:
            raise ValueError('Need at least one thing to graph')

    def add_series(self):
        self.series.append([self.curr_sys,self.curr_subsys,self.cols[self.curr_col], self.idxs.get(self.curr_idx)])
        print self.series

    def clear_series(self):
        self.series = []

    def initUI(self):
        self.parent.title("Commons Graph App")
        #Graph Button
        graphbutton = tk.Button(self, text="Click here to generate graph.", command=self.pass_graph)
        graphbutton.grid(row=2, column=2, columnspan=2, sticky="nsew")
        #plus button
        plusbutton = tk.Button(self, text="+", command=self.add_series)
        plusbutton.grid(row=0, column=2, sticky="ew")
        #minus button
        minusbutton = tk.Button(self, text="-")
        minusbutton.grid(row=0, column=3, sticky="ew")
        #clear button
        clearbutton = tk.Button(self, text="Clear series", command=self.clear_series)
        clearbutton.grid(row=0, column=4, sticky="ew")
        #Start Date textbox
        startdate = tk.Entry(self)
        startdate.grid(row=2,column=1, sticky="ew")
        startdate.insert(0, (datetime.today()-timedelta(30)).isoformat())
        self.startdate = startdate
        #end date textbox
        enddate = tk.Entry(self)
        enddate.grid(row=2,column=4, sticky="ew")
        enddate.insert(0, datetime.today().isoformat())
        self.enddate = enddate
        #list of systems
        syslist = tk.Listbox(self)
        syslist.insert(tk.END, *self.cg.system_map.iterkeys())
        syslist.bind("<<ListboxSelect>>", self.sys_onclick)
        syslist.grid(row=1, column=1, sticky="nsew")
        self.syslist = syslist
        #list of subsystems
        subsyslist = tk.Listbox(self)
        subsyslist.bind("<<ListboxSelect>>", self.subsys_onclick)
        subsyslist.grid(row=1, column=2, sticky="nsew")
        self.subsyslist = subsyslist
        #list of columns
        colslist = tk.Listbox(self)
        colslist.bind("<<ListboxSelect>>", self.cols_onclick)
        colslist.grid(row=1, column=3, sticky="nsew")
        self.colslist = colslist
        #list of indexes
        idxlist = tk.Listbox(self)
        idxlist.bind("<<ListboxSelect>>", self.idx_onclick)
        idxlist.grid(row=1, column=4, sticky="nsew")
        self.idxlist = idxlist


def main():
    print "loading... please wait"
    root = tk.Tk()
    app = GraphGui(root)
    root.mainloop()


if __name__ == '__main__':
    main()
