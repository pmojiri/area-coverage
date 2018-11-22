#!/usr/bin/python
import networkx as nx
import cv2
import numpy as np

class reeb_graph:
  #def __init__(self):

  def read_file(self, filename):
      # read map file
      return cv2.imread(filename) # Read an image

  def draw_critical_points(self, cp, img):
      for i in range (0, cp.shape[0]):
        cv2.circle(img, (cp[i][0], cp[i][1]), 10, (0, 255, 0), 3)
        text = "cp" + str(i)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(img, text, (cp[i][0], cp[i][1]), font, 1, (0, 0, 255), 1)
        cv2.line(img, (cp[i][0], 0), (cp[i][0], img.shape[0]), (255, 255, 0), 1)

  def draw_cells(self, cells, img):
      eulerian_cells_array = cells
      color = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255) ]
      #draw the eulerian cells
      for i in range (0, eulerian_cells_array.shape[0]):
        for j in range (0, (len(eulerian_cells_array[i]) - 2)):
          x_ceil = eulerian_cells_array[i][j][0][0]
          y_ceil = eulerian_cells_array[i][j][0][1]
          x_floor = eulerian_cells_array[i][j][1][0]
          y_floor = eulerian_cells_array[i][j][1][1]
          
          cv2.circle(img, (x_ceil, y_ceil), 1, color[i], -1)
          cv2.circle(img, (x_floor, y_floor), 1, color[i], -1)

        text = "cell" + str(i)
        font = cv2.FONT_HERSHEY_PLAIN
        point = int(len(eulerian_cells_array[i]) / 2)
        text_x = int((eulerian_cells_array[i][point][0][0] + eulerian_cells_array[i][point][1][0]) / 2)
        text_y = int((eulerian_cells_array[i][point][0][1] + eulerian_cells_array[i][point][1][1]) / 2)
        cv2.putText(img, text, (text_x, text_y), font, 1, (0, 0, 255), 1)

    
  def reeb_graph_construction(self, critical_points, cells, mapfile):     
      self.img = self.read_file(mapfile)
      cp = critical_points
      all_cells = cells
      self.draw_critical_points(cp, self.img)

      G = nx.MultiGraph()
      for i in range (0, cp.shape[0]):
        G.add_node(i)
      for i in range (0, all_cells.shape[0]):
        j = len(all_cells[i]) - 1
        G.add_edge(all_cells[i][j][0], all_cells[i][j][1])

      #print G.number_of_nodes(), G.number_of_edges()
      #print G.nodes()
      #print G.edges()
      #print nx.degree(G)
      return G

  def eulerian_reeb_graph(self, reeb_graph, cells):
      G = reeb_graph
      all_cells = cells
  
      # change node degrees to even value by adding new edge to some nodes
      # the repeated cells constructed by dividing them to two cell and construct new reeb graph and new cells boundary
      new_cells = []
      cell_number = 0
      for i in range (0, G.number_of_nodes()):
        degree = nx.degree(G, i)
        if degree % 2 != 0:
          G.add_edge(G.edges(i)[i][0], G.edges(i)[i][1])    
          lenght = all_cells.shape[0]
          for m in range (0, lenght):
            n = len(all_cells[m]) - 1
            condition = ((all_cells[m][n][0] == G.edges(i)[i][0]) and (all_cells[m][n][1] == G.edges(i)[i][1])) 
            #print condition
            if condition:
              cells= tuple([] for a in range(2)) 
              for j in range(0, n):
                middle_point_floor = (all_cells[m][j][0][0], int((all_cells[m][j][0][1] + all_cells[m][j][1][1])/2), all_cells[m][j][0][2])
                middle_point_ceil = (all_cells[m][j][0][0], int((all_cells[m][j][0][1] + all_cells[m][j][1][1])/2) + 3, all_cells[m][j][0][2])
                cells[0].append((all_cells[m][j][0], middle_point_floor))
                cells[1].append((middle_point_ceil, all_cells[m][j][1]))
        
              cells[0].append((G.edges(i)[i][0], G.edges(i)[i][1]))
              cells[1].append((G.edges(i)[i][0], G.edges(i)[i][1]))
              new_cells.append(cells[0])
              new_cells.append(cells[1])
              cell_number = cell_number + 1
              break 
        else:
          new_cells.append(all_cells[cell_number]) 
          
      new_cells_array = np.array(new_cells)

 
      ## new reeb grapg informations
      #print G.number_of_nodes(), G.number_of_edges()
      #print G.nodes()
      #print G.edges()
      #print nx.degree(G)
      return G, new_cells_array

  def eulerian_list(self, reeb_graph):
      G = reeb_graph
      # check new graph is eulerian or not, if yes, give the list of edges that should be passed, and order them and set them as forward or backward
      print nx.is_eulerian(G)      
      eulerian_list = list(nx.eulerian_circuit(G))
      return eulerian_list

  def eulerian_cells(self, eulerian_list, new_cells_array):
      eulerian_length = len(eulerian_list)
      unordered_cells = new_cells_array
      eulerian_cells = []
      for i in range(0, eulerian_length):   
        for m in range(0, unordered_cells.shape[0]):
          n = len(unordered_cells[m]) - 1
          condition_forward = ((unordered_cells[m][n][0] == eulerian_list[i][0]) and (unordered_cells[m][n][1] == eulerian_list[i][1])) 
          condition_backward = ((unordered_cells[m][n][0] == eulerian_list[i][1]) and (unordered_cells[m][n][1] == eulerian_list[i][0])) 
          print condition_forward, condition_backward

          if condition_forward:
            print "forward" + str(m)
            unordered_cells[m].append((1))
            eulerian_cells.append(unordered_cells[m])
            unordered_cells = np.delete(unordered_cells, m, 0)      
            break

          if condition_backward:
            print "backward" + str(m)
            unordered_cells[m].append((-1))
            eulerian_cells.append(unordered_cells[m])
            unordered_cells = np.delete(unordered_cells, m, 0)
            break
     
      eulerian_cells_array = np.array(eulerian_cells)
      self.draw_cells(eulerian_cells_array, self.img)
      cv2.imwrite("Eulerian_cells.jpg", self.img)
      return eulerian_cells_array 
