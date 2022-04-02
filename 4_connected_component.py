import cv2
import numpy as np
import matplotlib.pyplot as plt
# we read the image
a=cv2.imread('image.png',0)
# cv2.imshow('raw_image',a)
# cv2.waitKey(0)
#we convert our read image to binary
(thresh,binary_image)=cv2.threshold(a,128,255,cv2.THRESH_BINARY)
# cv2.imshow('binary_image',binary_image)
# cv2.waitKey(0)
rows=binary_image.shape[0]
columns=binary_image.shape[1]
# print(rows,columns)
x=0
y=0
label=0 # label count
#predict maximum number of objects that can be in the image
objects = []
for p in range(157):
        objects.append([])

########################################################################
# 
#       First Pass
# 
# #####################################################################        

labelled_image=np.zeros([rows,columns])
for i in range(rows):
    for j in range(columns):
        if(i==0 or j==0): # when its the pixel of either starting column of row
            if(i==0 and j==0): # when its the pixel starting pixel of image
                
                continue
            elif(i==0): # when its the pixel at start of row
                
                if(binary_image[i,j]!=0):
                    
                    if(binary_image[i-1,j]==1):
                        labelled_image[i,j]=labelled_image[i-1,j]
                    else:
                        #### new label made and new object identified
                        label=label+1   
                        labelled_image[i,j]=label
                        objects[object].append(label)
                else:
                    continue

            elif(j==0): #when its the pixel of starting column
                if(binary_image[i,j]!=0):
                    if( binary_image[i,j-1]):
                        labelled_image[i,j]=labelled_image[i,j-1]
                    else:
                        label=label+1
                        labelled_image[i,j]=label
                        objects[label].append(label)
                else:
                    continue
        else: # for the case of pixels other than starting row or column
            if(binary_image[i,j]!=0):# if the pixel is non-zero(its the object)
                if(binary_image[i,j-1]!=0 or binary_image[i-1,j]!=0):#if anyone of the neighbouring pixel is one
                    
                    if(binary_image[i,j-1]!=0 and binary_image[i-1,j]!=0):# if both neighbouring pixel are one
                        
                        if(labelled_image[i,j-1] == labelled_image[i-1,j]): # if label of both the pixels are same
                            labelled_image[i,j]=labelled_image[i,j-1]
                        else:# if label of both the pixels are different
                            labelled_image[i,j]=labelled_image[i,j-1]    #appending label in the equivalence table 
                            #empty the list for that pixel coz we have associated that pixel label to upper pixel label
                            objects[int(labelled_image[i,j])]=[]
                            #we find the list which has the label of upper pixel
                            for k in range(157):
                                #if label is found 
                                if labelled_image[i-1,j] in objects[k]:
                                    #see if label for our [i,j] pixel is there
                                    if labelled_image[i,j] in objects[k]:
                                        #if its there just continue
                                        continue
                                    else:
                                        #if itsn't append the label in that list
                                        objects[k].append(labelled_image[i,j])
                                else:
                                    continue
                            
                           
                    elif(binary_image[i,j-1]!=0): 
                        labelled_image[i,j]=labelled_image[i,j-1]
                    elif(binary_image[i-1,j]!=0):
                        labelled_image[i,j]=labelled_image[i-1,j]           
                else:
                    label=label+1
                    labelled_image[i,j]=label
                    objects[label].append(label)
            else:
                continue
# now we separate the lists which have labels accumulated. the empty lists are discarded
list_of_interest=[]
#this for loop checks all the lists
for i in range (157):
    #if the lists has some entry
    if(len(objects[i])!=0):
        #we included it in our list of interest
        list_of_interest.append(i)
# we convert our list to numpy array        
list=np.array(list_of_interest) 
# print(list)
#######################################################################
# 
#       2nd Pass
# 
# #####################################################################        

#checking all the rows
for i in range(rows):
    #checking all the colums
    for j in range (columns):
        #if its pixel with a label
        if(labelled_image[i,j]!=0):
            #we check the our equivalence table and see which list has the label
            for k in list:
                #if label is found in a list
                if labelled_image[i,j] in objects[k]:
                    #we assign that label a new value from start of list. so all labels in the same list have now same value
                    labelled_image[i,j]=objects[k][0]
                else:
                    continue
# we convert our labelled image to 8 bit unsigned int type                
labelled_image=labelled_image.astype(np.uint8)
#equalize the labels using histogram equilization so they are distinguishable
equalized_image = cv2.equalizeHist(labelled_image)

   
rgb=cv2.merge((equalized_image,equalized_image,equalized_image)) # we get the merged original matrix
original_shape=rgb.shape # we get its shape

# we flatten our orignal matrix
flattened=rgb.ravel()
# we get zero enteries of the flattened version
zero_enteries=np.argwhere(flattened == 0)
#now we merge our matrix on which we have applied operation
processed=cv2.merge((equalized_image,equalized_image-50,equalized_image-150))
#now we flatten that matrix
flattened=processed.ravel()
# now make the zero enteries in the processed matrix
flattened[zero_enteries]=0
# now we reshape our processed matrix
final=np.reshape(flattened,original_shape)
# now we print it
# print(final)

plt.imshow(final)
plt.savefig('processed.png')
plt.show()




