#!/usr/bin/env python3
"""
Simple e621 image viewer.

This program uses the esix library to connect to the site's API and
fetch images matching your query.
"""
from tkinter import *
from PIL import Image, ImageTk
from argparse import ArgumentParser
import esix
import urllib.request
import io

DEFAULT_QUERY = "blotch rating:safe"
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) ' +\
             'Gecko/20120101 Firefox/29.0'

def get_img_list(query,limit=75):
    query += ' -type:swf'
    print('Searching with query: '+query)
    search_result = esix.post.search(query,limit)
    return [f.file_url for f in search_result
            if f.file_ext in ('jpg','png','gif')]

class ImgView:
    win_width, win_height = (1024, 768)
    img_list = []
    cur_img = 0
    
    def __init__(self, master, query=None):
        self.master = master
        self.win_prop = self.win_width/float(self.win_height)
        self.master.geometry("%dx%d" % (self.win_width,self.win_height))
        if not query: query = ''

        menubar = Menu(self.master)
        options_menu = Menu(menubar,tearoff=0)
        self.search_limit = IntVar(value=75)
        search_limit = Menu(options_menu,tearoff=0)
        search_limit.add_radiobutton(label="25",value=25,
                                     variable=self.search_limit)
        search_limit.add_radiobutton(label="50",value=50,
                                     variable=self.search_limit)
        search_limit.add_radiobutton(label="75",value=75,
                                     variable=self.search_limit)
        search_limit.add_radiobutton(label="100",value=100,
                                     variable=self.search_limit)
        search_limit.add_radiobutton(label="None",value=0,
                                     variable=self.search_limit)
        options_menu.add_cascade(label="Search Limit",menu=search_limit)
        menubar.add_cascade(label="Options",menu=options_menu)
        self.master.config(menu=menubar)
        

        url_entry = Frame(self.master,padx=5,pady=5)
        url_entry.pack(side=TOP,fill="x")
        Label(url_entry,text='URL:',padx=2).pack(side=LEFT)
        self.url_entry = Entry(url_entry)
        self.url_entry.pack(side=LEFT,fill="x",expand=True)
        self.url_entry.bind("<Return>",self.on_search_click)
        self.url_entry.focus_set()
        self.url_entry.insert(END,query)
        self.search_button = Button(url_entry,text="Search",padx=2,
                                    command=self.on_search_click)
        self.search_button.pack(side=LEFT)
        
        image_area = Frame(self.master,padx=5,pady=2)
        image_area.pack(side=TOP,fill="both",expand=True)
        Button(image_area,text="<",
               command=self.on_prev_click).pack(side=LEFT,fill="y")
        self.image_frame = Frame(image_area,padx=5,pady=2)
        self.image_frame.pack(side=LEFT,fill="both",expand=True)
        Button(image_area,text=">",
               command=self.on_next_click).pack(side=RIGHT,fill="y")
        status_bar = Frame(self.master,padx=5)
        status_bar.pack(side=BOTTOM,fill="x")
        self.status_label = Label(status_bar)
        self.status_label.pack(side=LEFT,fill="x")
        

    def set_status(self,text,color='black'):
        self.status_label.configure(text=text,fg=color)

    def on_search_click(self,event=None):
        self.cur_img = 0
        self.search_button.configure(text='Searching',state=DISABLED)
        self.set_status('Searching...')
        self.master.update()
        query = self.url_entry.get()
        self.img_list = get_img_list(query,self.search_limit.get())
        self.set_status(str(len(self.img_list))+' images found.')
        self.search_button.configure(text='Search',state=NORMAL)
        if len(self.img_list): self.display_current_image()

    def on_next_click(self):
        if not len(self.img_list): return
        if self.cur_img >= len(self.img_list)-1: self.cur_img = 0
        else: self.cur_img += 1
        self.display_current_image()

    def on_prev_click(self):
        if not len(self.img_list): return
        if self.cur_img == 0: self.cur_img = len(self.img_list)-1
        else: self.cur_img -= 1
        self.display_current_image()
        
    def load_image(self,url):
        print('Loading '+url)
        try:
            req = urllib.request.Request(url,headers={
                'User-Agent':USER_AGENT})
            img_data = urllib.request.urlopen(req).read()
            data_stream = io.BytesIO(img_data)
            image = Image.open(data_stream)
        except Exception as err:
            print('Error: '+str(err),file=sys.stderr)
            return False
        frame_width, frame_height = (
            self.image_frame.winfo_width(),self.image_frame.winfo_height())
        frame_prop = frame_width/float(frame_height)
        img_prop = image.size[0]/float(image.size[1])
        if img_prop < frame_prop:
            img_h = int(frame_height)
            img_w = int(img_h*img_prop)
        else:
            img_h = int(frame_width/img_prop)
            img_w = int(img_h*img_prop)
        method = Image.BILINEAR
        image = image.resize((img_w,img_h),method)
        return image
        
    def show_image(self,image):
        self.tk_image = ImageTk.PhotoImage(image)
        label = Label(self.image_frame,image=self.tk_image)
        label.place(relx=0.5,rely=0.5,anchor=CENTER)

    def display_current_image(self):
        img = self.load_image(self.img_list[self.cur_img])
        if img:
            self.show_image(img)
            self.set_status('Image '+str(self.cur_img+1)+\
                            ' of '+str(len(self.img_list))+'.')
        

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('query',type=str,nargs='?',default=DEFAULT_QUERY)
    args = vars(parser.parse_args())
    root = Tk()
    app = ImgView(root,args['query'])
    root.mainloop()
