import networkx as nx
import numpy as np
from mesa import Model
from mesa.discrete_space import Network

from agents import NodeAgent

class AgentNetwork(Model):
    
    def __init__(self,seed=None):
        super().__init__(seed=seed)
        self.graph = nx.Graph()
        self.graph.add_node(0)
        self.graph.add_node(1)
        self.graph.add_edge(0,1)
        self.new_node=1
        self.grid = Network(self.graph,capacity=1,random=self.random) 
        NodeAgent.create_agents(model=self,n=2,cell=list(self.grid.all_cells))
    

    def step(self):
        print("taking steppp...........")
        self.new_node += 1
        self.graph.add_node(self.new_node)

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