import cv2

def TB_Bmin(threshold,ImageBGR,window,limits):

    limits['B']['min'] = threshold
    mask = cv2.inRange(ImageBGR,
                       (limits['B']['min'], limits['G']['min'], limits['R']['min']),
                       (limits['B']['max'], limits['G']['max'], limits['R']['max']))
    cv2.imshow(window, mask)

def TB_Bmax(threshold,ImageBGR,window,limits):

    limits['B']['max'] = threshold
    mask = cv2.inRange(ImageBGR,
                       (limits['B']['min'], limits['G']['min'], limits['R']['min']),
                       (limits['B']['max'], limits['G']['max'], limits['R']['max']))
    cv2.imshow(window, mask)

def TB_Gmin(threshold,ImageBGR,window,limits):

    limits['G']['min'] = threshold
    mask = cv2.inRange(ImageBGR,
                       (limits['B']['min'], limits['G']['min'], limits['R']['min']),
                       (limits['B']['max'], limits['G']['max'], limits['R']['max']))
    cv2.imshow(window, mask)

def TB_Gmax(threshold,ImageBGR,window,limits):

    limits['G']['max'] = threshold
    mask = cv2.inRange(ImageBGR,
                       (limits['B']['min'], limits['G']['min'], limits['R']['min']),
                       (limits['B']['max'], limits['G']['max'], limits['R']['max']))
    cv2.imshow(window, mask)

def TB_Rmin(threshold,ImageBGR,window,limits):

    limits['R']['min'] = threshold
    mask = cv2.inRange(ImageBGR,
                       (limits['B']['min'], limits['G']['min'], limits['R']['min']),
                       (limits['B']['max'], limits['G']['max'], limits['R']['max']))
    cv2.imshow(window, mask)

def TB_Rmax(threshold,ImageBGR,window,limits):

    limits['R']['max'] = threshold
    mask = cv2.inRange(ImageBGR,
                       (limits['B']['min'],limits['G']['min'],limits['R']['min']),
                       (limits['B']['max'],limits['G']['max'],limits['R']['max']) )
    cv2.imshow(window,mask)