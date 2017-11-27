# coding:utf-8
from MinCircleClass import MinCircleClass as mcc

if __name__ == '__main__':
    points = [[22.326033,114.167300],[22.324135,114.170397],[22.325710,114.168983],
              [22.321563,114.160698],[22.319737,114.161184],[22.317973,114.167922],[22.325898,114.168695],
              [22.321571,114.160680],[22.325548,114.166257],[22.319498,114.160996],[22.324556,114.158241],
              [22.322847,114.161497],[22.325049,114.163948],[22.325749,114.169046],[22.321409,114.161641],
              [22.321592,114.160779],[22.309917,114.171168],[22.320922,114.163619],[22.309845,114.171141],
              [22.319426,114.161320],[22.316540,114.169524],[22.316519,114.171693],[22.315718,114.169012],
              [22.324452,114.166395],[22.317070,114.172602],[22.319989,114.161365],[22.318547,114.170503],
              [22.310083,114.170790]]

    mcc = mcc(points,100,1000)
    print (mcc.GetMinCircleR())
    print (mcc.GetDistanceOfTwoPoints(points[0][0],points[0][1],points[1][0],points[1][1]))
