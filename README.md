![a](/apm/l/:packageName)

# Enhancement of the elemental imaging

**Elemental imaging** is visualization of the distribution of elements of interest within solid samples. It is widely used across different fields analyzing various materials by many analytical techniques. With destructive methods, such as LA-ICP-MS or LIBS, where the sample is ablated by laser beam spot, by spot, we get pixelated image where the resolution is dependant on the beam size. Decreasing the beam size infinitely is not possible, which leads us to image enhancement by computers.

Enhancement of the elemental imaging consists mostly of noise removal and incresing resolution.

## Training set preparation
The training set consists of original high resolution images and their 'crappyfied' version created by virtual ablation. **Laser Ablation** is the process of removing material from a solid sample by irradiating it with a laser beam. The quality of the resulting image is highly dependant on the contidions used for ablation.    

Modelling was performed using five consecutive matrix manipulation steps [[1]](https://pubs.rsc.org/en/content/articlehtml/2019/ja/c9ja00166b):
1. laser sampling of the sample in the ablation cell
2. introduction of Flicker noise (mostly associated with pulse reproducibility)
3. aerosol washout from the ablation cell and transfer to the detector
4. measurement by integrating the counts for a chosen dwell time
5. introduction of Poisson noise (as a result of counting statistics)

**LA conditions**

Parameter | Value
--- | --- 
Beam size | 5 μm
Repetition rate | 100 Hz

## Models
This deep learning model was build using the great [fast.ai](https://www.fast.ai/about/) library. It consists of [UNet](https://arxiv.org/pdf/1505.04597.pdf), where the encoder was created from a pretrained ResNet34 and [Perceptual loss](https://arxiv.org/abs/1603.08155) combined with a Least Absolute Deviations and gramian function. 

The model was finetuned on different datasets. In future we plan to explore different conditions of laser ablation, as well as creating specialized models for biological or geological samples. 

**Model-pets**
This model was trained using the subset of imagenet containing pets from fast.ai. This was the first model, just to test how the neurall network handles laser ablation data. This weights are not meant to be used for real ablation, since the dataset contains pictures of cats and dogs.

**Model-cells**
This model was trained using the [Recursion Cellular Image dataset](https://www.rxrx.ai). The pretrained weights are available  [here](https://www.dropbox.com/s/aa7fqv4sypb0ecy/model.pth).

## Results

**Example images from cell dataset**

![comparison1](results/cells/E07_s2_w2_plot.png)
![comparison2](results/cells/I07_s1_w5_plot.png)
![comparison2](results/cells/J20_s1_w2_plot.png)

## References

[[1]](https://pubs.rsc.org/en/content/articlehtml/2019/ja/c9ja00166b) van Elteren, J.T., Šelih, V.S. and Šala, M., 2019. Insights into the selection of 2D LA-ICP-MS (multi) elemental mapping conditions. Journal of Analytical Atomic Spectrometry, 34(9), pp.1919-1931.

[[2]](https://arxiv.org/pdf/1505.04597.pdf) Ronneberger, O., Fischer, P. and Brox, T., 2015, October. U-net: Convolutional networks for biomedical image segmentation. In International Conference on Medical image computing and computer-assisted intervention (pp. 234-241). Springer, Cham.
