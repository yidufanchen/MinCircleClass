# coding:utf-8

import os
import math

class MinCircleClass():
    def __init__(self,points = [],reDrawTimes = 50,fiterCounts = 10000):
        '''

        :param points: the set of points
        :param reDrawTimes: number of draws
        :param fiterCounts: need to obtain the minimum critical value of circumcircle
        '''
        self.points = points
        self.reDrawTimes = reDrawTimes
        self.fiterCounts = fiterCounts


    def GetMinCircleR(self):
        '''
        Get the smallest circumcircle
        :return:
        '''
        if len(self.points)==0:
            return [],None
        if len(self.points)==1:
            return self.points[0],0
        maxminll,centerll,circleR = self.GetFirstLLCenter()
        firstcirclell = centerll
        firstoutofpointdis = 0
        rescircleR = circleR
        rescenterll = centerll
        lastoutofpoint = []

        times = 0
        endflag = False
        while True:
            times += 1
            outcirclell,maxdistance = self.GetOutOfCirclePoint(centerll,circleR)
            if times==1:
                firstoutofpointdis = maxdistance
            if len(outcirclell)==1:
                if times>1:
                    maxminll1 = [[lastoutofpoint[0][0],lastoutofpoint[0][1]],[maxminll[0][0],maxminll[0][1]]]
                    newCenterx1,newCentery1,circleR1 = self.ReDrawCircle(maxminll1,outcirclell)
                    maxminll2 = [[lastoutofpoint[0][0],lastoutofpoint[0][1]],[maxminll[1][0],maxminll[1][1]]]
                    newCenterx2,newCentery2,circleR2 = self.ReDrawCircle(maxminll2,outcirclell)
                    if circleR1>circleR2:
                        newCenterx,newCentery,circleR = newCenterx2,newCentery2,circleR2
                    else:
                        newCenterx,newCentery,circleR = newCenterx1,newCentery1,circleR1
                    if times>self.reDrawTimes:
                        # print "Deal Times > 50 "
                        newCenterx,newCentery,circleR = firstcirclell[0],firstcirclell[1],firstoutofpointdis
                        rescenterll = (newCenterx,newCentery)
                        rescircleR = circleR
                        break
                else:
                    newCenterx,newCentery,circleR = self.ReDrawCircle(maxminll,outcirclell)

                if newCentery=='END':
                    endflag = True
                    break
                centerll = (newCenterx,newCentery)
                if endflag==False:
                    rescenterll = (newCenterx,newCentery)
                    rescircleR = circleR
                lastoutofpoint = outcirclell
            else:
                break
        return rescenterll,rescircleR


    def GetDistanceOfTwoPoints(self,lat1,lng1,lat2,lng2):
        '''
        Get the distance between two points on Earth
        :param lat1: first point latitude
        :param lng1: first point longitude
        :param lat2: second point latitude
        :param lng2: second point longitude
        :return: the distance of two points
        '''
        R = 6378.137  # earth radius in meters
        d2r = math.pi/180.0
        dLat = (lat2-lat1) * d2r
        dLon = (lng2-lng1) * d2r
        lat1 = lat1 * d2r
        lat2 = lat2 * d2r
        sin1 = math.sin(dLat/2)
        sin2 = math.sin(dLon/2)
        a = sin1 * sin1+sin2 * sin2 * math.cos(lat1) * math.cos(lat2)
        distance = R * 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
        if distance<0:
            distance = -distance
        distance = float("%.8f" % distance)
        return distance

    def FilterPoints(self):
        '''
        Get the circumscribed rectangle
        :return: the points of rectangular edge
        '''
        self.points.sort(key=lambda x:x[0])
        point1 = [self.points[0],self.points[-1]]
        self.points.sort(key=lambda x:x[1])
        point2 = [self.points[0],self.points[-1]]
        point1.extend(point2)
        return point1

    def GetFirstLLCenter(self):
        '''
        Set points for the initial two-point positioning center,
        and return to the maximum distance of two coordinates,
        the coordinates of the center circle radius
        :param points:
        :return:
        '''
        points = self.points.copy()
        if len(self.points)>self.fiterCounts:
            points = self.FilterPoints()
        maxdistance = 0
        maxminll = [0,0]
        for indexi,point in enumerate(points):
            lat1 = points[indexi][0]
            lon1 = points[indexi][1]
            indexj = indexi+1
            while indexj<len(points):
                lat2 = points[indexj][0]
                lon2 = points[indexj][1]
                distance = self.GetDistanceOfTwoPoints(lat1,lon1,lat2,lon2)
                if distance>=maxdistance:
                    maxdistance = distance
                    maxminll = [(lat1,lon1),(lat2,lon2)]
                indexj = indexj+1
        lat,lon = self.GetCenterOf2Point(maxminll[0][0],maxminll[0][1],maxminll[1][0],maxminll[1][1])

        centerll = (lat,lon)
        circleR = self.GetDistanceOfTwoPoints(centerll[0],centerll[1],maxminll[1][0],maxminll[1][1])
        return maxminll,centerll,circleR

    def DoExchangeValue(self,lat1,lon1,lat2,lon2):
        '''
        Exchange the two points position
        :param lat1: first point latitude
        :param lng1: first point longitude
        :param lat2: second point latitude
        :param lng2: second point longitude
        :return: the exchanged position of two points
        '''
        lat1 = lat1+lat2
        lon1 = lon1+lon2
        lat2 = lat1-lat2
        lon2 = lon1-lon2
        lat1 = lat1-lat2
        lon1 = lon1-lon2
        return lat1,lon1,lat2,lon2

    def GetCenterOf2Point(self,lat1,lon1,lat2,lon2):
        '''
        Gets the distance between the two points with the largest distance in the points
        as the diameter of the circle and returns the coordinates of the center of the circle
        :param lat1: first point latitude
        :param lng1: first point longitude
        :param lat2: second point latitude
        :param lng2: second point longitude
        :return: the center of two points
        '''
        d2r = math.pi/180.0
        if lon2-lon1<0:
            lat1,lon1,lat2,lon2 = self.DoExchangeValue(lat1,lon1,lat2,lon2)
        dLon = (lon2-lon1) * d2r
        dLon = abs(dLon)
        lat1 = lat1 * d2r
        lat2 = lat2 * d2r
        lon1 = lon1 * d2r
        bx = math.cos(lat2) * math.cos(dLon)
        by = math.cos(lat2) * math.sin(dLon)
        lat3 = math.atan2(math.sin(lat1)+math.sin(lat2),math.sqrt((math.cos(lat1)+bx) * (math.cos(lat1)+bx)+by * by))
        lon3 = lon1+math.atan2(by,math.cos(lat1)+bx)
        return lat3/d2r,lon3/d2r

    def GetCenterOf3Point(self,lat1,lon1,lat2,lon2,lat3,lon3):
        '''
        Get the center of three points
        :param lat1: first point latitude
        :param lng1: first point longitude
        :param lat2: second point latitude
        :param lng2: second point longitude
        :param lat3: third point latitude
        :param lon3: third point longitude
        :return: the center of three points
        '''
        flag = True
        times = 0
        d2r = math.pi/180.0
        lat1 = lat1 * d2r
        lat2 = lat2 * d2r
        lat3 = lat3 * d2r
        lon1 = lon1 * d2r
        lon2 = lon2 * d2r
        lon3 = lon3 * d2r

        while flag:
            times += 1
            x1 = math.cos(lat1) * math.cos(lon1)
            y1 = math.sin(lon1) * math.cos(lat1)
            z1 = math.sin(lat1)
            x2 = math.cos(lat2) * math.cos(lon2)
            y2 = math.sin(lon2) * math.cos(lat2)
            z2 = math.sin(lat2)
            x3 = math.cos(lat3) * math.cos(lon3)
            y3 = math.sin(lon3) * math.cos(lat3)
            z3 = math.sin(lat3)
            N = ((y2-y1) * (z3-z1)-(z2-z1) * (y3-y1),
                 (z2-z1) * (x3-x1)-(x2-x1) * (z3-z1),
                 (x2-x1) * (y3-y1)-(y2-y1) * (x3-x1))
            r = math.sqrt(N[0] * N[0]+N[1] * N[1]+N[2] * N[2])
            if r!=0.0:
                centerlat = math.asin(N[2]/r)
                centerlon = math.atan2(N[1],N[0])
                newdistance = self.GetDistanceOfTwoPoints(centerlat/d2r,centerlon/d2r,lat3/d2r,lon3/d2r)
                olddistance = self.GetDistanceOfTwoPoints(lat1/d2r,lon1/d2r,lat3/d2r,lon3/d2r)
                if newdistance>olddistance:
                    if times==1:
                        lat1,lon1,lat2,lon2 = self.DoExchangeValue(lat1,lon1,lat2,lon2)
                    elif times==2:
                        lat1,lon1,lat3,lon3 = self.DoExchangeValue(lat1,lon1,lat3,lon3)
                    elif times==3:
                        lat2,lon2,lat3,lon3 = self.DoExchangeValue(lat2,lon2,lat3,lon3)
                    else:
                        flag = False
                    continue
                return centerlat/d2r,centerlon/d2r
            else:
                return "END","END"
        return "END","END"

    def GetOutOfCirclePoint(self,centerll,circleR):
        '''
        Get the farthest point from the center of the circle
        :param centerll: the center of the circle
        :param circleR: the radius of the circle
        :return: the farthest point from the center of the circle and the distance
        '''
        lat1 = centerll[0]
        lon1 = centerll[1]
        maxdistance = circleR
        outcirclell = []
        for point in self.points:
            lat2 = point[0]
            lon2 = point[1]
            distance = self.GetDistanceOfTwoPoints(lat1,lon1,lat2,lon2)
            if distance>maxdistance:
                maxdistance = distance
                outcirclell = [point]
        return outcirclell,maxdistance

    def ReDrawCircle(self,maxminll,outcirclell):
        '''

        :param maxminll:
        :param outcirclell: the point of outside circle
        :return: new center and new radius
        '''
        newCenterx,newCentery = self.GetCenterOf3Point(maxminll[0][0],maxminll[0][1],maxminll[1][0],maxminll[1][1],
                                                  outcirclell[0][0],outcirclell[0][1])
        if newCenterx!="END":
            circleR = self.GetDistanceOfTwoPoints(newCenterx,newCentery,outcirclell[0][0],outcirclell[0][1])
            circleR1 = self.GetDistanceOfTwoPoints(newCenterx,newCentery,maxminll[0][0],maxminll[0][1])
            circleR2 = self.GetDistanceOfTwoPoints(newCenterx,newCentery,maxminll[1][0],maxminll[1][1])
            circleR = max(circleR,circleR1)
            circleR = max(circleR,circleR2)
            return newCenterx,newCentery,circleR
        else:
            return "END","END","END"
