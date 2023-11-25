import os

import requests


class LayoutAPI:

	@staticmethod
	def fire(folder_path, model='craft'):
		"""
		calls the layout parser api and returns the json response
		"""
		url = 'https://ilocr.iiit.ac.in/layout/'
		print(f'Performing layout parser using API at: {url}')
		# files = os.listdir(folder_path)
		#files = [os.path.join(folder_path, i) for i in files if i.endswith('jpg')]
		
		"""files = [(
			'images', (
				os.path.basename(image_path),
				open(image_path, 'rb'),
				'image/jpeg',
			)
		) for image_path in files]"""

		files = [(
			'images', (
				os.path.basename(folder_path),
				open(folder_path, 'rb'),
				'image/jpeg',
			)
		) ]
		response = requests.post(
			url,
			headers={},
			data={
				'model': model
			},
			files=files,
		)
		if response.ok:
			return response.json()
		else:
			print(response.text)
