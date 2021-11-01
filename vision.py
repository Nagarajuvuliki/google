from google.cloud import vision
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(BASE_DIR,'googlevision')+"\\psychic-apex-326811-5108c53a0e5a.json"
def localize_objects(path):
        """Localize objects in the local image.

        Args:
        path: The path to the local file.
        """
        client = vision.ImageAnnotatorClient()

        with open(path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        objects = client.object_localization(
            image=image).localized_object_annotations

        print('Number of objects found: {}'.format(len(objects)))
        return objects
        # for object_ in objects:
        #     print('\n{} (confidence: {})'.format(object_.name, object_.score))