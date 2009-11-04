#Copyright (c) 2009, Walter Bender

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from sprites import *
from card import *

CARD_DEFS = ((1,3,-2,-3),(2,3,-3,-2),(2,3,-4,-4),
             (2,1,-1,-4),(3,4,-4,-3),(4,2,-1,-2),
             (1,1,-2,-4),(4,2,-3,-4),(1,3,-1,-2))


#
# class for defining 3x3 matrix of cards
#
class Grid:
    # 012
    # 345
    # 678
    def __init__(self, tw):
        self.grid = [0,1,2,3,4,5,6,7,8,9]
        self.card_table = {}
        # stuff to keep around for the graphics
        self.w = tw.width
        self.h = tw.height
        self.d = tw.card_dim
        self.s = tw.scale
        # Initialize the cards
        i = 0 # i is used as a label on the sprite
        x = int((self.w-(self.d*3*self.s))/2)
        y = int((self.h-(self.d*3*self.s))/2)
        for c in CARD_DEFS:
            self.card_table[i] = Card(tw,c,i,x,y)
            self.card_table[i].draw_card()
            x += int(self.d*self.s)
            if x > (self.w+(self.d*2*self.s))/2:
                x = int((self.w-(self.d*3*self.s))/2)
                y += int(self.d*self.s)
            i += 1

    # reset everything to initial layout
    def reset3x3(self, tw):
        self.set_grid([0,1,2,3,4,5,6,7,8])
        self.set_orientation([0,0,0,0,0,0,0,0,0])
        for i in range(9):
            self.card_table[i].reload_image(tw, i)

    # TWO_BY_TWO = ((7,5,0,3),(7,4,5,2),(1,3,5,8),(4,5,6,1))
    # reset everything to initial layout
    def reset2x2(self, tw):
        self.set_grid([4,5,0,6,1,2,3,7,8])
        self.set_orientation([0,0,0,0,0,0,0,0,0])
        for i in range(9):
            self.card_table[i].reload_image(tw, i)
        for i in (0,2,3,7,8):
            hide(self.card_table[i].spr)

    # THREE_BY_TWO = ((7,5,0,2,4,3),(5,6,1,4,3,8))
    # reset everything to initial layout
    def reset3x2(self, tw):
        self.set_grid([7,5,0,2,4,3,1,6,8])
        self.set_orientation([0,0,0,0,0,0,0,0,0])
        for i in range(9):
            self.card_table[i].reload_image(tw, i)
        for i in (1,6,8):
            hide(self.card_table[i].spr)

    # TWO_BY_THREE = ((5,2,4,6,1,7),(7,1,2,5,8,0))
    # reset everything to initial layout
    def reset2x3(self, tw):
        self.set_grid([5,2,0,4,6,3,1,7,8])
        self.set_orientation([0,0,0,0,0,0,0,0,0])
        for i in range(9):
            self.card_table[i].reload_image(tw, i)
        for i in (0,3,8):
            hide(self.card_table[i].spr)

    # force a specific layout
    def set_grid(self, newgrid):
        x = int((self.w-(self.d*3*self.s))/2)
        y = int((self.h-(self.d*3*self.s))/2)
        for c in newgrid:
            for i in range(9):
                if self.card_table[i].spr.label == c:
                    self.card_table[i].spr.x = x
                    self.card_table[i].spr.y = y
                    self.card_table[i].draw_card()
            x += int(self.d*self.s)
            if x > (self.w+(self.d*2*self.s))/2:
                x = int((self.w-(self.d*3*self.s))/2)
                y += int(self.d*self.s)

    def set_orientation(self, neworientation):
        for c in range(9):
            self.card_table[c].set_orientation(neworientation[c],True)
            self.card_table[c].draw_card()

    # swap card a and card b
    # swap their entries in the grid and the position of their sprites
    def swap(self, a, b):
        self.print_grid()
        print a, b
        # swap grid elements and x,y positions of sprites
        # print "swapping cards " + str(a) + " and " + str(b)
        ai = self.grid.index(a)
        bi = self.grid.index(b)
        self.grid[bi] = a
        self.grid[ai] = b
        x = self.card_table[a].spr.x
        y = self.card_table[a].spr.y
        self.card_table[a].spr.x = self.card_table[b].spr.x
        self.card_table[a].spr.y = self.card_table[b].spr.y
        self.card_table[b].spr.x = x
        self.card_table[b].spr.y = y

    # print the grid
    def print_grid(self):
        print self.grid[0:3]
        print self.grid[3:6]
        print self.grid[6:9]
        return

    # print the grid orientations
    def print_orientations(self):
        print self.card_table[self.grid[0]].orientation,\
              self.card_table[self.grid[1]].orientation,\
              self.card_table[self.grid[2]].orientation 
        print self.card_table[self.grid[3]].orientation,\
              self.card_table[self.grid[4]].orientation,\
              self.card_table[self.grid[5]].orientation 
        print self.card_table[self.grid[6]].orientation,\
              self.card_table[self.grid[7]].orientation,\
              self.card_table[self.grid[8]].orientation 
        return

    # test all relevant borders, ignoring borders on the blank card
    def test3x3(self):
        for i in (0,1,3,4,6,7):
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i+1]].west != 0:
                return False
        for i in (0,1,2,3,4,5):
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i+3]].north != 0:
                return False
        return True

    # test all relevant borders, ignoring borders on the blank card
    def test2x3(self):
        for i in (0,3,6):
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i+1]].west != 0:
                return False
        for i in (0,1,3,4):
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i+3]].north != 0:
                return False
        return True

    # test all relevant borders, ignoring borders on the blank card
    def test3x2(self):
        for i in (0,1,3,4):
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i+1]].west != 0:
                return False
        for i in (0,1,2):
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i+3]].north != 0:
                return False
        return True

    # test all relevant borders, ignoring borders on the blank card
    def test2x2(self):
        for i in (0,3):
            if self.card_table[self.grid[i]].east + \
               self.card_table[self.grid[i+1]].west != 0:
                return False
        for i in (0,1):
            if self.card_table[self.grid[i]].south + \
               self.card_table[self.grid[i+3]].north != 0:
                return False
        return True

