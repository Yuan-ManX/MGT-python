import cv2
import os
import numpy as np
from scipy.signal import medfilt2d
from ._centroid import mg_centroid
from ._filter import motionfilter
import matplotlib.pyplot as plt

def motionvideo(self, method = 'Diff', filtertype = 'Regular', thresh = 0.03, blur = 'None', kernel_size = 3):
    self.get_video()
    self.blur = blur
    self.method = method
    self.thresh = thresh
    self.filtertype = filtertype

    ret, frame = self.video.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(self.of + '_motion.avi',fourcc, self.fps, (self.width,self.height))
    gramx = np.zeros([1,self.width,3])
    gramy = np.zeros([self.height,1,3])
    qom = np.array([]) #quantity of motion
    com = np.array([]) #centroid of motion
    ii = 0
    if self.color == False:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gramx = np.zeros([1,self.width])
        gramy = np.zeros([self.height,1])
    #average = frame.astype(np.float)/self.length
    while(self.video.isOpened()):
        #May need to do this, not sure
        if self.blur == 'Average':
            prev_frame = cv2.blur(frame,(10,10))
        elif self.blur == 'None':
            prev_frame = frame                 

        ret, frame = self.video.read()
        if ret==True:
            if self.blur == 'Average':
                frame = cv2.blur(frame,(10,10)) #The higher these numbers the more blur you get
            elif self.blur == 'None':
                frame = frame                   #No blurring, then frame equals frame 

            if self.color == True:
                frame = frame
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame = np.array(frame)
            frame = frame.astype(np.float)
            #average += frame/self.length
            if self.method == 'Diff':
            
                if self.color == True:
                    motion_frame_rgb = np.zeros([self.height,self.width,3])

                    for i in range(frame.shape[2]):
                        motion_frame = (np.abs(frame[:,:,i]-prev_frame[:,:,i])).astype(np.uint8)
                        motion_frame = motionfilter(motion_frame,self.filtertype,self.thresh,kernel_size)
                        motion_frame_rgb[:,:,i] = motion_frame

                    movement_y = np.mean(motion_frame_rgb,axis=1).reshape(self.height,1,3)
                    movement_x = np.mean(motion_frame_rgb,axis=0).reshape(1,self.width,3)
                    gramy = np.append(gramy,movement_y,axis=1)
                    gramx = np.append(gramx,movement_x,axis=0)
                   
                else:
                    motion_frame = (np.abs(frame-prev_frame)).astype(np.uint8)
                    motion_frame = motionfilter(motion_frame,self.filtertype,self.thresh,kernel_size)

                    movement_y = np.mean(motion_frame,axis=1).reshape(self.height,1)
                    movement_x = np.mean(motion_frame,axis=0).reshape(1,self.width)
                    gramy = np.append(gramy,movement_y,axis=1)
                    gramx = np.append(gramx,movement_x,axis=0)

            elif self.method == 'OpticalFlow':
                print('Optical Flow not implemented yet!')

            if self.color == False: 
                motion_frame = cv2.cvtColor(motion_frame, cv2.COLOR_GRAY2BGR)
                motion_frame_rgb = motion_frame
            out.write(motion_frame_rgb.astype(np.uint8))
            combite, qombite = mg_centroid(motion_frame_rgb.astype(np.uint8),self.width,self.height,self.color)
            if ii == 0:
                com = combite.reshape(1,2)
                qom = qombite
            else:
                com=np.append(com,combite.reshape(1,2),axis =0)
                qom=np.append(qom,qombite)
        else:
            break
        ii+=1
        print('Processing %s%%' %(int(ii/(self.length-1)*100)), end='\r')
    if self.color == False:
        gramx = cv2.cvtColor(gramx.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        gramy = cv2.cvtColor(gramy.astype(np.uint8), cv2.COLOR_GRAY2BGR)

    gramx = gramx/gramx.max()*255
    gramy = gramy/gramy.max()*255
    cv2.imwrite(self.of+'_mgx.bmp',gramx.astype(np.uint8))
    cv2.imwrite(self.of+'_mgy.bmp',gramy.astype(np.uint8))
    #cv2.imwrite(self.of+'_average.bmp',average.astype(np.uint8))
    plot_motion_metrics(self.of,com,qom,self.width,self.height)

def plot_motion_metrics(of,com,qom,width,height):
    plt.rc('text',usetex = True)
    plt.rc('font',family='serif')
    fig = plt.figure(figsize = (12,6))
    ax = fig.add_subplot(1,2,1) 
    ax.scatter(com[:,0]/width,com[:,1]/height,s=2)
    ax.set_xlim((0,1))
    ax.set_ylim((0,1))
    ax.set_xlabel('Pixels normalized')
    ax.set_ylabel('Pixels normalized')
    ax.set_title('Centroid of motion')
    ax = fig.add_subplot(1,2,2)
    ax.set_xlabel('Time[frames]')
    ax.set_ylabel('Pixels normalized')
    ax.set_title('Quantity of motion')
    ax.bar(np.arange(len(qom)-1),qom[1:]/(width*height))
    #ax.plot(qom[1:-1])
    plt.savefig('%s_motion_com_qom.eps'%of,format='eps')





