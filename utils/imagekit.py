from base64 import b64encode

from eunoia.settings import IMAGEKIT_PRIVATE_KEY, IMAGEKIT_PUBLIC_KEY, IMAGEKIT_URL_ENDPOINT
from imagekitio import ImageKit

imagekit = ImageKit(
  private_key = IMAGEKIT_PRIVATE_KEY,
  public_key = IMAGEKIT_PUBLIC_KEY,
  url_endpoint = IMAGEKIT_URL_ENDPOINT,
)

def upload_file(file, file_name):
  file_type = file.content_type.split("/")[1]
  file_name = f"{file_name}.{file_type}"
  response = imagekit.upload_file(
    file=b64encode(file.read()).decode("utf-8"),
    file_name=file_name
  )
  
  if response.file_id is None:
    print('Upload file error')
    return None
  else:
    return {
      "url": response.url,
      "id": response.file_id
    }

def delete_file(file_id):
  response = imagekit.delete_file(file_id)
  if response.response_metadata.http_status_code is not 204:
    print("Delete file error", response.get("error"))
  return