from tkinter import Tk, Text, E, W, END
from tkinter import ttk, filedialog, messagebox
from sys import exit
from index import ModPack
from threading import Thread

import os
import asyncio

class Main(Tk):
    def init(self):
        self.title('Curse ModPack Downloader')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.gm1 = int(self.screen_width * .6)
        self.gm2 = int(self.screen_height * .6)
        self.geometry(f'{self.gm1}x{self.gm2}+{self.gm1 // 3}+{self.gm2 // 4}')
        self.resizable(False, False) #TODO: UNCOMMENT THIS LINE
        self.iconbitmap('assets/icon.ico')
        self.configure(background='#1a1a1a')

        # Creating the widgets
        self.lbl1 = ttk.Label(self, 
                              text='Choose a ModPack :',
                              font=('Arial', 12),
                              background='#1a1a1a',
                              foreground='#ffffff',
                              )
        self.mdpack = ttk.Entry(self,
                                width=self.gm1 // 15,
                                font=('Arial', 12),
                                foreground='#1a1a1a',
                                background='#ffffff',
                                # cursor='hand2',
        
            )
        self.destfol_lbl = ttk.Label(self,
                                     text='Choose where to download :',
                                     background='#1a1a1a',
                                     foreground='#ffffff',
                                     font=('Arial', 12),)
        self.destfol = ttk.Entry(self,
                                 width=self.gm1 // 15,
                                 font=('Arial', 12),
                                 foreground='#1a1a1a',
                                 background='#ffffff',
            )
        self.fol_browse = ttk.Button(self,
                                     command=self.browse_dest,
                                     width=self.gm1 // 80,
                                     text='Browse',
                                     cursor='hand2',
                                     
            )
        self.browse_btn = ttk.Button(self,
                                     width=self.gm1 // 80,
                                     text='Browse',
                                     command=self.browse_file,
                                     cursor='hand2',

            )     
        self.pbar = ttk.Progressbar(self,
                                    length=int(self.gm1 * .604),
                                    orient='horizontal',
                                    mode='determinate',
            )
        self.p = ttk.Label(self,
                           text='Downloading Progress : ',
                            font=('Arial', 12),
                            background='#1a1a1a',
                            foreground='#ffffff',
            )
        self.textlog = Text(self,
                            width=self.gm1 // 13,
                            height=self.gm2 // 30,
                            background='#1a1a1a',
                            foreground='#ffffff',
                            state='disabled')
        self.start_download_btn = ttk.Button(self,
                                             command=lambda: asyncio.run(self.start_download()),
                                             text='Start Download',
                                             cursor='hand2',
            )
        self.logs_lbl = ttk.Label(self,
                             background='#1a1a1a',
                             foreground='#ffffff',
                             font=('Arial', 12),
                             text='Logs and Debug:',
            )
        self.copy_btn = ttk.Button(self,
                                   text='Copy Logs',
                                   command=self.copy_logs,
                                   cursor='hand2',
            )
        
        # Placing the widgets
        self.lbl1.grid(row=0,
                       column=0,
                       pady=10,
                       sticky=E,
                       padx=10,
                       )
        self.mdpack.grid(row=0,
                         column=1,
                         pady=10,
                         sticky=E,
                         padx=10,
            )
        self.browse_btn.grid(row=0,
                             column=2,
                             pady=10,
                            sticky=W,
                            padx=10,
            )
        self.destfol_lbl.grid(row=1,
                              column=0,
                              pady=10,
                              sticky=W,
                              padx=10,
            )
        self.destfol.grid(row=1,
                          column=1,
                          pady=10,
                          padx=10,
                          sticky=E,
            )
        self.fol_browse.grid(row=1,
                             column=2,
                             padx=10,
                             pady=10,
            )
        self.p.grid(row=2,
                    column=0,
                    pady=10,
                    padx=10,
                    sticky=E,
            )
        self.pbar.grid(row=2,
                       column=1,
                       pady=10,
                       padx=10,
                       sticky=E,
                       )
        self.textlog.grid(row=3,
                          column=1,
                          pady=10,
                          padx=10,
                          )
        self.logs_lbl.grid(row=3,
                           column=0,
                           pady=10,
                           padx=10,
            )
        self.start_download_btn.grid(row=4,
                                     column=1,
                                     pady=10,
                                     padx=10,
                                    #  columnspan=2,
                                     sticky=E,
                                     )
        self.copy_btn.grid(row=4,
                           column=1,
                           padx=10,
                           pady=10,
                           sticky=W,
            )
        
    def browse_file(self):
        file_ = filedialog.askopenfilename(
            filetypes=[('ModPack', ['*.zip', '*.rar']), ('All Files', ['*.*'])],
            title='Choose a ModPack',
            defaultextension='*.zip',
            initialdir=os.path.expanduser('~'),
        )
        if file_:
            self.mdpack.delete(0, END)
            self.mdpack.insert(0, file_)

    def browse_dest(self):
        folder = filedialog.askdirectory(
            initialdir=os.path.expanduser('~'),
            title='Choose where to download',
            mustexist=True,
        )
        if folder:
            self.destfol.delete(0, END)
            self.destfol.insert(0, folder)

    def copy_logs(self):
        self.textlog.clipboard_clear()
        self.textlog.clipboard_append(self.textlog.get(1.0, END))

    def download_modpack(self):
        self.modpack = ModPack(path=self.mdpack.get(), func=self.log)
        self.modpack.init()
        self.modpack.get_links()
        t = Thread(target=self.modpack.install, args=(self.destfol.get(), self.pbar))
        t.daemon = True
        t.start()
        return
    
    async def start_download(self):
        self.start_download_btn.config(state='disabled')
        try:
            self.download_modpack()
        except Exception as e:
            self.log('Error : {}'.format(e))
            self.log('Download Failed')
            messagebox.showerror('Error', f'Download Failed:\n Error: {e}')
        finally:
            self.start_download_btn.config(state='!disabled')
        
    def log(self, text, type_:str='info'):
        self.textlog.configure(state='normal')
        self.textlog.insert(END, f'[ {type_.upper()} ]: '+text+'\n')
        self.textlog.configure(state='disabled')
        self.textlog.see(END)
    
    def start(self):
        self.init()
        self.mainloop()
        exit(0)

if __name__ == '__main__':
    app = Main()
    app.start()