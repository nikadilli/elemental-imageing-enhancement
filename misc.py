import numpy as np
import PIL


def prediction_to_image(arr):
    """converts numpy array from model prediction to PIL image.

    Parameters
    ----------
    arr : ndarray 
        rgb image in array form to be converted """
        
    arr = np.squeeze((arr[0]+arr[1]+arr[2])/3)
    arr = arr/arr.max()*255
    im = PIL.Image.fromarray(np.uint8(arr))
    return im

def ablation_to_image(path, p=99):
    """converts csv from laser ablation to image clipping out outliers.

    Parameters
    ----------
    path : str or path 
        path to csv file
    p: float
        percentile to remove outliers from laser """
    
    savename = re.sub('\..*$', '', filename)+'.png'
    im = np.genfromtxt(path, delimiter=',')
    perc = np.percentile(im, p)
    im = np.where(im<perc, im, perc) 
    im = im/im.max()*255
    im = im.astype(np.uint8)
    imageio.imwrite(path + savename, im)
