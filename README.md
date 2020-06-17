# PersonCountingRaspberry on the Edge using AWS Greengrass

+ Here is the link for the video where I do explain step by step how I did it 
https://www.youtube.com/watch?v=bRWT_sbzGds

> Hardware : 

![image](https://user-images.githubusercontent.com/40724965/82109740-c195bc80-9738-11ea-94a3-19a9266b8b3c.png)

+ we are using a raspberry pi 3 with greengrass core software pre-installed & a pi camera module

> After Creating a greengrass group and lunching the core with adequate certificates, you can add your lambda to the greengrass group 
<img width="1440" alt="Screenshot 2020-06-16 at 21 41 45" src="https://user-images.githubusercontent.com/40724965/84889679-88cf6700-b099-11ea-98e8-6f6e35d1cea8.png">

> Add the Camera ressource that give the Lambda function to access to your local camera 
<img width="1440" alt="Screenshot 2020-06-16 at 21 41 53" src="https://user-images.githubusercontent.com/40724965/84889788-c2a06d80-b099-11ea-8bf5-0f033709646a.png">

> Add the machine learning ressource
<img width="1440" alt="Screenshot 2020-06-16 at 21 41 56" src="https://user-images.githubusercontent.com/40724965/84889820-d1872000-b099-11ea-8149-fbdc3e3f007a.png">

> Finally, add subscription which let your lambda function send data to AWS Cloud
<img width="1440" alt="Screenshot 2020-06-16 at 21 46 45" src="https://user-images.githubusercontent.com/40724965/84889955-01362800-b09a-11ea-8817-7df18ff46ebd.png">



>MQTT Client to display the data sent to the cloud in the topic your defined earlier in your lambda function

<img width="1440" alt="Screenshot 2020-05-16 at 03 31 17" src="https://user-images.githubusercontent.com/40724965/82109796-3d900480-9739-11ea-9cc6-b5977d34e955.png">

