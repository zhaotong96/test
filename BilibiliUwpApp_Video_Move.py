import os
import shutil
from pathlib import Path
import json
import re
#Aid 视频数字id 即av号
#Title 视频标题
#Uploader 上传者
#Mid 上传者id 即uid
#vName 视频文件的文件名
#PartName 视频分P的标题
#文件夹命名规则为 Mid_Uploader
#图片命名规则为 [文件夹] /Aid_Title
#视频命名规则为 [文件夹] /vName_PartName

sourcePath="D:\\biliDL"#工作路径
desPath="D:\\O"#输出路径

dirlist=os.listdir(sourcePath)#路径内的 Aid列表
for Aid in dirlist:#读Aid
        partlist=os.listdir(os.path.join(sourcePath,Aid))#Aid内的 part列表

        Title=""
        Uploader=""
        Mid=""
        #读视频dvi文件 即Advi
        AdviPath=os.path.join(sourcePath,Aid,Aid+".dvi")
        if(Path(AdviPath).is_file()):
            adFile=open(AdviPath,'r',encoding='UTF-8')
            jsondata=json.load(adFile)
            Uploader=jsondata['Uploader']
            Mid=jsondata['Mid']
            Title=jsondata['Title']
            if(Title==None):Title="_"
            Title=re.sub('[\/:*?"<>|]',"_",Title)
        
            #如果文件夹不存在    路径为      输出路径下的/Mid_Uploader
        if not((os.path.exists(os.path.join(desPath,Mid+"_"+Uploader)))):
            os.mkdir(os.path.join(desPath,Mid+"_"+Uploader))#mkdir
            
        #读图片
        picName=os.path.join(sourcePath,Aid,"cover.jpg")#获得图片路径
        print(picName)
        if(Path(picName).is_file()):
            desPic=(os.path.join(desPath,Mid+"_"+Uploader,Aid+"_"+Title+".jpg"))
            shutil.move(picName,desPic)

        
        for part in partlist:#读part
            partPath=os.path.join(sourcePath,Aid,part)
            if(Path(partPath).is_dir()):#如果为文件夹
                PartName=""
                #读part的dvi信息 即Pdvi
                Pdvipath=os.path.join(partPath,Aid+".info")
                if(Path(Pdvipath).is_file()):
                    pdFile=open(Pdvipath,'r',encoding='UTF-8')
                    pdJsondata=json.load(pdFile)
                    PartName=pdJsondata['PartName']
                    if(PartName==None):PartName="_"
                    PartName=re.sub('[\/:*?"<>|]',"_",PartName)

                vlist=os.listdir(partPath)#part内的 视频文件列表
                for video in vlist:
                    vEX = os.path.splitext(video)[1]#读视频文件扩展名
                    if(vEX==".mp4"):#如果为MP4
                        vName=os.path.join(partPath,video)#获得视频文件路径
                        print(vName)
                        vDes=(os.path.join(desPath,Mid+"_"+Uploader, (os.path.splitext(video)[0]) +"_"+PartName+".mp4"))
                        shutil.move(vName,vDes)
