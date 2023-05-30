# Eye_blinking_detection
<br/>

## 1. Results and test

### 1.1 Determine the maximum and minimum value of EAR
<div align=center>
<img width="246" alt="image" src="https://github.com/JasonJimmyJJ/Eye_blinking_detection/assets/134904329/89db2b78-2c46-4d36-a9f9-f907360980a7">
</div>

### 1.2 Start counting and display the count of complete and incomplete eye closing times in real time

<img width="245" alt="image" src="https://github.com/JasonJimmyJJ/Eye_blinking_detection/assets/134904329/2df5b32c-5720-4a09-9c01-442ac60d76ed">

### 1.3 Fully closed eyes and semi-closed eyes were tested

<img width="254" alt="image" src="https://github.com/JasonJimmyJJ/Eye_blinking_detection/assets/134904329/6e9f8f49-a3eb-4fe3-92fd-5a14a5b95b8c">

## 2. Realization steps

### 2.1 The dlib library is used for facial feature point recognition

The Dlib library can detect 68 feature points in face recognition, as shown in Figure 2 below, and obtain the indexes of the left and right eye facial marks respectively. The video stream is gray-scale processed by OpenCV to detect the location information of the human eye.
<img width="163" alt="image" src="https://github.com/JasonJimmyJJ/Eye_blinking_detection/assets/134904329/d471223c-8754-4a2e-bf8d-56f725690db8">

### 2.2 The aspect ratio of the eye is calculated to determine whether the eye blinks or not

Calculate the Eye Aspect Ratio (EAR). When the human eye is open, the EAR fluctuates around a certain value, and when the human eye is closed, the EAR drops rapidly and theoretically approaches zero. At that time, face detection models were not so accurate. So we think that when the EAR is below a certain threshold, the eye is closed. To detect the number of blinks, we need to set the number of consecutive frames of the same blink. Blinking speed is relatively fast, generally 1~3 frames to complete the blinking action. Both thresholds should be set according to the actual situation.

<img width="329" alt="image" src="https://github.com/JasonJimmyJJ/Eye_blinking_detection/assets/134904329/145f3906-ee27-4730-830c-daf38625e577">

### 2.3 Full blink versus half blink

Because to count the state of full blink and half blink, we need to make a judgment based on the value of EAR.

#### 2.3.1 Determine the EAR maximum and minimum values

First, we will ask the subject to stare at a specific part of the screen for 5-6 seconds, as shown in Figure 4 below. The subject will blink in the normal state. We can count the maximum and minimum EAR values of the subject during this time as the maximum and minimum EAR values of the fully open and fully closed eyes

<img width="264" alt="image" src="https://github.com/JasonJimmyJJ/Eye_blinking_detection/assets/134904329/74d52bc6-f603-4e6a-8d77-24083875555f">

#### 2.3.2 Set the blink threshold

As can be observed from the EAR value data in Figure 5 below, we can judge the degree of blinking by the inflection point. We set the EAR inflection point (red circle in Figure 5) as 80% or more of the EAR maximum value (when the eyes are closed), we set it as complete eye closing, and when the EAR inflection point occurs at 80%-20% of the maximum value, it is set as incomplete eye blinking.

<img width="217" alt="image" src="https://github.com/JasonJimmyJJ/Eye_blinking_detection/assets/134904329/7dc767ac-019c-4e3d-938a-498d01d2eddd">

### 2.4 Other details to consider

Are both eyes blinking at the same rate? By analyzing the EAR values of the left and right eyes, we can get that the values of the two eyes are basically the same, as shown in FIG. 6 below. Therefore, our final EAR value takes the average value of the left and right eyes to reduce the error of the experiment.

<img width="337" alt="image" src="https://github.com/JasonJimmyJJ/Eye_blinking_detection/assets/134904329/aaf66e5e-e77b-46a1-9146-45580e70552e">




