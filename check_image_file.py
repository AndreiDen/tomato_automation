import requests
import mimetypes

front_page_image_link = 'http://84.201.167.41:22549/files/3dead156448e3bc3b84eddab2fa32545/page-1.png'
response = requests.get(front_page_image_link)

content_type = response.headers['content-type']
extension = mimetypes.guess_extension(content_type)
file_size = response.headers.get('Content-Length')
print(response.status_code)
print(extension)
print(file_size)