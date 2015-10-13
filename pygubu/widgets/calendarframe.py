# encoding: utf8
from __future__ import unicode_literals

import calendar
try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk


def get_calendar(locale, fwday):
    # instantiate proper calendar class
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)


class CalendarFrame(ttk.Frame):
    """ Allows to choose a file or directory.
    
    Generates:
        <<CalendarDaySelected>>
        <<CalendarMonthChanged>>
        <<CalendarYearChanged>>
    
    """

    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        
        self.__cb = None
        self._cal = get_calendar(None, calendar.MONDAY)
        
        
        # BUILD UI
        # mainframe widget
        mainframe = self
        mainframe.configure(width='200', height='200', padding='2')
        # frame2 widget
        frame2 = ttk.Frame(mainframe)
        frame2.configure(width='200', height='200')
        # bprevm widget
        bprevm = ttk.Button(frame2)
        bprevm.configure(style='Toolbutton', width='2', text='L')
        bprevm.grid(column='0', row='0')
        bprevm.propagate(True)
        # lmonth widget
        lmonth = ttk.Label(frame2)
        lmonth.configure(anchor='center', text='Enero')
        lmonth.grid(ipadx='5', row='0', column='1', sticky='ew')
        lmonth.propagate(True)
        # bnmonth widget
        bnmonth = ttk.Button(frame2)
        bnmonth.configure(style='Toolbutton', width='2', text='R')
        bnmonth.grid(column='2', row='0')
        bnmonth.propagate(True)
        # bpyear widget
        bpyear = ttk.Button(frame2)
        bpyear.configure(style='Toolbutton', width='2', text='L')
        bpyear.grid(padx='5', column='4', row='0')
        bpyear.propagate(True)
        # lyear widget
        lyear = ttk.Label(frame2)
        lyear.configure(anchor='center', text='2015')
        lyear.grid(ipadx='5', row='0', column='5', sticky='ew')
        lyear.propagate(True)
        # bnyear widget
        bnyear = ttk.Button(frame2)
        bnyear.configure(style='Toolbutton', width='2', text='R')
        bnyear.grid(column='6', row='0')
        bnyear.propagate(True)
        frame2.grid(row='0', column='0', sticky='ew')
        frame2.propagate(True)
        frame2.columnconfigure(3, minsize='20', weight='1')
        # canvas widget
        canvas = tk.Canvas(mainframe)
        canvas.configure(highlightthickness='0', borderwidth='0', background='#ffffff', height='180')
        canvas.configure(width='260')
        canvas.grid(row='1', column='0', sticky='nsew')
        canvas.propagate(True)
        mainframe.grid(row='0', column='0', sticky='nsew')
        mainframe.propagate(True)
        mainframe.rowconfigure(1, weight='1')
        mainframe.rowconfigure(0, weight='0')
        mainframe.columnconfigure(0, weight='1')
        
        canvas.bind('<Configure>', self._on_canvas_configure)
        self._canvas = canvas
        self._draw_canvas(canvas)
        
    def _draw_canvas(self, canvas):
        ch = canvas.winfo_reqheight()
        cw = canvas.winfo_reqwidth()
        rowh = ch / 7.0
        colw = cw / 7.0
        # Header
        self._rheader = canvas.create_rectangle(0, 0, cw, rowh, width=0, fill='grey90')
        self._theader = [ 0 for x in range(0, 7)]
        ox = 0
        oy = rowh / 2.0
        coffset = colw / 2.0
        cols = self._cal.formatweekheader(3).split()
        for i in range(0, 7):
            x = ox + i * colw + coffset
            self._theader[i] = canvas.create_text(x, oy, text=cols[i])
        
        # background matrix
        self._recmat = rm = [ [0 for c in range(0, 7)] for x in range(0, 6)]
        oy = rowh
        ox = 0
        for f in range(0, 6):
            for c in range(0, 7):
                x = ox + c * colw
                y = oy + f * rowh
                x1 = x + colw - 1
                y1 = y + rowh - 1
                rec = canvas.create_rectangle(x, y, x1, y1, width=1,
                                              fill='white', outline='white',
                                              activeoutline='blue',
                                              activewidth=1)
                self._recmat[f][c] = rec
        
        # text matrix
        self._txtmat = tm = [ [0 for c in range(0, 7)] for x in range(0, 6)]
        weeks = self._cal.monthdayscalendar(2016, 10)
        xoffset = colw / 2.0
        yoffset = rowh / 2.0
        oy = rowh
        ox = 0
        for f in range(0, 6):
            for c in range(0, 7):
                x = ox + c * colw + coffset
                y = oy + f * rowh + yoffset
                # day text
                txt = ""
                if f < len(weeks):
                    day = weeks[f][c]
                    txt = "{0}".format(day) if day != 0 else ""
                tm[f][c] = canvas.create_text(x, y, text=txt, state=tk.DISABLED)
    
    def _redraw(self):
        print('on redraw')
        canvas = self._canvas
        ch = canvas.winfo_height()
        cw = canvas.winfo_width()
        rowh = ch / 7.0
        colw = cw / 7.0
        # Header
        canvas.coords(self._rheader, 0, 0, cw, rowh)
        ox = 0
        oy = rowh / 2.0
        coffset = colw / 2.0
        cols = self._cal.formatweekheader(3).split()
        for i in range(0, 7):
            x = ox + i * colw + coffset
            item = self._theader[i]
            canvas.coords(item, x, oy)
            canvas.itemconfigure(item, text=cols[i])
        
        # background matrix
        oy = rowh
        ox = 0
        for f in range(0, 6):
            for c in range(0, 7):
                x = ox + c * colw
                y = oy + f * rowh
                x1 = x + colw - 1
                y1 = y + rowh - 1
                rec = self._recmat[f][c]
                canvas.coords(rec, x, y, x1, y1)
        
        # text matrix
        weeks = self._cal.monthdayscalendar(2016, 10)
        xoffset = colw / 2.0
        yoffset = rowh / 2.0
        oy = rowh
        ox = 0
        for f in range(0, 6):
            for c in range(0, 7):
                x = ox + c * colw + coffset
                y = oy + f * rowh + yoffset
                # day text
                txt = ""
                if f < len(weeks):
                    day = weeks[f][c]
                    txt = "{0}".format(day) if day != 0 else ""
                item = self._txtmat[f][c]
                canvas.coords(item, x, y)
                canvas.itemconfigure(item, text=txt)
        # after idle callback trick
        self.__cb = None
    
    def _on_canvas_configure(self, event=None):
        print('on_canvas_configure')
        if self.__cb is None:
            self.__cb = self.after_idle(self._redraw)

    def configure(self, cnf=None, **kw):
        args = tk._cnfmerge((cnf, kw))
        key = 'type'
        if key in args:
            self._choose = args[key]
            del args[key]
        ttk.Frame.configure(self, args)

    config = configure

    def cget(self, key):
        option = 'type'
        if key == option:
            return self._choose
        return ttk.Frame.cget(self, key)
        
    def mark_day():
        pass
    
    def unmark_day():
        pass

if __name__ == '__main__':
    root = tk.Tk()
    c = CalendarFrame(root)
    c.grid()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
