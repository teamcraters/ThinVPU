# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 18:36:32 2020

@author: jgetchius
"""

# Dependencies
import cv2
import numpy as np
import copy
from matplotlib import pyplot as plt

# Classes
class ParamsClass:
    # This replicates the iloads
    def __init__(self):
        self.light_thresh_mult = 2.0
        self.shadow_thresh_mult = 2.0
        self.max_light_contour_area = 1000.0 * 1000.0
        self.min_light_contour_area = 1.0
        self.max_shadow_contour_area = 1000.0 * 1000.0
        self.min_shadow_contour_area = 1.0
        self.ellipse_frac_threshold = 0.05

class InternalClass:
    # This replicates the FSW functionality
    def __init__(self):
        self.params = ParamsClass()

# Crater detection algorithm
def detectCrater( framec, Internal, u_sun, debug_plots):
    
    # Frame was returned in color, now make it gray scale
    framebw = cv2.cvtColor(framec, cv2.COLOR_BGR2GRAY)
    
    # Let's equalize the histogram
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(11, 11))
    framebw = clahe.apply(framebw)
    
    # Zero out the found features
    found_features = []
    found_features_centers = []
    
    # Compute the mean/std of the frame and threshold it
    meanI = np.mean(framebw)
    stdI = np.std(framebw)

    #Theshold the images and find contours of specular regions    
    ret, frameo = cv2.threshold(framebw, meanI + Internal.params.light_thresh_mult*stdI, 255, cv2.THRESH_BINARY)
    im2, contours_light, hierarchy_l = cv2.findContours(frameo, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter through the contours and keep only viable ones
    contours_light_filtered = []
    for i in contours_light:

        area = cv2.contourArea(i)
        M = cv2.moments(i)
        if debug_plots == True:
            cv2.drawContours(framec, i, -1, (0, 0, 255), 3)
                     
        if M['m00'] != 0:
            if  debug_plots == True:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.drawMarker( framec, (cx, cy), (0, 0, 255))
                        
            if area < Internal.params.max_light_contour_area and area > Internal.params.min_light_contour_area:
                contours_light_filtered.append( i )
                
                
    # Find the shadows -- same as the lights
    ret, frameo = cv2.threshold(framebw, meanI - Internal.params.shadow_thresh_mult*stdI, 255, cv2.THRESH_BINARY_INV)
    im2, contours_shadow, hierarchy_s = cv2.findContours(frameo, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Cycle through the shadows and determine if they are a crater or not...
    for i in contours_shadow:
        
        area = cv2.contourArea( i )
        M = cv2.moments(i)
        
        if debug_plots == True:
            cv2.drawContours(framec, i, -1, (0, 255, 0), 3)
            
            
        if M['m00'] != 0:
            
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

        
            if debug_plots == True:
                cv2.drawMarker(framec, (cx, cy), (0, 255, 0))
            
        if area < Internal.params.max_shadow_contour_area and area > Internal.params.min_shadow_contour_area:
            
            # Make a search circle
            perimeter = cv2.arcLength(i,False)
            rad = int(perimeter / (2.0 + np.pi))
            rad2 = rad**2
            
            # Move the center of the search circle
            xo = int(cx + rad * u_sun[0])
            yo = int(cy + rad * u_sun[1])
            
            if xo > 0 and yo > 0:
            
                if debug_plots == True:
                    cv2.circle(framec, (xo, yo), rad, (255, 255, 0), 2)

                found_light = 0
                mergedCrater = copy.deepcopy(i)
                isacrater = False
                
                # Cycle through the reduced lights and attempt to pair them up
                for j in contours_light_filtered:
                    Ml = cv2.moments(j)
                    if Ml['m00'] > 0:
                        clx = int(Ml['m10']/Ml['m00'])
                        cly = int(Ml['m01']/Ml['m00'])
                    
                    radpt2 = ((clx - xo)**2 + (cly - yo)**2)
                    
                    if radpt2 < rad2:
                        mergedCrater = np.vstack([mergedCrater, j])
                        found_light = 1
                             
                # We have a light and shadow pair!  Check if its a craters
                if found_light == 1:
        
                    # Minimum enclosing circle
                    (x, y), radius = cv2.minEnclosingCircle(mergedCrater)
                    center = (int(x), int(y))
                    radius = int(radius)
                    
                    # Get a convex hull -- which outlines all the features we have
                    # grouped together
                    hull = cv2.convexHull(mergedCrater)
                    hull_list = []
                    hull_list.append(hull)
                    areaCrater = cv2.contourArea(hull)
                    areaCircle = np.pi * radius**2
                    
                    # Compute fraction of area
                    areafrac = areaCrater / areaCircle
                    
                    # Compute circulairty
                    perimeter = cv2.arcLength(hull, True)
                    circularity = 4*np.pi*(areaCrater/(perimeter*perimeter))
                                        
                    if areafrac > Internal.params.area_frac_threshold :   
                        if (circularity > 0.8) and (circularity < 1.2):
                            framec = cv2.circle(framec,center,radius, (0, 255, 0), 5)
                            found_features.append(hull)
                            found_features_centers.append(center)
                            cv2.drawContours(framec, hull_list, -1, (0, 0, 255), 5, 8)
                            isacrater = True
    
    return contours_shadow, contours_light, found_features, found_features_centers



