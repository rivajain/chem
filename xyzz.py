import re
from sympy import Matrix, lcm
import streamlit as st

elementList=[]
elementMatrix=[]

st.set_page_config(layout="wide", page_icon="💬", page_title="CEB")
st.markdown("<h1 style='text-align: center; color: grey;'>Chemical Equation Balancer</h1>", unsafe_allow_html=True)

st.image("https://c4.wallpaperflare.com/wallpaper/22/728/16/technology-physics-and-chemistry-chemistry-hd-wallpaper-preview.jpg")

st.subheader("Hello Fellow Students!!!")
st.text("Lets Balance our Chemical Equations here")
st.text("Please input your reactants, this is case sensitive")
st.text("Your input should look like: H2O+Ag3(Fe3O)4")
reactants = st.text_input("Reactants:", "")

st.text("Please input your products, this is case sensitive")
products = st.text_input("Products:", "")

reactants=reactants.replace(' ', '').split("+")
products=products.replace(' ', '').split("+")
def addToMatrix(element, index, count, side):
    if(index == len(elementMatrix)):
       elementMatrix.append([])
       for x in elementList:
            elementMatrix[index].append(0)
    if(element not in elementList):
        elementList.append(element)
        for i in range(len(elementMatrix)):
            elementMatrix[i].append(0)
    column=elementList.index(element)
    elementMatrix[index][column]+=count*side
    
def findElements(segment,index, multiplier, side):
    elementsAndNumbers=re.split('([A-Z][a-z]?)',segment)
    i=0
    while(i<len(elementsAndNumbers)-1):#last element always blank
          i+=1
          if(len(elementsAndNumbers[i])>0):
            if(elementsAndNumbers[i+1].isdigit()):
                count=int(elementsAndNumbers[i+1])*multiplier
                addToMatrix(elementsAndNumbers[i], index, count, side)
                i+=1
            else:
                addToMatrix(elementsAndNumbers[i], index, multiplier, side)        
    
def compoundDecipher(compound, index, side):
    segments=re.split('(\([A-Za-z0-9]*\)[0-9]*)',compound)    
    for segment in segments:
        if segment.startswith("("):
            segment=re.split('\)([0-9]*)',segment)
            multiplier=int(segment[1])
            segment=segment[0][1:]
        else:
            multiplier=1
        findElements(segment, index, multiplier, side)

try:   
    for i in range(len(reactants)):
        compoundDecipher(reactants[i],i,1)
    if len(products)!=0 and len(reactants)!=0:
        for i in range(len(products)):
            compoundDecipher(products[i],i+len(reactants),-1)
        elementMatrix = Matrix(elementMatrix)
        elementMatrix = elementMatrix.transpose()
        if len(elementMatrix.nullspace())!=0:
            solution=elementMatrix.nullspace()[0]
            multiple = lcm([val.q for val in solution])
            solution = multiple*solution
            coEffi=solution.tolist()
            output=""
            for i in range(len(reactants)):
                output+=str(coEffi[i][0])+reactants[i]
                if i<len(reactants)-1:
                   output+=" + "
            output+=" -> "
            for i in range(len(products)):
               output+=str(coEffi[i+len(reactants)][0])+products[i]
               if i<len(products)-1:
                   output+=" + "

            st.info(output)
except:
    st.error('This is an error', icon="🚨")
