from typing import List
import os
def caption_images(paths: List[str]) -> List[str]:
	if os.getenv("SKIP_VISION") == "1":
		return [""] * len(paths)
	try:
		from PIL import Image  # type: ignore
		from transformers import BlipProcessor, BlipForConditionalGeneration
		model_name = "Salesforce/blip-image-captioning-base"
		processor = BlipProcessor.from_pretrained(model_name)
		model = BlipForConditionalGeneration.from_pretrained(model_name)
		captions = []
		for p in paths:
			image = Image.open(p).convert("RGB")
			inputs = processor(image, return_tensors="pt")
			out = model.generate(**inputs, max_new_tokens=30)
			text = processor.decode(out[0], skip_special_tokens=True)
			captions.append(text)
		return captions
	except:
		return [""] * len(paths)

