#development stage: do no run on images larger than 128x128px
import bpy
import mathutils
import random
import copy

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
temp = [None] * img_width*img_height*4
for row in range(img_width):
	indexAdd=(row*4*img_width)
	for col in range(img_height):
		thisEdgeIntensity=mathutils.Color()
		thisEdgeIntensity.hsv=[0,0,0]

		temp[indexAdd+(col*4)+0]=0.0
		temp[indexAdd+(col*4)+1]=0.0
		temp[indexAdd+(col*4)+2]=0.0
		temp[indexAdd+(col*4)+3]=1.0
		if not(indexAdd+(col)<img_width):#ignore bottom edge
			temp[indexAdd+(col*4)+0]=1.0
			temp[indexAdd+(col*4)+1]=0.0
			temp[indexAdd+(col*4)+2]=0.0
			temp[indexAdd+(col*4)+3]=1.0
		if not(indexAdd+(col)>((img_width*img_height*4)-4*img_width)):#ignore top edge
			temp[indexAdd+(col*4)+0]=1.0
			temp[indexAdd+(col*4)+1]=1.0
			temp[indexAdd+(col*4)+2]=0.0
			temp[indexAdd+(col*4)+3]=1.0
		if not(col%(img_width*4)==0):#ignore left edge
			temp[indexAdd+(col*4)+0]=0.0
			temp[indexAdd+(col*4)+1]=1.0
			temp[indexAdd+(col*4)+2]=1.0
			temp[indexAdd+(col*4)+3]=1.0
		if not(col-img_width+1%(img_width*4)==0):#ignore right edge
			temp[indexAdd+(col*4)+0]=0.5
			temp[indexAdd+(col*4)+1]=0.0
			temp[indexAdd+(col*4)+2]=1.0
			temp[indexAdd+(col*4)+3]=1.0

img.pixels=temp
coverageMap = [50] *(img_width*img_height)
for row in range(img_width):
	indexAdd=(row*4*img_width)
	for col in range(img_height):
			tempColor = mathutils.Color()
			#tempColor = [temp[indexAdd+(col*4)+0],temp[indexAdd+(col*4)+1],temp[indexAdd+(col*4)+2]]
			tempColor.r = copy.copy(temp[indexAdd+(col*4)+0])
			tempColor.g = copy.copy(temp[indexAdd+(col*4)+1])
			tempColor.b = copy.copy(temp[indexAdd+(col*4)+2])
			coverageMap[(row*img_width)+col]=copy.copy(tempColor.v)
coverageSum=0         
for i in range(img_width*img_height):
	coverageSum+=coverageMap[i]
print("coverage average is:"+str(coverageSum/(img_width*img_height)))
            


            