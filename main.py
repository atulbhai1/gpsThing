from tkinter import *
from tkinter.messagebox import *
from datetime import datetime, timedelta
def get_entry(prompt, name='tk', button='OK'):
    global show
    window = Tk()
    window.title(name)
    show = ''
    Label(window, text=prompt).grid(row=0, column=0, sticky=W)
    entry = Entry(window)
    entry.grid(row=0, column=1)
    def ok():
        global show
        show = entry.get()
        window.destroy()
    Button(window, text=button, command=ok).grid(row=2, column=0, columnspan=2)
    window.mainloop()
    return show
intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds, granularity=4):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(round(value), name))
    return ', '.join(result[:granularity])
def get_dropdown(prompt, options=[''], name='tk', button='OK'):
    window = Tk()
    window.title(name)
    Label(window, text=prompt).grid(row=0, column=0, sticky=W)
    answer = StringVar()
    answer.set(options[0])
    answers = list(options)
    OptionMenu(window, answer, *answers).grid(row=0, column=1)
    Button(window, text=button, command=window.destroy).grid(row=1, column=0, columnspan=2)
    window.mainloop()
    return answer.get()
def theMainApp():
    formatted = "Unit Number, Street Name(Avenue->Aveune), City, County, State/Province, Postal Code, Country"
    start_address = get_entry(f'Starting Address(Use a ({formatted}) format):', 'Travel Info Calculator', 'Next')
    end_address = get_entry(f'Ending Address(Use a ({formatted}) format)', 'Travel Info Calculator', 'Next')
    MilesOrKilometers = get_dropdown('Miles Or Kilometers?', ['miles', 'km'], 'Travel Info Calculator', 'Next')
    try:
        from geopy import Nominatim
        locator = Nominatim(user_agent="geoapiExercises")
        location = locator.geocode(start_address)
        #9857 Shearwater Aveune Northwest, Concord, Cabarrus County, North Carolina, 28027:28078, United States
        start_coor = (location.latitude, location.longitude)
        location = locator.geocode(end_address)
        #1036 Old Sackville Rd, Middle Sackville, NS B4E 3A6, Canada
        end_coor = (location.latitude, location.longitude)
        print(start_coor, end_coor)
        import requests
        import json
        # call the OSMR API
        r = requests.get(f"http://router.project-osrm.org/route/v1/car/{start_coor[1]},{start_coor[0]};{end_coor[1]},{end_coor[0]}?overview=false""")
        # then you load the response using the json libray
        # by default you get only one alternative so you access 0-th element of the `routes`
        routes = json.loads(r.content)
        route_1 = routes.get("routes")[0]
        print(route_1)
        print(routes.get("routes"))
        if MilesOrKilometers == 'miles':
            total_distance = (route_1['legs'][0]['distance'])/1760
        else:
            total_distance = (route_1['legs'][0]['distance'])/1094
        total_time = display_time(route_1['legs'][0]['duration'])
        tk = Tk()
        tk.title('Travel Info Calculator')
        Label(master=tk, text=f'Info for {start_address.replace("Aveune", "Avenue")} to {end_address.replace("Aveune", "Avenue")}', font=("Arial", 16)).pack()
        Label(master=tk, text=f'Total Distance: {round(total_distance)} {MilesOrKilometers}').pack()
        Label(master=tk, text=f'Total Time: {total_time}').pack()
        Button(master=tk, text='Ok', command=tk.destroy).pack()
        tk.mainloop()
        if askyesno('Travel Info Calculator', 'Want to get info on another journey?'):
            theMainApp()
    except Exception as e:
        print(e)
        showerror('Travel Info Calculator', 'Something bad happened, please try again')
        if askyesno('Travel Info Calculator', 'Want to try again?'):
            theMainApp()
theMainApp()