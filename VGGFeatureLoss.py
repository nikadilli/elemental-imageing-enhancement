import fastai
from fastai.vision import *
from fastai.callbacks import *
from fastai.utils.mem import *

from torchvision.models import vgg16_bn
from skimage.measure import compare_ssim

def gram_matrix(x):
    n,c,h,w = x.size()
    x = x.view(n, c, -1)
    return (x @ x.transpose(1,2))/(c*h*w)


class VGG16FeatureLoss(nn.Module):
    # create loss from VGG16 pretrained model and gram matrix
    def __init__(self, lyrs_wgts):
        super().__init__()
        
        # create vgg16 instance
        self.model = vgg16_bn(True).features.cuda().eval()
        requires_grad(self.model, False)
        
        # get layers with relu
        blocks = [i-1 for i,o in enumerate(children(self.model)) if isinstance(o,nn.MaxPool2d)]
        self.loss_features = [self.model[i] for i in blocks[2:5]]

        self.hooks = hook_outputs(self.loss_features, detach=False)
        self.wgts = lyrs_wgts
        self.metric_names = ['LAD',] + [f'feat_{i}' for i in range(len(blocks[2:5]))
                ] + [f'gram_{i}' for i in range(len(blocks[2:5]))]

    def make_features(self, x, clone=False):
        self.model(x)
        return [(o.clone() if clone else o) for o in self.hooks.stored]

    def forward(self, input, target):
        out_feat = self.make_features(target, clone=True)
        in_feat = self.make_features(input)
        # base l1 loss
        self.feat_losses = [F.l1_loss(input,target)]
        
        # feature loss
        self.feat_losses += [F.l1_loss(f_in, f_out)*w
                            for f_in, f_out, w in zip(in_feat, out_feat, self.wgts)]
        # gram matrix loss
        self.feat_losses += [F.l1_loss(gram_matrix(f_in), gram_matrix(f_out))*w**2 * 5e3
                            for f_in, f_out, w in zip(in_feat, out_feat, self.wgts)]

        self.metrics = dict(zip(self.metric_names, self.feat_losses))
        return sum(self.feat_losses)

    def __del__(self):
            self.hooks.remove()

