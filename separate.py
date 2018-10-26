import cv2
import numpy as np
import random
import os


def postMap(all, white):
    post = 255 - (imgWhite - imgAll)
    post = cv2.cvtColor(post, cv2.COLOR_BGR2GRAY)
    ret, post = cv2.threshold(post, 200, 255, cv2.THRESH_BINARY)
    return post


def getPost(imgPost, comp):
    circles = cv2.HoughCircles(imgPost, cv2.HOUGH_GRADIENT, 1,
                               20, param1=50, param2=30, minRadius=95, maxRadius=125)
    imgPost = cv2.medianBlur(imgPost, 3)
    circles = np.uint16(np.around(circles))
    imgPost = cv2.cvtColor(imgPost, cv2.COLOR_GRAY2BGR)

    #create an img which only the position of posts is drawn.
    for i in circles[0, :]:
        cv2.circle(imgPost, (i[0], i[1]), 2, (0, 0, 255), 3)
        cv2.circle(imgPost, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv2.imwrite("detected{}.png".format(comp), imgPost)

    return circles[0, :]


def trim(img, centerX, centerY, width, height, name,save=True):
    leftTop = (centerX - int(width / 2), centerY - int(height / 2))
    imgTrim = img[leftTop[1]:leftTop[1] +
                  height, leftTop[0]:leftTop[0] + width]
    if save:
        cv2.imwrite(name, imgTrim)
    return imgTrim


def inflation(folder,out):
    files=os.listdir(folder)
    for file in files:
        if file[-4::]==(".png" or ".jpg"):
            img=cv2.imread(os.path.join(folder,file))
            for i in range(4):
                img=img.transpose(1,0,2)[:,::-1]
                cv2.imwrite(os.path.join(out,file)[:-4:]+"-{}.png".format(90*i),img)
                imgMirror=cv2.flip(img,1)
                cv2.imwrite(os.path.join(out,file)[:-4:]+"-{}-t.png".format(90*i),imgMirror)




if __name__ == "__main__":

    for comp in (38, 39):
        imgAll = cv2.imread("all{0}.png".format(comp))
        imgWhite = cv2.imread("white{0}.png".format(comp))
        imgPost = postMap(imgAll, imgWhite)
        cv2.imwrite("thresh{}.png".format(comp),imgPost)
        posts = getPost(imgPost, comp)
        for j, post in enumerate(posts):
            trim(imgWhite, post[0], post[1], 300, 300,
                 "Post/{0}post-{1}.png".format(comp, j))
            trim(imgWhite, random.randint(posts.min(axis=0)[0], posts.max(axis=0)[0]), random.randint(
                posts.min(axis=0)[1], posts.max(axis=0)[1]), 300, 300, "NOTPost/{0}not-{1}.png".format(comp, j))

    inflation("Post","Post水増し")
    inflation("NOTPost","NOTPost水増し")
