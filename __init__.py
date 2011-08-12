import os
from mtcPoker5CardDraw import Game
from libavg.utils import getMediaDir, createImagePreviewNode

__all__ = [ 'apps', 'disableExitButton',]

def createPreviewNode(maxSize):
    filename = os.path.join(getMediaDir(__file__), 'preview.png')
    return createImagePreviewNode(maxSize, absHref = filename)

apps = ({'class': Game,
            'createPreviewNode': createPreviewNode},
            )
