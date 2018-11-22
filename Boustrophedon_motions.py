#!/usr/bin/python
import cv2
import numpy as np 

class boustrophedon_motions:
  #def __init__(self):

  def read_file(self, filename):
      # read map file
      return cv2.imread(filename) # Read an image

  def draw_waypoints(self, waypoints, color):
      for i in range (0, len(waypoints)):
         cv2.circle(self.img, (waypoints[i][0], waypoints[i][1]), 2, color, -1)
         text = str(i)
         font = cv2.FONT_HERSHEY_PLAIN
         #cv2.putText(self.img, text, (waypoints[i][0], waypoints[i][1]), font, 1, color, 1) 

  def draw_sweepinglines(self, waypoints, color):
      for i in range (0, len(waypoints) - 1):
         cv2.line(self.img, (waypoints[i][0], waypoints[i][1]), (waypoints[i + 1][0], waypoints[i + 1][1]), color, 1, cv2.CV_AA) 


  def percell_motions(self, footprint, eulerian_list, eulerian_cells, diameter, m_position, mapfile):
      f = footprint
      self.img = self.read_file(mapfile)
      n_cells = eulerian_cells.shape[0]
      color = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 0, 0), (0, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255) ]

      cell_waypoints = tuple([] for m in range (int(n_cells)))
      cell_waypoints_m1 = tuple([] for m in range (int(n_cells)))
      cell_waypoints_m2 = tuple([] for m in range (int(n_cells)))
      for i in range (0, n_cells):
        L = len(eulerian_cells[i])
        direction = eulerian_cells[i][L - 1]
        vertices = eulerian_cells[i][L - 2]
        i_start = eulerian_cells[i][0][0][0]
        i_end = eulerian_cells[i][L - 3][0][0]
        cell_width = i_end - i_start
        n_sweepiglines = int(cell_width / f)
        f_half = int(f / 2)
        sweepingline_list = []
        for j in range (0, n_sweepiglines):
          sweepingline_list.append(f_half * (2 * j + 1))
        waypoints = []
        waypoints_m1 = []
        waypoints_m2 = []
        if direction == 1:
          start_point = ((eulerian_cells[i][0][1][0]), (eulerian_cells[i][0][1][1]))
          for j in range (0, len(sweepingline_list)):
            i_line = sweepingline_list[j] 
            if (j % 2 != 0):
              if j == len(sweepingline_list) :
                mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][0][1])))
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][1][1] + mid)))
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][1][1])))

                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][0][1])))
                waypoints_m1.append(((i_start + i_line - m_position + int(diameter/3) ) , (eulerian_cells[i][i_line][0][1])))
                waypoints_m1.append(((i_start + i_line - m_position + int(2*diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position + int(diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(2*diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][0][1])))
                #waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line ][1][1] + mid)))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][1][1])))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line ][1][1])))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][0][1])))
                waypoints_m2.append(((i_start + i_line + m_position + int(diameter/3) ) , (eulerian_cells[i][i_line][0][1])))
                waypoints_m2.append(((i_start + i_line + m_position + int(2*diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position + int(diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(2*diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][0][1])))
                #waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1] + mid)))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1])))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1])))
              
              else:
                mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][0][1])))
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][1][1] + mid)))
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][1][1])))

                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][0][1])))
                waypoints_m1.append(((i_start + i_line - m_position + int(diameter/3) ) , (eulerian_cells[i][i_line][0][1])))
                waypoints_m1.append(((i_start + i_line - m_position + int(2*diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position + int(diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(2*diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][0][1] )))
                #waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line ][1][1] + mid)))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][1][1] )))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][1][1] + int(diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position - int(diameter/3) ) , (eulerian_cells[i][i_line][1][1] + int(2*diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position - int(2*diameter/3) ) , (eulerian_cells[i][i_line][1][1] + int(diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line ][1][1])))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][0][1])))
                waypoints_m2.append(((i_start + i_line + m_position + int(diameter/3) ) , (eulerian_cells[i][i_line][0][1])))
                waypoints_m2.append(((i_start + i_line + m_position + int(2*diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position + int(diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(2*diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][0][1])))
                #waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1] + mid)))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1])))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1] + int(diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position - int(diameter/3) ) , (eulerian_cells[i][i_line][1][1] + int(2*diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position - int(2*diameter/3) ) , (eulerian_cells[i][i_line][1][1] + int(diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1] )))

            if (j % 2 == 0):
              if j == 0:
                mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][1][1])))
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][1][1] + mid)))
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][0][1])))

                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][1][1] )))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][1][1] )))
                #waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][1][1] + mid)))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][0][1] )))
                waypoints_m1.append(((i_start + i_line - m_position ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position - int(diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(2*diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position - int(2*diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][0][1])))

                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1])))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1])))
                #waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1] + mid)))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][0][1])))
                waypoints_m2.append(((i_start + i_line + m_position ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position - int(diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(2*diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position - int(2*diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][0][1])))


              else:
                mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][1][1])))
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][1][1] + mid)))
                waypoints.append(((i_start + i_line) , (eulerian_cells[i][i_line][0][1])))

                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][1][1])))
                waypoints_m1.append(((i_start + i_line - m_position + int(diameter/3)) , (eulerian_cells[i][i_line][1][1] )))
                waypoints_m1.append(((i_start + i_line - m_position + int(2*diameter/3)) , (eulerian_cells[i][i_line][1][1] + int(diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position + int(diameter/3)) , (eulerian_cells[i][i_line][1][1] + int(2*diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][1][1])))
                #waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][1][1] + mid)))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][0][1])))
                waypoints_m1.append(((i_start + i_line - m_position ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position - int(diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(2*diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position - int(2*diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m1.append(((i_start + i_line - m_position) , (eulerian_cells[i][i_line][0][1] )))

                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1] )))
                waypoints_m2.append(((i_start + i_line + m_position + int(diameter/3)) , (eulerian_cells[i][i_line][1][1])))
                waypoints_m2.append(((i_start + i_line + m_position + int(2*diameter/3) ) , (eulerian_cells[i][i_line][1][1] + int(diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position + int(diameter/3) ) , (eulerian_cells[i][i_line][1][1] + int(2*diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1])))
                #waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][1][1] + mid)))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][0][1] )))
                waypoints_m2.append(((i_start + i_line + m_position ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position - int(diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(2*diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position - int(2*diameter/3) ) , (eulerian_cells[i][i_line][0][1] - int(diameter/3))))
                waypoints_m2.append(((i_start + i_line + m_position) , (eulerian_cells[i][i_line][0][1])))

          if (len(sweepingline_list) % 2 == 0):
              mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
              waypoints.append((i_end - f_half , (eulerian_cells[i][L - 3 - f_half][1][1] )))
              waypoints.append((i_end - f_half, (eulerian_cells[i][L - 3 - f_half][1][1] + mid)))
              waypoints.append((i_end - f_half, (eulerian_cells[i][L - 3 - f_half][0][1])))

              waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] )))
              waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(2*diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position + int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] )))
              #waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] + mid)))
              waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][0][1] )))
              waypoints_m1.append(((i_end - f_half - m_position ) , (eulerian_cells[i][L - 3 - f_half][0][1] - int(diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position - int(diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][0][1] - int(2*diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position - int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][0][1]  - int(diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][0][1])))

              waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] )))
              waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(2*diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position + int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][1][1])))
              #waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] + mid)))
              waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][0][1])))
              waypoints_m2.append(((i_end - f_half + m_position ) , (eulerian_cells[i][L - 3 - f_half][0][1] - int(diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position - int(diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][0][1] - int(2*diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position - int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][0][1] - int(diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][0][1])))


          if (len(sweepingline_list) % 2 != 0):
              mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
              waypoints.append((i_end - f_half, (eulerian_cells[i][L - 3 - f_half][0][1] )))
              waypoints.append((i_end - f_half, (eulerian_cells[i][L - 3 - f_half][1][1] + mid)))
              waypoints.append((i_end - f_half, (eulerian_cells[i][L - 3 - f_half][1][1] )))

              waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][0][1] )))
              waypoints_m1.append(((i_end - f_half - m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][0][1])))
              waypoints_m1.append(((i_end - f_half - m_position + int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][0][1] - int(diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][0][1] - int(2*diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][0][1] )))
              #waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half ][1][1] + mid)))
              waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] )))
              waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position - int(diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(2*diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position - int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(diameter/3))))
              waypoints_m1.append(((i_end - f_half - m_position) , (eulerian_cells[i][L - 3 - f_half][1][1])))
              waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][0][1])))
              waypoints_m2.append(((i_end - f_half + m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][0][1])))
              waypoints_m2.append(((i_end - f_half + m_position + int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][0][1] - int(diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][0][1] - int(2*diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][0][1])))
              #waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] + mid)))
              waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][1][1])))
              waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position - int(diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(2*diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position - int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - f_half][1][1] + int(diameter/3))))
              waypoints_m2.append(((i_end - f_half + m_position) , (eulerian_cells[i][L - 3 - f_half][1][1])))
            

        if direction == -1:
          start_point = ((eulerian_cells[i][L - 3][0][0] - f_half), (eulerian_cells[i][L - 3][0][1] + f_half))
          for j in range (0, len(sweepingline_list)):
            i_line = sweepingline_list[j] 
            if (j % 2 != 0):
              mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
              waypoints.append(((i_end - i_line) , (eulerian_cells[i][L - 3 - i_line][1][1] )))
              waypoints.append(((i_end - i_line) , (eulerian_cells[i][L - 3 - i_line][0][1] - mid)))
              waypoints.append(((i_end - i_line) , (eulerian_cells[i][L - 3 - i_line][0][1] )))

              waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][1][1])))
              waypoints_m1.append(((i_end - i_line + m_position - int(diameter/3)) , (eulerian_cells[i][L - 3 - i_line][1][1])))
              waypoints_m1.append(((i_end - i_line + m_position - int(2* diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(diameter/3))))
              waypoints_m1.append(((i_end - i_line + m_position - int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(2*diameter/3))))
              waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] )))
              #waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] + mid)))
              waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][0][1] )))
              waypoints_m1.append(((i_end - i_line + m_position ) , (eulerian_cells[i][L - 3 - i_line][0][1]- int(diameter/3))))
              waypoints_m1.append(((i_end - i_line + m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][0][1]  - int(2*diameter/3))))
              waypoints_m1.append(((i_end - i_line + m_position + int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][0][1]  - int(diameter/3))))
              waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][0][1] )))

              waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] )))
              waypoints_m2.append(((i_end - i_line - m_position - int(diameter/3)) , (eulerian_cells[i][L - 3 - i_line][1][1] )))
              waypoints_m2.append(((i_end - i_line - m_position - int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(diameter/3))))
              waypoints_m2.append(((i_end - i_line - m_position - int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(2*diameter/3))))
              waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] )))
              #waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] + mid)))
              waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][0][1] )))
              waypoints_m2.append(((i_end - i_line - m_position ) , (eulerian_cells[i][L - 3 - i_line][0][1] - int(diameter/3))))
              waypoints_m2.append(((i_end - i_line - m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][0][1] - int(2*diameter/3))))
              waypoints_m2.append(((i_end - i_line - m_position + int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][0][1] - int(diameter/3))))
              waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][0][1])))


            if (j % 2 == 0):
              if j == 0:
                mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
                waypoints.append(((i_end - i_line) , (eulerian_cells[i][L - 3 - i_line][0][1])))
                waypoints.append(((i_end - i_line) , (eulerian_cells[i][L - 3 - i_line][0][1] - mid)))
                waypoints.append(((i_end - i_line) , (eulerian_cells[i][L - 3 - i_line][1][1])))

                waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][0][1] )))
                waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] )))
                waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][1][1]  + int(diameter/3))))
                waypoints_m1.append(((i_end - i_line + m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1]  + int(2*diameter/3))))
                waypoints_m1.append(((i_end - i_line + m_position + int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1]  + int(diameter/3))))
                waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] )))

                waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][0][1] )))
                
                waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] )))
                waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(diameter/3))))
                waypoints_m2.append(((i_end - i_line - m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(2*diameter/3))))
                waypoints_m2.append(((i_end - i_line - m_position + int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(diameter/3))))
                waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][1][1])))

              else:
                mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
                waypoints.append(((i_end - i_line) , (eulerian_cells[i][L - 3 - i_line][0][1])))
                waypoints.append(((i_end - i_line) , (eulerian_cells[i][L - 3 - i_line][0][1] - mid)))
                waypoints.append(((i_end - i_line) , (eulerian_cells[i][L - 3 - i_line][1][1])))

                waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][0][1])))
                waypoints_m1.append(((i_end - i_line + m_position - int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][0][1])))
                waypoints_m1.append(((i_end - i_line + m_position - int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][0][1] - int(diameter/3))))
                waypoints_m1.append(((i_end - i_line + m_position - int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][0][1] - int(2*diameter/3))))
                waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][0][1])))
                #waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][0][1] + mid)))
                waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] )))
                waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(diameter/3))))
                waypoints_m1.append(((i_end - i_line + m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(2*diameter/3))))
                waypoints_m1.append(((i_end - i_line + m_position + int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(diameter/3))))
                waypoints_m1.append(((i_end - i_line + m_position) , (eulerian_cells[i][L - 3 - i_line][1][1])))

                waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][0][1] )))
                waypoints_m2.append(((i_end - i_line - m_position - int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][0][1])))
                waypoints_m2.append(((i_end - i_line - m_position - int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][0][1]  - int(diameter/3))))
                waypoints_m2.append(((i_end - i_line - m_position - int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][0][1] - int(2*diameter/3))))
                waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][0][1] )))
                #waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][0][1] + mid)))
                waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][1][1] )))
                waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][1][1]  + int(diameter/3))))
                waypoints_m2.append(((i_end - i_line - m_position + int(diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(2*diameter/3))))
                waypoints_m2.append(((i_end - i_line - m_position + int(2*diameter/3) ) , (eulerian_cells[i][L - 3 - i_line][1][1] + int(diameter/3))))
                waypoints_m2.append(((i_end - i_line - m_position) , (eulerian_cells[i][L - 3 - i_line][1][1])))


          if (len(sweepingline_list) % 2 == 0):
              mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
              waypoints.append((i_start + f_half, (eulerian_cells[i][0 + f_half][0][1])))
              waypoints.append((i_start + f_half, (eulerian_cells[i][0 + f_half][0][1] - mid)))
              waypoints.append((i_start + f_half, (eulerian_cells[i][0 +  f_half][1][1])))

              waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][0][1])))
              waypoints_m1.append(((i_start + f_half + m_position - int(diameter/3) ) , (eulerian_cells[i][0 + f_half][0][1])))
              waypoints_m1.append(((i_start + f_half + m_position - int(2*diameter/3) ) , (eulerian_cells[i][0 + f_half][0][1] - int(diameter/3))))
              waypoints_m1.append(((i_start + f_half + m_position - int(diameter/3) ) , (eulerian_cells[i][0 + f_half][0][1] - int(2*diameter/3))))
              waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][0][1])))
              #waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][0][1] + mid)))
              waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][1][1])))
              waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][1][1] + int(diameter/3))))
              waypoints_m1.append(((i_start + f_half + m_position + int(diameter/3) ) , (eulerian_cells[i][0 + f_half][1][1] + int(2*diameter/3))))
              waypoints_m1.append(((i_start + f_half + m_position + int(2*diameter/3) ) , (eulerian_cells[i][0 + f_half][1][1] + int(diameter/3))))
              waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][1][1])))

              waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][0][1])))
              waypoints_m2.append(((i_start + f_half - m_position - int(diameter/3) ) , (eulerian_cells[i][0 + f_half][0][1])))
              waypoints_m2.append(((i_start + f_half - m_position - int(2*diameter/3) ) , (eulerian_cells[i][0 + f_half][0][1] - int(diameter/3))))
              waypoints_m2.append(((i_start + f_half - m_position - int(diameter/3) ) , (eulerian_cells[i][0 + f_half][0][1] - int(2*diameter/3))))
              waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][0][1] )))
              #waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][0][1] + mid)))
              waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][1][1])))
              waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][1][1] + int(diameter/3))))
              waypoints_m2.append(((i_start + f_half - m_position + int(diameter/3) ) , (eulerian_cells[i][0 + f_half][1][1] + int(2*diameter/3))))
              waypoints_m2.append(((i_start + f_half - m_position + int(2*diameter/3) ) , (eulerian_cells[i][0 + f_half][1][1] + int(diameter/3))))
              waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][1][1])))

          if (len(sweepingline_list) % 2 != 0):
              mid = (eulerian_cells[i][i_line][0][1] - eulerian_cells[i][i_line][1][1])/2
              waypoints.append((i_start + f_half, (eulerian_cells[i][0 + f_half][1][1] )))
              waypoints.append((i_start + f_half, (eulerian_cells[i][0 + f_half][0][1] - mid)))
              waypoints.append((i_start + f_half, (eulerian_cells[i][0 + f_half][0][1])))

              waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][1][1])))
              waypoints_m1.append(((i_start + f_half + m_position - int(diameter/3)) , (eulerian_cells[i][0 + f_half][1][1])))
              waypoints_m1.append(((i_start + f_half + m_position - int(2* diameter/3) ) , (eulerian_cells[i][0 + f_half][1][1] + int(diameter/3))))
              waypoints_m1.append(((i_start + f_half + m_position - int(diameter/3) ) , (eulerian_cells[i][0 + f_half][1][1] + int(2*diameter/3))))
              waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][1][1])))
              #waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][1][1] + mid)))
              waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][0][1])))
              waypoints_m1.append(((i_start + f_half + m_position ) , (eulerian_cells[i][0 + f_half][0][1] - int(diameter/3))))
              waypoints_m1.append(((i_start + f_half + m_position + int(diameter/3) ) , (eulerian_cells[i][0 + f_half][0][1] - int(2*diameter/3))))
              waypoints_m1.append(((i_start + f_half + m_position + int(2*diameter/3) ) , (eulerian_cells[i][0 + f_half][0][1] - int(diameter/3))))
              waypoints_m1.append(((i_start + f_half + m_position) , (eulerian_cells[i][0 + f_half][0][1] )))

              waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][1][1] )))
              waypoints_m2.append(((i_start + f_half - m_position - int(diameter/3)) , (eulerian_cells[i][0 + f_half][1][1] )))
              waypoints_m2.append(((i_start + f_half - m_position - int(2*diameter/3) ) , (eulerian_cells[i][0 + f_half][1][1] + int(diameter/3))))
              waypoints_m2.append(((i_start + f_half - m_position - int(diameter/3) ) , (eulerian_cells[i][0 + f_half][1][1] + int(2*diameter/3))))
              waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][1][1])))
              #waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][1][1] + mid)))
              waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][0][1])))
              waypoints_m2.append(((i_start + f_half - m_position ) , (eulerian_cells[i][0 + f_half][0][1] - int(diameter/3))))
              waypoints_m2.append(((i_start + f_half - m_position + int(diameter/3) ) , (eulerian_cells[i][0 + f_half][0][1] - int(2*diameter/3))))
              waypoints_m2.append(((i_start + f_half - m_position + int(2*diameter/3) ) , (eulerian_cells[i][0 + f_half][0][1] - int(diameter/3))))
              waypoints_m2.append(((i_start + f_half - m_position) , (eulerian_cells[i][0 + f_half][0][1])))
        
        #print np.array(waypoints)
        self.draw_waypoints(waypoints, (0,165,255))
        self.draw_sweepinglines(waypoints, (0,165,255))

        #self.draw_waypoints(waypoints_m1, color[i + 1])
        #self.draw_sweepinglines(waypoints_m1, (0, 255, 0))

        #self.draw_waypoints(waypoints_m2, color[i + 2])
        #self.draw_sweepinglines(waypoints_m2, (0, 0, 255))

        cell_waypoints[i].append(waypoints)
        cell_waypoints_m1[i].append(waypoints_m1)
        cell_waypoints_m2[i].append(waypoints_m2)
     
      cell_waypoints_array = np.array(cell_waypoints)
      cell_waypoints_m1_array = np.array(cell_waypoints_m1)
      cell_waypoints_m2_array = np.array(cell_waypoints_m2)
      print cell_waypoints_array
      self.between_cell_motions(cell_waypoints_array)
      #self.between_cell_motions(cell_waypoints_m1_array)
      #self.between_cell_motions(cell_waypoints_m2_array)
      cv2.imwrite("waypoints_fleet.jpg", self.img)
      return cell_waypoints_array, cell_waypoints_m1_array, cell_waypoints_m2_array

  def between_cell_motions(self, cell_waypoints):
      for i in range (0, cell_waypoints.shape[0] - 1):
        L = int(len(cell_waypoints[i][0]))
        #print L
        cv2.line(self.img, (cell_waypoints[i][0][L - 1][0], cell_waypoints[i][0][L - 1][1]), (cell_waypoints[i + 1][0][0][0], cell_waypoints[i + 1][0][0][1]), (0, 0, 0), 1)
     
              
 
        
