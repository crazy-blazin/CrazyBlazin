from PIL import Image
import PIL
import torch
import requests
import asyncio


def face2paint_(device="cpu", size=512, side_by_side=False):
    from PIL import Image
    from torchvision.transforms.functional import to_tensor, to_pil_image

    def face2paint(
        model: torch.nn.Module,
        img: Image.Image,
        size: int = size,
        side_by_side: bool = side_by_side,
        device: str = device,
    ) -> Image.Image:
        w, h = img.size
        s = min(w, h)
        img = img.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
        img = img.resize((size, size), Image.LANCZOS)

        with torch.no_grad():
            input = to_tensor(img).unsqueeze(0) * 2 - 1
            output = model(input.to(device)).cpu()[0]

            if side_by_side:
                output = torch.cat([input[0], output], dim=2)

            output = (output * 0.5 + 0.5).clip(0, 1)
        output = to_pil_image(output)
        # output = output.resize((w, h), Image.BILINEAR)
        return output

    return face2paint

async def arcanify(link):
    # https://github.com/bryandlee/animegan2-pytorch/blob/main/hubconf.py
    torch.hub._validate_not_a_forked_repo=lambda a,b,c: True
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", pretrained="face_paint_512_v2").to(device).eval()
    # face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", device=device)
    face2paint = face2paint_(device=device)
    
    link_check_slash = link.split('/')
    link_check_dot = link.split('.')
    file_types = ['jpg', 'png', 'jpeg']
    webtypes = ['http:', 'https:']
    # if link_check_slash[0] not in webtypes:
    #     return False
    
    path_out = f'tools/imagefolder/output.jpg'
    # requests download image from url and save it to path
    with open(path_out, 'wb') as f:
        f.write(requests.get(link).content)

    try:
        img = Image.open('tools/imagefolder/output.jpg').convert("RGB")
    except PIL.UnidentifiedImageError:
        return False

    out = face2paint(model, img)
    out.save(f'tools/imagefolder/forged.jpg')

    return 'tools/imagefolder/forged.jpg'