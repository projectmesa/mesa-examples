import networkx as nx
import numpy as np
from mesa import Model, DataCollector
from mesa.discrete_space import Network

from agents import NodeAgent

def calculate_total_degree(model):
    _ , degree = zip(*model.graph.degree())
    return sum(degree)

class AgentNetwork(Model):
    
    def __init__(self,num=100,seed=None):
        super().__init__(seed=seed)
        self.num = num
        self.graph = nx.Graph()
        self.new_node=1
        for i in range(self.num):
            self.graph.add_node(i)

        self.graph.add_edge(0,1)

        self.datacollector = DataCollector(
            {
            "Degree": calculate_total_degree,
            }
        )
    
        self.grid = Network(self.graph,capacity=1,random=self.random) 
        NodeAgent.create_agents(model=self,n=self.num,cell=list(self.grid.all_cells))
    

    def step(self):
        print("taking steppp...........")
        self.new_node += 1

        # if self.new_node >= self.num:
        #     break
            
        # self.graph.add_node(self.new_node)

        # extract node IDs along with their degrees
        nodes, degree = zip(*self.graph.degree())
        total_degree = sum(degree)

        # probabilities of connecting to an existing node
        probabilities = [d/total_degree for d in degree]

        # choose an existing node based on the computed probabilities
        chosen_node = np.random.choice(nodes, p=probabilities)

        # add the new node and connect it to the choosen node
        self.graph.add_edge(chosen_node,self.new_node)

        # for x in self.agents:
        #     print(x.unique_id)

        self.datacollector.collect(self)