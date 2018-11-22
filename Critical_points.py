#!/usr/bin/python
import cv2
import numpy as np

class critical_points:
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

  def find_cp(self, bitmap):
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
      #canny_edges = self.laplacian(bitmap)
      
      height, width = bitmap.shape
      print height, width
      
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
            #cv2.circle(self.img, (i,j), 2, (0, 0, 255), -1)                    
        self.p = np.array(points)
        self.s_free = np.array(s_free)
        #print "s is" + str(s)
        #print "s_free is " + str(self.s_free)
                
        filtered_points = []        
        m = 0
        m_next = 0
        m_up = self.p.shape[0]
        while m < m_up:
          #print "m is :" + str(m) 
          neighbors= []
          neighbors.append(self.p[m][1])
          n = m + 1
          if n < m_up:
            while n < m_up:
              #print "n is :" + str(n)
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
          cv2.circle(self.img, (i,neighbors_mean), 2, (0, 255, 255), -1)

        filtered_points_array = np.array(filtered_points)
        self.filtered_points.append(filtered_points)
        #print "candidated cp points for : " + str(i) + "are:" + str(filtered_points_array)

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
            #print "k is :" + str(k) 
            s_neighbors= []
            s_neighbors.append((self.s_free[k][0], self.s_free[k][1], self.s_free[k][2]))
            l = k + 1
            if l < k_up:
              while l < k_up:
                #print "l is :" + str(l)
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
            #print "slice free space count is :" + str(s_free_count)
            grouped_s_neighbors.append(s_neighbors)
          self.grouped_s_free.append(grouped_s_neighbors)
          #print "free space grouped : " + str(i) + "are:" + str(self.grouped_s_free)
        else :
          self.grouped_s_free.append([])

      self.filtered_points_array = np.array(self.filtered_points)
      #print "candidated cp points are: " + str(self.filtered_points_array), self.filtered_points_array.shape[0]
      self.grouped_s_free_array = np.array(self.grouped_s_free)
      #print "grouped free slice are :" + str(self.grouped_s_free_array), self.grouped_s_free_array.shape[0]        
      #print "slice disconectivity count are :" + str(self.s_count), self.s_count.shape[0]
      #print "free slice disconectivity count are :" + str(self.s_free_count), self.s_free_count.shape[0] 
      cv2.imwrite("candidated_cp.jpg", self.img)

     
      cp_start = []
      cp_end = []
      cp_middle = []
      cp = []
      for a in range(0, width):
        #print "a is" + str(a)
        free_space = self.grouped_s_free_array[a]
        #print free_space, len(free_space)
        cp_candidate_end = self.filtered_points_array[a - 1]

        if a == 0:
          if (len(free_space) == 0) :
            if (self.s_count[a] < self.s_count[a + 1]):             
              cp_start.append(self.filtered_points_array[a])
              cp.append(self.filtered_points_array[a])
              cv2.circle(self.img, (a, cp_candidate_start[0][1]), 10, (0, 255, 0), 3)

            if (self.s_count[a] > self.s_count[a + 1]):             
              cp_end.append(self.filtered_points_array[a - 1])
              cp.append(self.filtered_points_array[a - 1])
              cv2.circle(self.img, (a, cp_candidate_end[0][1]), 10, (0, 255, 0), 3)
           
        if a == (width - 1): 
          if (len(free_space) == 0) :
            if (self.s_count[a] > self.s_count[a-1]):            
              cp_start.append(self.filtered_points_array[a])
              cp.append(self.filtered_points_array[a ])
              cv2.circle(self.img, (a, cp_candidate_start[0][1]), 10, (0, 255, 0), 3)

            if (self.s_count[a] < self.s_count[a-1]):             
              cp_end.append(self.filtered_points_array[a - 1])
              cp.append(self.filtered_points_array[a - 1])
              cv2.circle(self.img, (a, cp_candidate_end[0][1]), 10, (0, 255, 0), 3)

        else:               
          if (self.s_free_count[a] < self.s_free_count[a + 1]):  
            #print "I am increasing", len(free_space)
            for e in range (0, len(self.filtered_points_array[a + 1])):
              pp = self.filtered_points_array[a + 1]
              point_p = pp[e][1]
              condition = bitmap[point_p, a]
 
              if ((len(self.filtered_points_array[a]) <= 2) and (len(free_space) != 0) and condition == 0):          
                free_space_a = self.grouped_s_free_array[a + 1]
                #print len(free_space_a), free_space_a
                #print len(self.filtered_points_array[a + 1])
                for b in range(0, len(self.filtered_points_array[a + 1])):
                  p = self.filtered_points_array[a + 1]
                  point = p[b][1]              
                  for c in range(0, len(free_space_a)):
                    free_space_points = []
                    for d in range(0, len(free_space_a[c])):
                      free_space_points.append(free_space_a[c][d][1])
                    free_space_points_array = np.array(free_space_points)
                    #print free_space_points_array
                  
                    f_lo = np.amin(free_space_points_array)
                    f_up = np.amax(free_space_points_array) 
                    #print len(self.filtered_points_array[a + 1]), self.filtered_points_array[a + 1 ]
                    #print f_lo, f_up, point
                    if free_space_points_array.shape[0] <= 2:
                      if (f_lo <= point <= f_up):
                        cp.append(p[b])
                        cv2.circle(self.img, (a, point), 10, (0, 0, 255), 2)                 
                    else:
                      if (f_lo < point < f_up):
                        cp.append(p[b])
                        cv2.circle(self.img, (a, point), 10, (0, 0, 255), 2)

              else:                     
                for b in range(0, len(self.filtered_points_array[a])):
                  p = self.filtered_points_array[a]
                  point = p[b][1]
                  if len(free_space) == 0:
                    if ((self.s_count[a -1 ] < self.s_count[a]) and (self.s_count[a] < self.s_count[a + 1])): 
                      #print "I am here in start increase" + str(point)
                      cp.append(self.filtered_points_array[a][b])
                      cv2.circle(self.img, (self.filtered_points_array[a][b][0], self.filtered_points_array[a][b][1]), 10, (255, 0, 0), 2)
                  else:
                    for c in range(0, len(free_space)):
                      free_space_points = []
                      for d in range(0, len(free_space[c])):
                        free_space_points.append(free_space[c][d][1])
                      free_space_points_array = np.array(free_space_points)
                      #print free_space_points_array
                  
                      f_lo = np.amin(free_space_points_array)
                      f_up = np.amax(free_space_points_array) 
                      #print len(self.filtered_points_array[a]), self.filtered_points_array[a]
                      #print len(self.filtered_points_array[a + 1]), self.filtered_points_array[a + 1]
                      #print f_lo, f_up, point

                      if (f_lo < point < f_up):
                        cp.append(p[b])
                        cv2.circle(self.img, (a, point), 10, (255, 255, 0), 3)


          if (self.s_free_count[a - 1] > self.s_free_count[a]): 
            #print "I am decreasing", len(free_space)
            #print len(self.filtered_points_array[a -1]), self.filtered_points_array[a - 1] 
            for b in range (0, len(self.filtered_points_array[a - 1])):
              p = self.filtered_points_array[a - 1]
              point = p[b][1]
              condition = bitmap[point, a]
 
              if ((len(free_space) != 0) and condition == 0):              
                free_space_a = self.grouped_s_free_array[a - 1]
                #print len(free_space_a), free_space_a
                #print len(self.filtered_points_array[a - 1])
                #for b in range(0, len(self.filtered_points_array[a - 1])):
                #p = self.filtered_points_array[a - 1]
                #point = p[b][1]              
                for c in range(0, len(free_space_a)):
                  free_space_points = []
                  for d in range(0, len(free_space_a[c])):
                    free_space_points.append(free_space_a[c][d][1])
                  free_space_points_array = np.array(free_space_points)
                  #print free_space_points_array
                  
                  f_lo = np.amin(free_space_points_array)
                  f_up = np.amax(free_space_points_array) 
                  #print len(self.filtered_points_array[a - 1]), self.filtered_points_array[a - 1 ]
                  #print f_lo, f_up, point
                  if free_space_points_array.shape[0] <= 2:
                    if (f_lo <= point <= f_up):
                      cp.append(p[b])
                      cv2.circle(self.img, (a-1, point), 10, (0, 0, 255), 2)                 
                  else:
                    if (f_lo < point < f_up):
                      cp.append(p[b])
                      cv2.circle(self.img, (a-1, point), 10, (0, 0, 255), 2)
              else:
                #for b in range(0, len(self.filtered_points_array[a - 1])):                            
                #p = self.filtered_points_array[a - 1]              
                #point = p[b][1]
                if len(free_space) == 0:
                  if ((self.s_count[a] < self.s_count[a - 1]) and (self.s_count[a - 1] > self.s_count[a + 1])): 
                    #print "I am here in end decrease" + str(point)
                    cp.append(self.filtered_points_array[a - 1][b])
                    cv2.circle(self.img, (p[b][0], p[b][1]), 10, (255, 0, 0), 2)                
                else:
                  for c in range(0, len(free_space)):
                    free_space_points = []
                    for d in range(0, len(free_space[c])):
                      free_space_points.append(free_space[c][d][1])
                    free_space_points_array = np.array(free_space_points)
                    if free_space_points_array.shape[0] != 0:
                      f_lo = np.amin(free_space_points_array) 
                      f_up = np.amax(free_space_points_array) 
                      #print free_space_points_array, f_lo, f_up, point
  
                      if ((f_lo < point < f_up) and (f_lo < point < (f_up - 1))):
                        cp.append(p[b])
                        cv2.circle(self.img, (a, point), 10, (0, 255, 0), 3)
                        #print "I am here in middle decrease" + str(point)

      #print "cp start:" + str(cp_start)
      #print "cp end:" + str(cp_end)
      #print "cp middle:" + str(cp_middle)
      #print "cp:" + str(cp)
      cv2.imwrite("cp.jpg", self.img)
      self.cp = np.array(cp)
      #print self.cp
      
      results = []        
      i = 0
      i_next = 0
      i_up = self.cp.shape[0]
      while i < i_up:
        #print "i is :" + str(i) 
        results.append(self.cp[i])
        j = i + 1
        if j < i_up:
          while j < i_up:
            #print "j is :" + str(j)
            condition = ((self.cp[i][0] == self.cp[j][0]) and (self.cp[i][1] == self.cp[j][1]))
            if not condition:
              i_next = j 
              break          
            else :
              i_next = j + 1
            j = j + 1
        else :
          i_next = i + 1
        i = i_next
      #print results
      self.cp = np.array(results)

      return self.cp

       
