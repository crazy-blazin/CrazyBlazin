from PIL import Image
import torch
import requests
import asyncio

async def arcanify(link):
    torch.hub._validate_not_a_forked_repo=lambda a,b,c: True
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", pretrained="face_paint_512_v2").to(device).eval()
    face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", device=device)

    link_check_slash = link.split('/')
    link_check_dot = link.split('.')
    file_types = ['jpg', 'png', 'jpeg']
    webtypes = ['http:', 'https:']
    if link_check_dot[-1] not in file_types or link_check_slash[0] not in webtypes:
        return False
    
    path_out = f'tools/imagefolder/output.jpg'
    # requests download image from url and save it to path
    with open(path_out, 'wb') as f:
        f.write(requests.get(link).content)

    img = Image.open('tools/imagefolder/output.jpg').convert("RGB")
    out = face2paint(model, img)
    out.save(f'tools/imagefolder/forged.jpg')

    return 'tools/imagefolder/forged.jpg'