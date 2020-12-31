import imageio
import numpy as np
import os

def deletefromfolder(path):
    datadir = path
    print('Directory:', datadir)

    rmmap = dict()
    total = 0
    repeatcnt = 0
    for root, directories, filenames in os.walk(datadir):
        for filename in filenames:
            total += 1
            if filename.endswith('.jpg') and not filename.startswith('._'):
                filei = os.path.join(root, filename)
                imi = imageio.imread(filei)
                npi = np.asarray(imi).reshape(1, -1).reshape((2025, ))
                idf = npi.tolist()
                for i in range(len(idf)):
                    idf[i] = str(idf[i])
                strlist = ''.join(idf)

                if strlist in rmmap.keys():
                    repeatcnt += 1
                    rmmap[strlist].append(filename)
                else:
                    rmmap[strlist] = list()

    #for key in rmmap:
    #    print(rmmap[key])
    print('Repeat/Total: {}/{}'.format(repeatcnt, total))
    for key in rmmap:
        for item in rmmap[key]:
            os.remove(os.path.join(datadir,fg item))

if __name__ == '__main__':
    images_path = os.path.dirname(os.path.realpath(__file__))
    dirlist = os.listdir(images_path)
    for item in dirlist:
        deletefromfolder(os.path.join(images_path,item))