---
marp: true
---

# Find and classify the hidden playing card during image captioning - combining two models.

Deep Learning project

---
# Team
Antonio Georgiev, 0MI0600089
Bojidar Goranov, 0MI0600022
Teodor Kostadinov, 4MI0600097
 
![bg h:400px right Teamwork meme](media/teamwork_meme.jpg)

---

# Idea

The purpose of this project is to attempt combining **two pre trained** models - a card **classification model** and an **image captioning model**. The expected result is to have a model that can **both find** and **identify the card** on an image taken from Google Maps street view.

---

# Card classification model
- [Cards Image Dataset-Classification](https://www.kaggle.com/datasets/gpiosenka/cards-image-datasetclassification/data) in Kaggle
- Use a pre-trained **CNN** model.

![bg h:400px right Card example](media/queen_of_hearts.jpg)

---
# Image captioning model
- [Flickr Image dataset](https://www.kaggle.com/datasets/hsankesara/flickr-image-dataset) in Kaggle
- Use a pre-trained **CNN** model.

![bg w:550px left Flickr image example](media/flickr_image.jpg)

---
# Data

Combining the two datasets - **enormous** number of possible input files.

- **7624** cards training images
- **31783** Flickr images

---

![bg h:70% w:70% Input image variant combining card with normal image](media/input_v1.jpg)

---

![bg h:70% w:70% Input image variant combining card with normal image](media/input_v2.jpg)

---

![bg h:70% w:70% Input image variant combining card with normal image](media/input_v3.jpg)

---

![Multiple flickr images from the dataset](media/flickr_multiple_images.png)

---

![Multiple images of seven of spades from the dataset](media/seven_of_diamonds_multiple.png)

---

# Technologies

---

# Difficulties

- Creating and labeling the input data.
- Defining the exact output format that we want.

---
# Relevant papers


---
# Thank you
