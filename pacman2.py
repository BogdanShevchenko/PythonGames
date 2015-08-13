import tkinter

class drawer():
    def __init__(self):
        self.init_var()
        self.root = tkinter.Tk()
        self.can = tkinter.Canvas(width=self.field_size[0], height=self.field_size[1])
        self.elements["canvas"] = self.can
        ###
        #fon = tkinter.PhotoImage(width=self.fon_size[0], height=self.fon_size[1], file = self.fon)
        #image = self.can.create_image(self.field_size[0] / 2, self.field_size[1] / 2, image=fon)
        self.can.pack()
        ###
        self.redraw()
        self.root.mainloop()
    def init_var(self):
        self.fon_size = (300, 300)
        self.field_size = [300, 300]
        self.time_speed = 250
        self.fon = "fon.gif"
        self.figs = {}
        self.tWindows = {}
        self.game = pacman(self)
        self.elements = {}
        self.delete_marks = []
        
    def bind(self, event_type):
        self.root.bind(event_type, self.game.controls)

    def redraw(self):
        for mark in self.delete_marks:
            self.can.delete(mark)
            for fig in self.figs[mark]:
                fig[0](fig[1], mark)
        self.delete_marks = []
        if self.game != 0:
            self.game.recalc()
        self.can.after(self.time_speed, self.redraw)

    def line(self, *args, **kwargs):
        if "mark" in kwargs:
            mark = kwargs["mark"]
        else:
            mark = "JAFL"
        self.can.create_line(args[0], args[1], args[2], args[3], tag = mark)
        if mark not in self.figs:
            self.figs[mark] = []
        self.figs[mark].append([args, kwargs])

    def toplevel(self, *args, **kwargs):
        if "title" in kwargs:
            title = kwargs.pop("title")
        else:
            title = "Window number " + str(len(self.tWindows)+1)
        if title not in self.tWindows:
            self.tWindows[title]=tkinter.Toplevel()
            if "width" in kwargs and "height" in kwargs:
                self.tWindows[title].geometry("{0}x{1}".format(kwargs["width"], kwargs["height"]))
            self.tWindows[title].title(title)
            self.tWindows[title].focus_set()

    def del_window(self, title):
        if title in self.tWindows:
            self.tWindows[title].destroy()
            del self.tWindows[title]
        else:
            print("Attempt to delete non-existing window!")
        
    def new_entry(self, *args, **kwargs):
        if "name" in kwargs:
            name = kwargs["name"]
        else:
            name = "Element number " + str(len(self.elements) + 1) 
        if name not in self.elements:
            self.elements[name]=tkinter.Entry(self.tWindows[args[0]], **kwargs)
            self.elements[name].pack()

    def new_label(self, *args, **kwargs):
        if "name" in kwargs:
            name = kwargs["name"]
        else:
            name = "Element number " + str(len(self.elements) + 1) 
        if name not in self.elements:
            self.elements[name]=tkinter.Label(self.tWindows[args[0]], **kwargs)
            self.elements[name].pack()

    def new_button(self, *args, **kwargs):
        if "name" in kwargs:
            name = kwargs["name"]
        else:
            name = "Element number " + str(len(self.elements) + 1) 
        if name not in self.elements:
            function = kwargs.pop("function", 0)
            self.elements[name]=tkinter.Button(self.tWindows[args[0]],**kwargs)
            self.elements[name].pack()
            if function != 0:
                self.elements[name].bind("<ButtonPress>", function)
                
    def element_method(self, name, method, *args, **kwargs):
        exec_method = getattr(self.elements[name], method)
        return exec_method(*args, **kwargs)
    
##########################
class pacman(drawer):
    def __init__(self, drawer):
        self.init_var()
        self.drawer = drawer
        self.drawer.game = self
        print("game is created!")
        
    def init_var(self):
        self.field_squares = [0, 0]
        self.is_going = True
        self.mode = "red"
        self.def_size = [20, 30]
        
    def recalc(self):
        if self.mode == "red":
            if self.field_squares == [0,0]:
                self.set_squares()
            else:
                self.redactor()

    def set_squares(self):
        SR = "Size Request"
        self.drawer.toplevel(title = SR, height = 100, width = 200)
        self.drawer.new_label(SR, width = 10, name = "h_label", text = "Height: ")
        self.drawer.new_entry(SR, width = 10, name = "h_text")
        self.drawer.new_label(SR, width = 10, name = "w_label", text = "Width: ")
        self.drawer.new_entry(SR, width = 10, name = "w_text")
        self.drawer.new_button(SR, width = 10, name = "size_b", text = "Ok", function = self.size_enter)

    def size_enter(self, event):
        m_get = "get"
        self.field_squares[0] = self.drawer.element_method("h_text", m_get)
        self.field_squares[1] = self.drawer.element_method("h_text", m_get)

        for i in [0,1]:
            if self.field_squares[i].isdigit():
                self.field_squares[i] = int(self.field_squares[i])
            else:
                self.field_squares[i] = self.def_size[i]
        self.drawer.del_window("Size Request")
        self.drawer.field_size[1] = self.drawer.field_size[0] * self.field_squares[1] / self.field_squares[0]
        self.drawer.element_method("canvas", "config", width = self.drawer.field_size[0], height = self.drawer.field_size[1])
        for i in range(self.field_squares[1] - 1):
            self.drawer.line((i + 1) * self.drawer.field_size[0] / self.field_squares[0], 0, (i + 1) * self.drawer.field_size[0] / self.field_squares[0], self.drawer.field_size[1], mark = "grid")
        for j in range(self.field_squares[0] - 1):
            self.drawer.line(0, (j + 1) * self.drawer.field_size[1] / self.field_squares[1], self.drawer.field_size[0], (j + 1) * self.drawer.field_size[1] / self.field_squares[1], mark = "grid")

        
    def redactor(self):
        pass 

    
draw_mashina = drawer()
#game1 = pacman(draw_mashina)
    
        
