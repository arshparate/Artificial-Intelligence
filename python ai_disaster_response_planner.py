import tkinter as tk
from tkinter import ttk
import heapq
import random
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

# =============================================================
# ULTRA ADVANCED AI DISASTER COMMAND CENTER
# Manual Simulation + Auto Simulation + Multi-Agent AI Planning
# =============================================================

# -------------------------------------------------------------
# GRAPH MODEL (CITY INFRASTRUCTURE)
# -------------------------------------------------------------

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self,u,v,cost):
        self.graph.setdefault(u,[]).append((v,cost))
        self.graph.setdefault(v,[]).append((u,cost))

    def neighbors(self,node):
        return self.graph.get(node,[])


# -------------------------------------------------------------
# ROUTING AI (A* SEARCH)
# -------------------------------------------------------------

def heuristic(a,b):
    return abs(hash(a)-hash(b)) % 10


def a_star(graph,start,goal):

    pq=[]
    heapq.heappush(pq,(0,start))

    came={start:None}
    cost={start:0}

    while pq:

        _,current=heapq.heappop(pq)

        if current==goal:
            break

        for nxt,w in graph.neighbors(current):

            new_cost=cost[current]+w

            if nxt not in cost or new_cost<cost[nxt]:

                cost[nxt]=new_cost

                priority=new_cost+heuristic(nxt,goal)

                heapq.heappush(pq,(priority,nxt))

                came[nxt]=current

    if goal not in came:
        return None

    path=[]
    node=goal

    while node:
        path.append(node)
        node=came[node]

    path.reverse()

    return path


# -------------------------------------------------------------
# CITY NETWORK
# -------------------------------------------------------------

graph=Graph()

edges=[
("Base","Hospital",4),
("Base","FireStation",3),
("FireStation","SectorA",2),
("SectorA","SectorB",2),
("SectorB","SectorC",3),
("Hospital","SectorB",4),
("SectorC","ReliefCamp",2),
("SectorB","Airport",5),
("Airport","ReliefCamp",3),
("SectorC","Harbor",4),
("Harbor","ReliefCamp",2)
]

for u,v,w in edges:
    graph.add_edge(u,v,w)

locations=list(graph.graph.keys())


# -------------------------------------------------------------
# RESOURCE DATABASE
# -------------------------------------------------------------

rescue_teams=[
"Fire Rescue Unit",
"Medical Rapid Team",
"Flood Rescue Team",
"Police Emergency Unit",
"NDRF Special Unit"
]

vehicles=[
"Ambulance",
"Fire Truck",
"Rescue Boat",
"Helicopter",
"Drone Surveillance"
]


# -------------------------------------------------------------
# DISASTER GENERATOR
# -------------------------------------------------------------

def auto_disaster():

    disaster=random.choice([
    "Flood",
    "Fire",
    "Earthquake",
    "Chemical Leak",
    "Building Collapse"
    ])

    location=random.choice(locations)

    severity=random.randint(1,10)

    population=random.randint(100,2000)

    spread=random.randint(10,90)

    return disaster,location,severity,population,spread


# -------------------------------------------------------------
# GRAPH VISUALIZATION
# -------------------------------------------------------------

def show_graph(path=None,danger=None):

    G=nx.Graph()

    for u in graph.graph:
        for v,w in graph.graph[u]:
            G.add_edge(u,v,weight=w)

    pos=nx.spring_layout(G)

    node_colors=[]

    for n in G.nodes():

        if n==danger:
            node_colors.append("red")
        else:
            node_colors.append("skyblue")

    edge_colors=[]

    for u,v in G.edges():

        if path and u in path and v in path:
            edge_colors.append("red")
        else:
            edge_colors.append("gray")

    nx.draw(G,pos,with_labels=True,node_color=node_colors,edge_color=edge_colors,node_size=2600)

    labels=nx.get_edge_attributes(G,'weight')

    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

    plt.title("AI Disaster Network Simulation")

    plt.show()


# -------------------------------------------------------------
# COMMAND CENTER GUI
# -------------------------------------------------------------

class CommandCenter:

    def __init__(self,root):

        self.root=root

        root.title("AI DISASTER COMMAND CENTER")

        root.geometry("1250x750")

        root.configure(bg="#0f172a")

        header=tk.Label(root,
        text="AI DISASTER RESPONSE COMMAND CENTER",
        font=("Segoe UI",22,"bold"),
        fg="cyan",
        bg="#020617")

        header.pack(fill="x",pady=10)


        # METRICS DASHBOARD

        dash=tk.Frame(root,bg="#0f172a")
        dash.pack(fill="x")

        self.metric=tk.Label(dash,
        text="Active Disasters: 0 | Teams Deployed: 0 | People Rescued: 0",
        fg="lime",
        bg="#0f172a",
        font=("Segoe UI",11,"bold"))

        self.metric.pack(anchor="w",padx=20,pady=5)


        # CONTROL PANEL

        panel=tk.Frame(root,bg="#0f172a")
        panel.pack(pady=10)

        ttk.Button(panel,text="Manual Simulation",command=self.manual_sim).grid(row=0,column=0,padx=10)

        ttk.Button(panel,text="Auto Simulation",command=self.auto_mode).grid(row=0,column=1,padx=10)

        ttk.Button(panel,text="Show City Network",command=lambda: show_graph()).grid(row=0,column=2,padx=10)


        # MANUAL INPUTS

        manual=tk.Frame(root,bg="#0f172a")
        manual.pack()

        tk.Label(manual,text="Disaster Type",bg="#0f172a",fg="white").grid(row=0,column=0)
        tk.Label(manual,text="Location",bg="#0f172a",fg="white").grid(row=0,column=1)
        tk.Label(manual,text="Severity",bg="#0f172a",fg="white").grid(row=0,column=2)

        self.disaster_box=ttk.Combobox(manual,values=["Flood","Fire","Earthquake","Chemical Leak","Collapse"],width=20)
        self.disaster_box.grid(row=1,column=0,padx=5)

        self.loc_box=ttk.Combobox(manual,values=locations,width=20)
        self.loc_box.grid(row=1,column=1,padx=5)

        self.severity_box=ttk.Combobox(manual,values=list(range(1,11)),width=10)
        self.severity_box.grid(row=1,column=2,padx=5)


        # CONSOLE OUTPUT

        frame=tk.Frame(root,bg="#0f172a")
        frame.pack(fill="both",expand=True,padx=20,pady=20)

        self.console=tk.Text(frame,bg="#020617",fg="white",font=("Consolas",11))

        self.console.pack(fill="both",expand=True)


        # METRICS

        self.disasters=0
        self.teams=0
        self.rescued=0


    # -------------------------------------------------

    def run_ai(self,disaster,location,severity,population,spread):

        start="Base"

        path=a_star(graph,start,location)

        team=random.choice(rescue_teams)

        vehicle=random.choice(vehicles)

        eta=random.randint(5,25)

        rescued_now=random.randint(20,150)

        self.disasters+=1
        self.teams+=1
        self.rescued+=rescued_now

        self.metric.config(text=f"Active Disasters: {self.disasters} | Teams Deployed: {self.teams} | People Rescued: {self.rescued}")

        route=" -> ".join(path) if path else "No route"

        time=datetime.now().strftime("%H:%M:%S")

        report=f"""
========================================================
AI DISASTER RESPONSE SIMULATION
Time: {time}
========================================================

Disaster Type      : {disaster}
Location           : {location}
Severity           : {severity}/10
Population At Risk : {population}
Spread Risk        : {spread}%

Optimal Route
-----------------------------------
{route}

AI Resource Allocation
-----------------------------------
Team     : {team}
Vehicle  : {vehicle}
ETA      : {eta} minutes

Evacuation Update
-----------------------------------
People Rescued This Mission : {rescued_now}

MISSION STATUS : ACTIVE RESPONSE
========================================================
"""

        self.console.insert(tk.END,report)

        show_graph(path,location)


    # -------------------------------------------------

    def manual_sim(self):

        disaster=self.disaster_box.get()
        location=self.loc_box.get()
        severity=int(self.severity_box.get()) if self.severity_box.get() else 5

        population=random.randint(200,2000)

        spread=random.randint(10,90)

        if not disaster or not location:
            return

        self.run_ai(disaster,location,severity,population,spread)


    # -------------------------------------------------

    def auto_mode(self):

        disaster,location,severity,population,spread=auto_disaster()

        self.run_ai(disaster,location,severity,population,spread)

        self.root.after(8000,self.auto_mode)


# -------------------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------------------

if __name__=="__main__":

    root=tk.Tk()

    app=CommandCenter(root)

    root.mainloop()
