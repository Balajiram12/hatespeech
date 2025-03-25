import clip
import torch
import os
from PIL import Image
from torchvision import transforms

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device)
model.to(device).eval()

# Descriptions for hate speech and non-hate speech
descriptions = {
    'good meme': 'a nonhateful meme that is good',
    'hateful meme': 'a hateful meme containing racism, sexism, nationality, religion or disability'
}

text_labels = [descriptions['good meme'], descriptions['hateful meme']]
text_tokens = clip.tokenize([desc for desc in text_labels]).to(device)


def preprocess(image):
    """Preprocesses an image for CLIP."""

    preprocess_transforms = transforms.Compose([
        transforms.Resize(size=224, interpolation=transforms.InterpolationMode.BICUBIC),  # Resize
        transforms.CenterCrop(size=(224, 224)),  # Center crop
        transforms.Lambda(lambda image: image.convert("RGB")),  # Convert to RGB
        transforms.ToTensor(),  # Convert to PyTorch tensor
        transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], 
                             std=[0.26862954, 0.26130258, 0.26130258])  # Normalize
    ])

    return preprocess_transforms(image)

def classify_meme(image_path):
    """Classifies a meme as hateful or non-hateful using CLIP."""

    # Load and preprocess the image
    image = Image.open(image_path)
    image_input = preprocess(image).unsqueeze(0).to(device)  

    # Calculate image and text features
    with torch.no_grad():
        image_features = model.encode_image(image_input).float()
        text_features = model.encode_text(text_tokens).float()

    # Normalize features
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # Calculate similarity
    similarity = text_features.cpu().numpy() @ image_features.cpu().numpy().T

    # Classify based on similarity and hate_similarity
    if similarity[0][0] < 0.2:  # Check similarity with "good meme" description
        predicted_label = 0  # Non-hateful
    else:
        hate_similarity = (image_features.cpu() @ text_features.cpu().T).softmax(dim=-1)
        if hate_similarity[0][0] > hate_similarity[0][1]: 
            predicted_label = 0  # Non-hateful (higher similarity to "good meme")
        else:
            predicted_label = 1  # Hateful (higher similarity to "hateful meme")

    return predicted_label


# Example usage:
# dataset_path = "dataset"  # Replace with your dataset path
# predicted_labels = []

# for folder in ["good_memes", "hateful_memes"]:
#     folder_path = os.path.join(dataset_path, folder)
#     for filename in os.listdir(folder_path):
#         if filename.endswith((".jpg", ".jpeg", ".png")):
#             image_path = os.path.join(folder_path, filename)
#             predicted_label = classify_meme(image_path)
#             predicted_labels.append(predicted_label)
#             print(f"Image: {filename}, Predicted Label: {predicted_label}")

# ... further analysis of predicted_labels ...



