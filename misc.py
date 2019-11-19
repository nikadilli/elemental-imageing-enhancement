import numpy as np
import PIL


def prediction_to_image(arr):
    """converts numpy array from model prediction to PIL image.

    Parameters
    ----------
    arr : ndarray 
        rgb image in array form to be converted """
        
    arr = np.squeeze((img_pr[0]+img_pr[1]+img_pr[2])/3)
    arr = arr/arr.max()*255
    im = PIL.Image.fromarray(np.uint8(arr))
    return im
