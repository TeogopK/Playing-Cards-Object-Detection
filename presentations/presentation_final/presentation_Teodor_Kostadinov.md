---
marp: true
---

# Playing cards object detection model 

### Developing a model that can detect multiple cards and identify their suit and rank.

by Teodor Kostadinov, 4MI0600097, 
Faculty of Mathematics and Informatics, Sofia University

---

# Business idea

Developing an application that can:
- assist during a game of Blackjack, Bridge, Belot, Poker, etc.

---

# Business idea

To create the application a model recognizing the playing cards is required.
A **fast implementation** of the required model is needed as soon as possible to develop the business!

---

# Problem #1

Since the business **is just starting**, no senior Data science team members are currently available.
There is no advanced knowledge on the topic, **nor time** to develop a model from scratch.

---

# Solution to Problem #1

Use a popular **pretrained model** and a **library** that allows easy access to ease the implementation.
In our case:
- **YOLOv8** model
- **Pyhton ultralytics** library

---
# Problem #2 

There is **no public dataset** available.*
There is no time to create a big dataset, with well-designed examples for training, nor time to label them.

---
# Finding a dataset

A person, facing the same problem, has created a syntethic dataset with over 20,000 images. [Link](https://www.kaggle.com/datasets/andy8744/playing-cards-object-detection-dataset) to dataset in kaggle

> First I took 20-30 second videos of all 52 cards under variable light temperature and brightness. The images were processed with open-cv. The DTD dataset (https://www.robots.ox.ac.uk/~vgg/data/dtd/) was used to simulate backgrounds of various textures for our dataset.

--- 
# Examples of the images

A set of 1, 2 or 3 cards together placed on different backgrounds.

![alt text](media/synthetic_image_example.jpg)

---
# Examples of the images

Since the dataset is generated programmatically, there are obvious patterns.

![h:500px alt text](media/synthetic_data_example.png)

---

# Our YOLOv8_syntethic model

- Trained on **YOLOv8 medium** using 10 epochs
- Trained with **20 000 images** split 70/20/10 and 52 classes.
- **2 hours training** time on NVIDIA RTX A2000 8GB Laptop GPU.
- Can detect each card from the test set with **~99%** accuracy.

---
# Our YOLOv8_synthetic model statistics

The results are impressive on paper:

![alt text](media/yolov8_synthethic.png)

---
# Our YOLOv8_synthetic in practice

Working pretty good on similar style pictures:

![alt text](media/yolov8_synthethic_example1.png)

---
# Our YOLOv8_synthetic in practice

![alt text](media/yolov8_synthethic_example2.png)

---
# Our YOLOv8_synthetic in practice

![alt text](media/yolov8_synthethic_example5.jpg)


---
# Our YOLOv8_synthetic in practice

When the images differ from the synthetic format the results drop as well:

![alt text](media/yolov8_synthethic_example3.png)

---
# Our YOLOv8_synthetic in practice

It can also detect printings of a train data but not other types of cards:

![alt text](media/yolov8_synthethic_example4.png)

---
# Creating own small dataset

The dataset is created with **"real" life** examples of cards.
Since 52 classes of cards require a lot of data - the classes were **cut to 13** (Hearts only).

---
# Our real dataset examples

Captured and labeled **100** photos with different configurations of cards.

![h:500px](media/own_data_example.jpg)

---
# Our YOLOv8_real model

- Trained on YOLOv8 medium using **100** epochs
- Trained with **100 images** split 70/20/10 and 13 classes.
- **20 minutes training** time on NVIDIA RTX A2000 8GB Laptop GPU.
- Results are not quite impressive but this is expected as the low number of data entries.


---
# Our YOLOv8_real model statistics

The results are impressive on paper:

![alt text](media/yolov8_real_results.png)

---
# Our YOLOv8_real on test set

The test set is not perfect, there are a handful of mistakes. 

![h:500px](media/yolov8_real_predictions.jpg)

---
# Our YOLOv8_real in practice

It is doing ok on images with Hearts, but not as good as YOLOv8_synthetic

![alt text](media/yolov8_real_example1.jpg)

---
# Our YOLOv8_real in practice

![h:500px](media/yolov8_real_example3.jpg)

---
# Our YOLOv8_real in practice

However, it does confuse other suits for Hearts.

![alt text](media/yolov8_real_example2.jpg)

---
# Our YOLOv8_real in practice

![h:500px](media/yolov8_real_example4.jpg)

---
# Augmented dataset workaround

Developed a Python script that **transforms the images** in a dataset, effectively multiplying the dataset.
The library used to transform the marked bounding boxes in the original dataset correctly to the augmented one is: [***imgaug***](https://imgaug.readthedocs.io/en/latest/)

---

# Augmented dataset example

![h:600px](media/augmented_data_example.png)

---
# Our YOLOv8_aug model

- Trained on YOLOv8 medium using **100** epochs
- Trained with **1000 images** split 70/20/10 and 13 classes.
- **40 minutes training** time on NVIDIA RTX A2000 8GB Laptop GPU.
- Results are questionable - similar to the model without augmentation.


---
# Our YOLOv8_aug model statistics

Observing similar mAP50 and mAP50-95 percents as YOLOv8_real.

![alt text](media/yolov8_aug_results.png)

---
# Our YOLOv8_aug on test set

It is still making similar mistakes to the previous model:

![h:500px](media/yolov8_aug_predictions.jpg)

---
# Our YOLOv8_aug in practice

It still does not detect the Ace, loses the King though.

![alt text](media/yolov8_aug_example1.jpg)

---

# Combining the datasets

Combined the synthetic and "real" datasets, taking all **100 images** from the "real" dataset and **10 times more** from the synthetic one.
Developed a script the **relabels** all 52 classes **to the 13** from the "real" one, dropping all classes that are not Hearts.


---
# Our YOLOv8_comb model

- Trained on YOLOv8 medium using **100** epochs
- Trained with **1100 images** split 70/20/10 and 13 classes.
- **50 minutes training** time on NVIDIA RTX A2000 8GB Laptop GPU.
- Results are worse than the synthetic model.

---
# Our YOLOv8_comb model statistics

![alt text](media/yolov8_comb_results.png)

---
# Our YOLOv8_comb on test set

It is doing fine on the test set, detecting only Hearts.

![h:500px](media/yolov8_comb_predictions.jpg)

---
# Our YOLOv8_comb in practice

Doing similarly to the other models in some situations.

![alt text](media/yolov8_comb_example1.jpg)

---

# Our YOLOv8_comb in practice

The model managed to detect the Ace, but not the King:

![alt text](media/yolov8_comb_example2.jpg)

---

# Our YOLOv8_comb in practice

There are definite examples that the model is not better than the others.

![h:500px](media/yolov8_comb_example3.jpg)

---
# Retraining the synthetic YOLOv8_synth model

Using the well-performing YOLOv8_synth as **base model** to **fine-tune** the model on the Hearts dataset with **13 classes**.

---
# Our YOLOv8_tuned model

- Trained on YOLOv8 medium using **100** epochs
- Pretrained with **20 000 images** and 52 classes.
- Fine-tuned with **100 images** split 70/20/10 and 13 classes.
- **10 minutes training** time on NVIDIA RTX A2000 8GB Laptop GPU.


---
# Our YOLOv8_tuned model statistics

![alt text](media/yolov8_tuned_results.png)

---
# Our YOLOv8_tuned on test set


![h:500px](media/yolov8_tuned_predictions.jpg)

---

# Our YOLOv8_tuned in practice

The model finally detects the Ace of hearts, but still mistakes other suits for Hearts.

![h:500px](media/yolov8_tuned_example2.jpg)

---

# Our YOLOv8_tuned in practice

An improvement on the total number of Hearts recognized when the cards are stacked.

![h:500px](media/yolov8_tuned_example4.jpg)

---

# Our YOLOv8_tuned in practice

Good recognition between red and black cards.

![h:400px](media/yolov8_tuned_example1.jpg)

---

# Our YOLOv8_tuned in practice

Example of **similar** recognition compared to the base synthetic model: 

![alt text](media/yolov8_tuned_example3.jpg)

---

# Our YOLOv8_tuned in practice

Example of **worse** recognition than the base synthetic model:

![h:500px](media/yolov8_tuned_example5.jpg)

---
# Live Demo
---

# Conclusion

### More data, better results!

---

# Conclusion

- **Fine-tuning a synthetic model** seems like the **most promising** option if a **good amount of data** is available for fine-tuning.
- Combining two datasets **should be tested** with a more even distribution between the datasets, or a **bigger amount of data** in general.

---

# Positive examples

**YOLOv8_comb** manages to find the Heart:

![h:500px](media/positive_comb.jpg)

---

# Positive examples

**YOLOv8_tuned** manages to find the Heart and the printed Ace of Hearts:

![h:500px](media/positive_tuned.jpg)

---

# Thank you for the attention!