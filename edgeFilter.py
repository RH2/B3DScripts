#development stage: do no run on images larger than 128x128px
import bpy
import mathutils
import random
import copy

def abs(a):
	if(a<0):
		return(a*-1)
	return(a)
def lerp(a,b,f):
    delta=b-a   
    return(a+(delta*f))
def colSetA(a,b,c,d,f):
    col=mathutils.Color()
    result=None
    if(random.random()<0.2):
        result=[lerp(a[0],b[0],f),lerp(a[1],b[1],f),lerp(a[2],b[2],f)]
    else:
        result=[lerp(c[0],d[0],f),lerp(c[1],d[1],f),lerp(c[2],d[2],f)]
    return(result)
def checkPixels(img_x,img_y,x,y):
	return(1.0)

a=mathutils.Color()
a.hsv=[0.2,0,1]
a2=copy.copy(a)
a2.hsv=[0.4,1,1]

beta=mathutils.Color()
beta.hsv=[0.0,0,0.5]
beta2=copy.copy(a)
beta2.hsv=[0.2,1,1]


D=bpy.data
img=bpy.data.images["image"]
img_width=img.size[1]
img_height=img.size[0]
temp = [0] * img_width*img_height*4
img_copy= [0] * img_width*img_height*4
for px in range(len(img.pixels)):
	img_copy[px] = copy.copy(img.pixels[px])

for row in range(img_width):
	indexAdd=(row*4*img_width)
	for col in range(img_height):
		check_up=False
		check_down=False
		check_left=False
		check_right=False
		currentPixel=mathutils.Color()
		comparePixel=mathutils.Color()
		currentIndex=indexAdd+(col*4)
		currentPixel.r=copy.copy(img_copy[currentIndex])
		currentPixel.g=copy.copy(img_copy[currentIndex+1])
		currentPixel.b=copy.copy(img_copy[currentIndex+2])
		thisEdgeIntensity=mathutils.Color()
		thisEdgeIntensity.hsv=[0,0,0]

		currentIndex=indexAdd+(col*4)
		temp[currentIndex]=0.0
		temp[currentIndex+1]=0.0
		temp[currentIndex+2]=0.0
		temp[currentIndex+3]=1.0
		if not(indexAdd+(col)<img_width):#then process bottom edge
			check_down=True
		if not(indexAdd+(col)>((img_width*img_height*4)-4*img_width)):#ignore top edge
			check_up=True
		if not(col%(img_width*4)==0):#ignore left edge
			check_left=True
		if not(col-img_width+1%(img_width*4)==0):#ignore right edge
			check_right=True

		if(check_up==True):
			currentIndex=indexAdd+((4*img_width)-4)+(col*4)
			comparePixel.r=img_copy[currentIndex+0]
			comparePixel.g=img_copy[currentIndex+1]
			comparePixel.b=img_copy[currentIndex+2]
			thisEdgeIntensity.v+=abs(currentPixel.v-comparePixel.v)/8
			thisEdgeIntensity.h+=0.1*thisEdgeIntensity.v
			thisEdgeIntensity.s+=1	
		if(check_down==True):
			currentIndex=indexAdd-((4*img_width)+4)+(col*4)
			comparePixel.r=img_copy[currentIndex+0]
			comparePixel.g=img_copy[currentIndex+1]
			comparePixel.b=img_copy[currentIndex+2]
			thisEdgeIntensity.v+=abs(currentPixel.v-comparePixel.v)/8
			thisEdgeIntensity.h+=0.1*thisEdgeIntensity.v
			thisEdgeIntensity.s+=1		
		if(check_right==True):
			currentIndex=indexAdd+(col*4)+4
			comparePixel.r=img_copy[currentIndex+0]
			comparePixel.g=img_copy[currentIndex+1]
			comparePixel.b=img_copy[currentIndex+2]
			thisEdgeIntensity.v+=abs(currentPixel.v-comparePixel.v)/8
			thisEdgeIntensity.h+=0.1*thisEdgeIntensity.v
			thisEdgeIntensity.s+=1	
		if(check_left==True):
			currentIndex=indexAdd+(col*4)-4
			comparePixel.r=img_copy[currentIndex+0]
			comparePixel.g=img_copy[currentIndex+1]
			comparePixel.b=img_copy[currentIndex+2]
			thisEdgeIntensity.v+=abs(currentPixel.v-comparePixel.v)/8
			thisEdgeIntensity.h+=0.1*thisEdgeIntensity.v
			thisEdgeIntensity.s+=1	

		currentIndex=indexAdd+(col*4)
		temp[currentIndex+0]=thisEdgeIntensity.r*2
		temp[currentIndex+1]=thisEdgeIntensity.g*2
		temp[currentIndex+2]=thisEdgeIntensity.b*2
		temp[currentIndex+3]=1.0

for px in range(len(img_copy)):
	img_copy[px]=img_copy[px]*.5 + temp[px]*2
img.pixels=img_copy
coverageMap = [0] *(img_width*img_height)
for row in range(img_width):
	indexAdd=(row*4*img_width)
	for col in range(img_height):
			tempColor = mathutils.Color()
			tempColor.r = copy.copy(temp[indexAdd+(col*4)+0])
			tempColor.g = copy.copy(temp[indexAdd+(col*4)+1])
			tempColor.b = copy.copy(temp[indexAdd+(col*4)+2])
			coverageMap[(row*img_width)+col]=copy.copy(tempColor.v)
coverageSum=0         
for i in range(img_width*img_height):
	coverageSum+=coverageMap[i]
print("coverage average is:"+str(coverageSum/(img_width*img_height)))
            


            