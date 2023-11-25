import base64
import io
import json
import os
import time
from os.path import join

import requests


class OCRAPI:

	@staticmethod
	def fire(folder_path, language_code,modality):
		"""
		calls the layout parser api and returns the json response
		"""
		url = 'https://ilocr.iiit.ac.in/ocr/infer'
		images = os.listdir(folder_path)
		images = sorted(images, key=lambda x:int(x.strip().split('.')[0]))
		image_names = images.copy()
		images = [join(folder_path, i) for i in images if i.endswith('jpg')]
		images = [base64.b64encode(open(i, 'rb').read()).decode() for i in images]
		if(modality=='handwritten'):
			version = 'v3'
		elif(modality=='printed'):
			if(language_code=='te'):
				version='v4.8u_robust'
			else:
				version='tesseract'
		elif(modality=='scenetext'):
			version='v3_st'
		print(version)
		ocr_request = {
			'imageContent': images,
			'modality': modality,
			'version': version,
			'language': language_code,
		}
		headers = {
			'Content-Type': 'application/json'
		}
		print(f'Performing OCR using API at: {url}')
		response = requests.post(
			url,
			headers=headers,
			data=json.dumps(ocr_request),
		)
		if response.ok:
			ret = response.json()
			ret = [i['text'] for i in ret]
			return {i[0]: i[1] for i in zip(image_names, ret)}

