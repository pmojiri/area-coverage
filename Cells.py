#!/usr/bin/python
import cv2
import numpy as np
from Critical_points import critical_points

class cell:
  #def __init__(self):

  def read_file(self, filename):
      # read map file
      return cv2.imread(filename) # Read an image    

  def laplacian(self, bitmap):
      # laplacian function
      laplacian= cv2.Laplacian(bitmap, cv2.CV_16S)
      laplacian = cv2.convertScaleAbs(laplacian)
      cv2.imwrite("laplacian.jpg", laplacian) 
      return laplacian

  def canny(self, bitmap):
      # canny edges detection function
      #bitmap = cv2.blur(bitmap, (4,4))
      canny_edges = cv2.Canny(bitmap, 100, 300)
      canny_edges = cv2.convertScaleAbs(canny_edges)
      cv2.imwrite("canny_edges.jpg", canny_edges)
      return canny_edges

  def cell_construction(self, bitmap):
      # read map file:
      filename = "map_stong.png"
      filename = "map_zoom20.png"
      #filename = "square.png"
      filename = "Ellipes.png"
      filename = "map_loafers_1.jpg"
      #filename = "circle.png"
      #filename = "1.png"
      #filename = "2.png"
      #filename = "3.png"
      #filename = "StongPondmap.png"
      #filename = "mix.png"
      #filename = "mixed_mixed.png"
      self.img = self.read_file(filename)

      #compute the gradient of a bitmap image using laplacian or canny edges detection     
      laplacian = self.laplacian(bitmap)
      canny_edges = self.canny(bitmap)


      criticalpoints = critical_points()
      cp = criticalpoints.find_cp(bitmap)
      for i in range (0, cp.shape[0]):
        cv2.circle(self.img, (cp[i][0], cp[i][1]), 10, (0, 255, 0), 3)
        text = "cp" + str(i)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(self.img, text, (cp[i][0], cp[i][1]), font, 1, (0, 0, 255), 2, cv2.CV_AA )

      
      height, width = bitmap.shape
      
      s = np.zeros(height)
      self.s_count = np.zeros(width)
      self.s_free_count = np.zeros(width)
      self.filtered_points = []
      self.grouped_s_free = []
            
      for i in range(0, width):
        points = []
        s_free = []
        for j in range(0, height):
          s[j] = bitmap[j,i]
          if bitmap[j,i] > 0.0:
            s_free.append((i, j, bitmap[j,i]))
          if canny_edges[j,i] > 0.0:
            points.append((i, j, canny_edges[j,i], bitmap[j,i]))                    
        self.p = np.array(points)
        self.s_free = np.array(s_free)

                
        filtered_points = []        
        m = 0
        m_next = 0
        m_up = self.p.shape[0]
        while m < m_up:
          neighbors= []
          neighbors.append(self.p[m][1])
          n = m + 1
          if n < m_up:
            while n < m_up:
              condition = np.abs(self.p[n][1] - self.p[m][1]) == n - m
              if not condition:
                m_next = n 
                break          
              else :
                neighbors.append(self.p[n][1])
                m_next = n + 1
              n = n + 1
          else :
            m_next = m + 1
          m = m_next
          self.neighbors = np.array(neighbors)
          neighbors_mean = np.mean(self.neighbors)
          neighbors_mean = np.int_(neighbors_mean)            
          filtered_points.append((i, neighbors_mean, canny_edges[neighbors_mean,i], bitmap[neighbors_mean,i]))

        filtered_points_array = np.array(filtered_points)
        self.filtered_points.append(filtered_points)

        if filtered_points_array.shape[0] == 0.0:
          self.s_count[i] = 0.0
        else:
          self.s_count[i] = filtered_points_array.shape[0] + 1 

        if self.s_free.shape[0] != 0:
          k = 0
          k_up = self.s_free.shape[0] 
          grouped_s_neighbors = []
          s_free_count = 0
          k_next = 0                              
          while k < k_up :
            s_neighbors= []
            s_neighbors.append((self.s_free[k][0], self.s_free[k][1], self.s_free[k][2]))
            l = k + 1
            if l < k_up:
              while l < k_up:
                condition = np.abs(self.s_free[l][1] - self.s_free[k][1]) == l - k
                if not condition:
                  k_next = l 
                  break          
                else :
                  s_neighbors.append((self.s_free[l][0], self.s_free[l][1], self.s_free[l][2]))
                  k_next = l + 1
                l = l + 1 
            else :
              k_next = k + 1
            k = k_next
            
            s_neighbors_array = np.array(s_neighbors)          
            s_free_count = s_free_count + 1
            self.s_free_count[i] = s_free_count
            grouped_s_neighbors.append(s_neighbors)
          self.grouped_s_free.append(grouped_s_neighbors)
        else :
          self.grouped_s_free.append([])

      self.filtered_points_array = np.array(self.filtered_points)
      self.grouped_s_free_array = np.array(self.grouped_s_free)

      cells_all = []
      a = 1
      a_up = width
      num = 0
      cp_s = 0
      cp_e = 0

      while a < a_up:
        #print a
        if (self.s_free_count[a] != self.s_free_count[a - 1]) and (self.s_free_count[a] !=0):
          cell_num = self.s_free_count[a]
          if (self.s_free_count[a] < self.s_free_count[a - 1]):
            for i in range(0, int(cell_num)):
              x_0 = self.grouped_s_free_array[a][i][0][0]
              y_0 = self.grouped_s_free_array[a][i][0][1]
              x_n = self.grouped_s_free_array[a][i][len(self.grouped_s_free_array[a][i]) - 1][0]
              y_n = self.grouped_s_free_array[a][i][len(self.grouped_s_free_array[a][i]) - 1][1]
              cv2.line(self.img, (x_0, y_0), (x_n, y_n), (255, 255, 0), 2)
          if (self.s_free_count[a] > self.s_free_count[a - 1]):
            for i in range(0, int(self.s_free_count[a - 1])):
              x_0 = self.grouped_s_free_array[a - 1][i][0][0]
              y_0 = self.grouped_s_free_array[a - 1][i][0][1]
              x_n = self.grouped_s_free_array[a - 1 ][i][len(self.grouped_s_free_array[a - 1][i]) - 1][0]
              y_n = self.grouped_s_free_array[a - 1][i][len(self.grouped_s_free_array[a - 1][i]) - 1][1]
              cv2.line(self.img, (x_0, y_0), (x_n, y_n), (255, 255, 0), 2)

          for i_check in range(0, cp.shape[0]):
            if (cp[i_check][0] == a) or (cp[i_check][0] == (a - 1)) or (cp[i_check][0] == (a + 1)) :
              cp_s = i_check
          
          cell_num = self.s_free_count[a]
          #print "creating cells" + str (cell_num)
          cells= tuple([] for i in range (int(cell_num)))        
          b = a
          while self.s_free_count[b] == self.s_free_count[b + 1]:
            #print "b is " + str(b)
            free_space = self.grouped_s_free_array[b]
            for c in range(0, int(cell_num)):
              max_value = len(free_space[c])
              cells[c].append((free_space[c][0], free_space[c][max_value - 1]))
            b = b + 1
            for i_check in range(0, cp.shape[0]):
              if (cp[i_check][0] == b) or (cp[i_check][0] == (b - 1)) or (cp[i_check][0] == (b + 1)) :
                cp_e = i_check
               
          for d in range(0, int(cell_num)):
            cells[d].append((cp_s, cp_e))
            cells_all.append(cells[d])
            num = num + 1

          a = b
          num = num + 1

        else:
          a = a + 1
         
      cells_all = np.array(cells_all)

      color = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255), (0, 255, 255), (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255)]
      for i in range (0, cells_all.shape[0]):
        #print (len(cells_all[i]) - 1)
        for j in range (0, (len(cells_all[i]) - 1)):
          x_ceil = cells_all[i][j][0][0]
          y_ceil = cells_all[i][j][0][1]
          x_floor = cells_all[i][j][1][0]
          y_floor = cells_all[i][j][1][1]
          
          cv2.circle(self.img, (x_ceil, y_ceil), 2, color[i], -1)
          cv2.circle(self.img, (x_floor, y_floor), 2, color[i], -1)

        text = "cell" + str(i)
        font = cv2.FONT_HERSHEY_PLAIN
        point = int(len(cells_all[i]) / 2)
        text_x = int((cells_all[i][point][0][0] + cells_all[i][point][1][0]) / 2)
        text_y = int((cells_all[i][point][0][1] + cells_all[i][point][1][1]) / 2)
        cv2.putText(self.img, text, (text_x, text_y), font, 1, (0, 0, 255), 1, cv2.CV_AA )
      cv2.imwrite("cells.jpg", self.img)
      return cells_all

