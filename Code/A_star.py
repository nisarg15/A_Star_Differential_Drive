import heapq as hq
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import copy

def taking_inputs():

    yi = int(input("Enter y coordinate of start point = "))
    xi = int(input("Enter x coordinate of start point = "))
    thi = int (input("Enter input thetha in degree = "))

    UL = int( input("Enter RPM of left wheel of the bot "))
    UR = int( input("Enter RPM of right whell of the bot"))
    r = 11 # radius of buger turtle bot
    yg = int(input("Enter y coordinate of GOAL point = "))
    xg = int(input("Enter x coordinate of GOAL point = "))
    clearance = int(input("Enter clearance"))
    # thg = int(input("Enter the goal angle for goal point"))

    return xi,yi,xg,yg, thi, r, clearance, UL, UR

def check_condition(img,yi,xi,yg,xg):
    
    if img[yi][xi] == 0:
        print("The start location is on an obstacle kindly re-input the points")
        exit()
    
    if img[yg][xg] == 0:
        print("The goal location is on an obstacle kindly re-input the points")
        exit()
    
    if yi >= 250 or yi <0 :
        print("y coordinate of start point is out of bounds")
        exit()
    
    if yg >= 250 or yg <0 :
        print("y coordinate of goal point is out of bounds")
        exit()
    
    if xi >= 400 or xi < 0:
        print("x coordinate of start point is out of bounds")
        exit()
    
    if xg >= 400 or xg < 0:
        print("x coordinate of goal point is out of bounds")
        exit()
    



def draw_obstacles(r=0):
    data = np.zeros((250,400), dtype=np.uint8)
    data[:,:] = [255]
    
    img = cv2.circle(data, (300,65), 45+r, (0), -1) #drawing a circle as an obstacle

    hex = np.array( [ [200,105-r], [240+r,130], [240+r, 170], [200,195+r], [160-r,170], [160-r,130] ] ) #drawing hexagonal obstacle
    cv2.fillPoly(img, pts =[hex], color=(0))
    
    poly = np.array( [ [33-r,63], [115+r,45-r], [83+r,72], [107+r,152+r] ] ) #drawing polygonal shape as obstacle
    cv2.fillPoly(img, pts =[poly], color=(0))
   
    return img


def allpossiblesteps(Xi,Yi,Thetai, cost2come, xgoal, ygoal,img, actionset):
    steps = []
    y_max = 250
    x_max = 400
    actions=actionset

    r = 3.3   #radius of burger turtle
    L = 16   #length of burger turtle
    dt = 0.1
    
    Xn=Xi
    Yn=Yi
    # Thetan = 3.14 * Thetai / 180  #degree to radian

    for UL , UR in actions:
        t = 0
        D=0
        Xn=Xi
        Yn=Yi
        Thetan = Thetai
        Thetan = 3.14 * Thetai / 180 #radian
        while t<1:
            t = t + dt
            Xs = int(round(Xn,0))
            Ys = int(round(Yn,0))
            
            Delta_Xn = 0.5*r * (UL + UR) * math.cos(Thetan) * dt
            Delta_Yn = 0.5*r * (UL + UR) * math.sin(Thetan) * dt

            Xn = Xn + Delta_Xn
            Yn = Yn - Delta_Yn

            if int(Xn) < x_max-5 and int(Xn) >= 0 and int(Yn) >= 0 and int(Yn) < y_max-5 and img[int(round(Yn,0)),int(round(Xn,0))] == 255:
                cv2.line(img,(Xs,Ys),(int(round(Xn,0)),int(round(Yn,0))), 150, 1)
                cv2.imshow("Animation", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
     
            Thetan = Thetan + (r / L) * (UR - UL) * dt
            # if Thetan < 0:
            #     Thetan = 360 + Thetan

            D=D+ math.sqrt(math.pow((0.5*r * (UL + UR) * math.cos(Thetan) * dt),2)+math.pow((0.5*r * (UL + UR) * math.sin(Thetan) * dt),2))

        degThetan = ((Thetan*180/3.14)/360 - int((Thetan*180/3.14)/360))*360
        
        # srev = (180 * (Thetan) / 3.14)/360
        
        Final_C2C = round(cost2come + D,2)
        
        Xn = int(round(Xn,0))
        Yn = int(round(Yn,0))
        if Xn < x_max and Xn >= 0 and Yn >= 0 and Yn < y_max:
            # cost2go = int (abs(xgoal - Xn ) + abs(ygoal - Yn))
            cost2go = int(math.sqrt((xgoal - Xn )**2 + (ygoal - Yn)**2))
            
            tc = cost2go + Final_C2C
            
            temp = (Yn,Xn,Final_C2C,degThetan,tc)
            # print(temp)
            # print(img[Yn,Xn])
            if img[Yn][Xn] != 0:

                # print("Hello")
                steps.append(temp)
    # print(steps)
    return steps

def backtrack(tup,xi,yi,oq,org_img):
    
    y,x = tup
    ans = []
    
    sum = oq[(y,x)][0]
    sum3 = oq[(y,x)][2]
    ans.append([y,x])
    #print(oq)
    while x!=xi or y!=yi:
        org_img[y][x] = 10
        #print(oq[(y,x)][1])
        #print(y,x)
        y_new, x_new = oq[(y,x)][1]
        ans.append([y_new,x_new])
        cv2.line(org_img,(x,y),(x_new,y_new),140,1)
        y,x = y_new, x_new
    
    print("Total cost : ", sum)
    print("Cost to come : ", sum3)
    print("Backtracking Path from goal point to start point")
    print(ans)

    cv2.imshow("Final Path", org_img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
    # exit()  

salut = 1

def main():

    xi,yi,xg,yg,thi,r,clearance, RPM1, RPM2 = taking_inputs()    
    #radius of the bot is 11cm
    # xi,yi,xg,yg,thi,r, clearance, RPM1, RPM2 = 20,220,390,20, 0, 11 , 5, 7, 14
    
    # RPM1 = 7
    # RPM2 = 14
    action_set = ((0,RPM1),(RPM1,0),(RPM1,RPM1), (0,RPM2), (RPM2,0), (RPM2,RPM2), (RPM1, RPM2), (RPM2,RPM1))
    
    img = draw_obstacles(r+clearance+2)

    check_condition(img,yi,xi,yg,xg)
    
    org_img = draw_obstacles()

    Goal_var = (yg,xg)  #storing goal location
 
    Q = [] #DS to fetch the lowest c2c
    T_C = int(((xg - xi)**2 + (yg - yi)**2)**0.5) + 0
    # T_C = abs(xg - xi) + abs(yg - yi) + 0

    d1 = (T_C,(-1,-1),(yi,xi),thi,0)  #initialised -1 as parents of start point
    hq.heappush(Q, d1)
    hq.heapify(Q)
    
    cq = {} #initialising closed list
    
    oq = {}
    oq[(yi,xi)] = [T_C,[-1,-1],0]  #this can be treated as visited
   
    while Q:
        # print(Q)
        ele = hq.heappop(Q)

        cq[ele[2]] = 1  #adding into the closed queue should include parent as well

        y, x = ele[2]
        angle = ele[3]

        if (xg - x)**2 + (yg - y)**2 <= 8 :        #if the coordinates of current node is near to goal node
            #backtracking, successful return
            # cv2.destroyAllWindows() 
            print("Found")
            backtrack(ele[2],xi,yi,oq,org_img)
            salut = 2
            break

        else:
            # print("Hello")
            total_cost = ele[0]
            cost2come = ele[4]
            #print(cost2come)
            if (y,x) in oq:  #this condition can be removed
                
                if oq[(y,x)][0] < total_cost:
                    total_cost = oq[(y,x)][0]
                
                if oq[(y,x)][2] < cost2come:
                    cost2come = oq[(y,x)][2]
                
            #there are 5 location for the coordinate moment each with constant cost to come
            
            for child_y, child_x, c2c, angle, total_C in allpossiblesteps(x,y,angle,cost2come,xg ,yg ,img, action_set):
                # gg = 8
                # print(child_y, child_x, c2c, angle, total_C)
                if child_x < 400 and child_x >= 0 and child_y >= 0 and child_y < 250 and img[child_y,child_x] != 0:

                    # cv2.line(img,(x,y),(child_x,child_y), 150, 1)
                    # cv2.imshow("Animation", img)
                    # if cv2.waitKey(0) & 0xFF == ord('q'):
                    #     break
                    
                    if (child_y,child_x) not in cq and img[y][x] != 0:

                        if (child_y,child_x) not in oq:
                            # fc2c = c2c + cost2come + gg
                            hq.heappush(Q,(total_C,(y,x),(child_y,child_x),angle,c2c)) #putting in openlist
                            hq.heapify(Q) 
                            oq[(child_y,child_x)] = [total_C,[y,x],c2c]
                            
                        else:
                            if oq[(child_y,child_x)][0] >  total_C:
                                oq[(child_y,child_x)][1] = [y,x]   #change the parent
                                oq[(child_y,child_x)][0] =  total_C
                            
                            if oq[(child_y,child_x)][2] >  c2c:
                                oq[(child_y,child_x)][1] = [y,x]
                                oq[(child_y,child_x)][2] =  c2c

                if (xg - child_x)**2 + (yg - child_y)**2 <= 8 :        #if the coordinates of current node is near to goal node
                        #backtracking, successful return
                        # cv2.destroyAllWindows() 
                    print("Found")
                    backtrack(ele[2],xi,yi,oq,org_img)
                    salut = 2
                    exit(1)

    if salut == 1: 
        print("no solution found")
    
    else:
        print()

    # cv2.destroyAllWindows()     

if __name__ == "__main__":
    main()
