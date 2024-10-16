from dataclasses import dataclass
import mesa
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt  # Додано для візуалізації
from mesa.experimental.cell_space import CellAgent, Network


@dataclass
class NodeCoordinates:
    city: int
    x: float
    y: float

    @classmethod
    def from_line(cls, line: str):
        # Ініціалізація координат вузла з файлу
        city, x, y = line.split()
        return cls(int(city), float(x), float(y))


class TSPGraph:
    def __init__(self, g: nx.Graph, pheromone_init: float = 1e-6):
        self.g = g
        self.pheromone_init = pheromone_init
        self._add_edge_properties()  # Додаємо початкові властивості ребер

    @property
    def pos(self):
        # Повертаємо позиції вузлів графа
        return {k: v["pos"] for k, v in dict(self.g.nodes.data()).items()}

    @property
    def cities(self):
        # Повертаємо список міст (вузлів)
        return list(self.g.nodes)

    @property
    def num_cities(self):
        # Повертаємо кількість міст
        return len(self.g.nodes)

    def _add_edge_properties(self):
        # Додаємо властивості ребер: відстань, видимість, феромон
        for u, v in self.g.edges():
            u_x, u_y = self.g.nodes[u]["pos"]
            v_x, v_y = self.g.nodes[v]["pos"]
            self.g[u][v]["distance"] = ((u_x - v_x) ** 2 + (u_y - v_y) ** 2) ** 0.5
            self.g[u][v]["visibility"] = 1 / self.g[u][v]["distance"]
            self.g[u][v]["pheromone"] = self.pheromone_init

    @classmethod
    def from_random(cls, num_cities: int, seed: int = 0) -> "TSPGraph":
        # Створення випадкового графа
        g = nx.random_geometric_graph(num_cities, 2.0, seed=seed).to_directed()
        return cls(g)

    @classmethod
    def from_tsp_file(cls, file_path: str) -> "TSPGraph":
        # Ініціалізація графа з TSP-файлу
        with open(file_path) as f:
            lines = f.readlines()
            while lines.pop(0).strip() != "NODE_COORD_SECTION":
                pass

            g = nx.Graph()
            for line in lines:
                if line.strip() == "EOF":
                    break
                node_coordinate = NodeCoordinates.from_line(line)
                g.add_node(node_coordinate.city, pos=(node_coordinate.x, node_coordinate.y))

        # Створення повного графа
        for u in g.nodes():
            for v in g.nodes():
                if u == v:
                    continue
                g.add_edge(u, v)

        return cls(g)


class AntTSP(CellAgent):
    """
    Агент-мурашка, який вирішує задачу комівояжера.
    """

    def __init__(self, model, alpha: float = 1.0, beta: float = 5.0):
        super().__init__(model)
        self.alpha = alpha
        self.beta = beta
        self._cities_visited = []  # Міста, які відвідав агент
        self._traveled_distance = 0  # Загальна пройдена відстань
        self.tsp_solution = []  # Рішення для TSP
        self.tsp_distance = 0  # Відстань для TSP
        self.graph = self.model.grid.G

    def calculate_pheromone_delta(self, q: float = 100):
        # Розрахунок дельти феромону для ребер
        results = {}
        for idx, start_city in enumerate(self.tsp_solution[:-1]):
            end_city = self.tsp_solution[idx + 1]
            results[(start_city, end_city)] = q / self.tsp_distance
        return results

    def move_to(self, cell) -> None:
        # Рух до наступного міста (вузла)
        self._cities_visited.append(cell)
        if self.cell:
            self._traveled_distance += self.graph[self.cell.coordinate][cell.coordinate]["distance"]
        super().move_to(cell)

    def decide_next_city(self):
        # Вибір наступного міста на основі феромонів і видимості
        neighbors = self.cell.neighborhood
        candidates = [n for n in neighbors if n not in self._cities_visited]

        if len(candidates) == 0:
            return self.cell  # Якщо немає доступних міст, залишаємося в поточному

        # Формула для ймовірності вибору наступного міста
        results = []
        for city in candidates:
            val = (
                (self.graph[self.cell.coordinate][city.coordinate]["pheromone"]) ** self.alpha
                * (self.graph[self.cell.coordinate][city.coordinate]["visibility"]) ** self.beta
            )
            results.append(val)

        # Нормалізація результатів для обчислення ймовірностей
        results = np.array(results)
        norm = results.sum()
        results /= norm

        # Вибір нового міста на основі ймовірностей
        new_city = self.random.choices(candidates, weights=results)[0]
        return new_city

    def step(self):
        """
        Крок агента: переміщення та оновлення рішень TSP.
        """
        for _ in range(self.model.num_cities - 1):
            new_city = self.decide_next_city()
            self.move_to(new_city)

        # Оновлення рішення та відстані після повного маршруту
        self.tsp_solution = [entry.coordinate for entry in self._cities_visited]
        self.tsp_distance = self._traveled_distance
        self._cities_visited = []
        self._traveled_distance = 0


class AcoTspModel(mesa.Model):
    """
    Модель для вирішення задачі комівояжера з використанням алгоритму мурашиних колоній.
    """

    def __init__(
        self,
        num_agents: int = 20,
        tsp_graph: TSPGraph = TSPGraph.from_random(20),
        max_steps: int = int(1e6),
        ant_alpha: float = 1.0,
        ant_beta: float = 5.0,
    ):
        super().__init__()
        self.num_agents = num_agents  # Кількість агентів
        self.tsp_graph = tsp_graph  # Граф міст для TSP
        self.num_cities = tsp_graph.num_cities
        self.all_cities = set(range(self.num_cities))
        self.max_steps = max_steps
        self.grid = Network(tsp_graph.g, random=self.random)  # Використання мережі для агента

        # Створення агентів
        for _ in range(self.num_agents):
            agent = AntTSP(model=self, alpha=ant_alpha, beta=ant_beta)
            city = self.grid.all_cells.select_random_cell()  # Вибір випадкового початкового міста
            agent.move_to(city)

        self.num_steps = 0
        self.best_path = None  # Найкращий шлях
        self.best_distance = float("inf")  # Найменша відстань
        self.best_distance_iter = float("inf")  # Найменша відстань за ітерацію
        tsp_graph._add_edge_properties()  # Ініціалізація феромонів

        # Колектор даних для збору результатів
        self.datacollector = mesa.datacollection.DataCollector(
            model_reporters={
                "num_steps": "num_steps",
                "best_distance": "best_distance",
                "best_distance_iter": "best_distance_iter",
                "best_path": "best_path",
            },
            agent_reporters={
                "tsp_distance": "tsp_distance",
                "tsp_solution": "tsp_solution",
            },
        )
        self.datacollector.collect(self)  # Збір початкових даних

        self.running = True

    def update_pheromone(self, q: float = 100, ro: float = 0.5):
        # Оновлення рівнів феромону з урахуванням випаровування
        delta_tau_ij = {}
        for k, agent in enumerate(self.agents):
            delta_tau_ij[k] = agent.calculate_pheromone_delta(q)

        for i, j in self.grid.G.edges():
            # Випаровування феромонів
            tau_ij = (1 - ro) * self.grid.G[i][j]["pheromone"]
            # Додавання внеску від кожного агента
            for k, delta_tau_ij_k in delta_tau_ij.items():
                tau_ij += delta_tau_ij_k.get((i, j), 0.0)
            self.grid.G[i][j]["pheromone"] = tau_ij

    def step(self):
        """
        Крок моделі для активації агентів і збору даних.
        """
        self.agents.shuffle_do("step")  # Перемішуємо агентів перед кожним кроком
        self.update_pheromone()  # Оновлення феромонів після кожного кроку

        # Визначення найкращого рішення за ітерацію
        best_instance_iter = float("inf")
        for agent in self.agents:
            if agent.tsp_distance < self.best_distance:
                self.best_distance = agent.tsp_distance
                self.best_path = agent.tsp_solution
            if agent.tsp_distance < best_instance_iter:
                best_instance_iter = agent.tsp_distance

        self.best_distance_iter = best_instance_iter

        if self.num_steps >= self.max_steps:
            self.running = False

        self.datacollector.collect(self)  # Збір даних після кожного кроку

    def visualize(self):
        """
        Візуалізація поточного стану графа та феромонів.
        """
        plt.figure(figsize=(10, 10))
        pos = self.tsp_graph.pos  # Позиції міст
        nx.draw(self.grid.G, pos, node_size=300, node_color="skyblue", with_labels=True)
        edge_pheromones = [self.grid.G[u][v]["pheromone"] for u, v in self.grid.G.edges()]
        nx.draw_networkx_edges(self.grid.G, pos, width=edge_pheromones, edge_color=edge_pheromones, edge_cmap=plt.cm.Blues)
        plt.title("Visualization of the current TSP solution and pheromone levels")
        plt.show()  # Показуємо графік

# Приклад використання:
model = AcoTspModel()
model.visualize()  # Виклик візуалізації
