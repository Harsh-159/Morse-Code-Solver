import cv2

#dict for alphanumeric to morse
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

#arr to morse letter
def decrypt(message):
    decipher = ''
    dummy = ''
    ans=''
    for letter in message:
        if letter==" ":
            try:
                ans+= list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(dummy)]
                dummy=''
            except:
                pass
        else:
            dummy += letter
    if dummy!='':
        try:
            ans += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(dummy)]
        except:
            pass
    return ans

#shapes to .-by area
def getContours(img,method):
    contours,Hierchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    arr=[]
    y=[]
    for cnt in contours:
        area=cv2.contourArea(cnt)
        arr.append(area)
        peri=cv2.arcLength(cnt,True)
        approx=cv2.approxPolyDP(cnt,0.02*peri,True)
        a,b,c,d=cv2.boundingRect(approx)
        y.append(b+d/2)
    if method=='image':
        arr=arr[::-1]
        y=y[::-1]
    if len(arr)>0:
        mid=sum(arr)/len(arr)
    else:
        return ''
    last=y[0]
    for i in range(1,len(y)):
        diff=y[i]-last
        last=y[i]
        y[i-1]=diff
    y.pop()
    y_mid=(max(y)+min(y))/2
    code=[]
    for i in range(len(arr)-1):
        if arr[i]>mid:
            code.append('-')
        else:
            code.append('.')
        if y[i] > y_mid:
            code.append(" ")
    if arr[-1] > mid:
        code.append('-')
    else:
        code.append('.')
    return decrypt(code)

#recording from webcam
# cap=cv2.VideoCapture(0)
# cap.set(10,72)
# decoded=''
# while True:
#     success, img=cap.read()
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img = cv2.GaussianBlur(img, (7, 7), 0)
#     img=cv2.Canny(img,100,100)
#     if getContours(img,"webcam")!='':
#         decoded=getContours(img,"webcam")
#     cv2.putText(img,decoded,(250,440),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
#     cv2.imshow("WebCam",img)
#     if cv2.waitKey(1)& 0xFF==ord('s'):
#         break

#reading via image
img=cv2.imread('Resources/alphabet.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#img = cv2.GaussianBlur(img, (7, 7), 0)
img=cv2.Canny(img,100,100)
decoded=getContours(img,'image')
print(decoded)