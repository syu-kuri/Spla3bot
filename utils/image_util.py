import requests
from PIL import Image

class ImageUtil:
    @staticmethod
    def gen_image_by_url(url1: str, url2: str):
      """
      Generate image by url

      :param url1: image url
      :param url2: image url
      :return: image
      """
      response1 = requests.get(url1, stream=True)
      response2 = requests.get(url2, stream=True)

      response1.raw.decode_content = True
      response2.raw.decode_content = True

      img1 = Image.open(response1.raw)
      img2 = Image.open(response2.raw)

      dst = Image.new('RGB', (img1.width + img2.width, min(img1.height, img2.height)))

      dst.paste(img1, (0, 0))
      dst.paste(img2, (img1.width, 0))

      return dst
