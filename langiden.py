import base64
import json
import os
from os.path import join

import requests


class LangIdenAPI:

	@staticmethod
	def fire(folder_path):
		"""
		calls the layout parser api and returns the json response
		"""
		url = "https://ilocr.iiit.ac.in/layout/postprocess/language/scenetext"
		print(f'Performing Language identification using API at: {url}')
		images = os.listdir(folder_path)
		try:
			images = sorted(images, key=lambda x:int(x.strip().split('.')[0]))
		except:
			images = sorted(images)
		image_names = images.copy()
		images = [join(folder_path, i) for i in images if i.endswith('jpg') or i.endswith('png')]
		images = [base64.b64encode(open(i, 'rb').read()).decode() for i in images]
		req = {
			'images': images,
		}
		headers = {
			'Content-Type': 'application/json'
		}
		response = requests.post(
			url,
			headers=headers,
			data=json.dumps(req),
		)
		if response.ok:
			ret = response.json()
			ret = [i['text'] for i in ret]
			return {i[0]: i[1] for i in zip(image_names, ret)}


if __name__ == '__main__':
	folder_path = '/home/pooja/test'

	ret = LangIdenAPI.fire(folder_path)
	with open(join(folder_path, 'out.json'), 'w', encoding='utf-8') as f:
		f.write(json.dumps(ret, indent=4))
