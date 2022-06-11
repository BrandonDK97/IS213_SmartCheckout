# Smart Checkout System
## IS213 Enterprise Solution Development Project - G9T7

# Table of Contents
1. [Project Overview](#project-overview)
2. [Technical Overview Diagram](#technical-overview-diagram)
3. [How to Set Up Smart Checkout System with Docker](#how-to-set-up-smart-checkout-system-with-docker)
4. [How to Set Up Smart Checkout System with Kubernetes](#how-to-set-up-smart-checkout-system-with-kubernetes)
5. [User Scenarios](#user-scenarios)
6. [Frameworks and Databases Utilised](#frameworks-and-databases-utilised)
7. [Contributors](#contributors)


# Project Overview
<img src="ReadmeFiles\logo.jpg">
There is a need to expedite Checkout processes in brick and mortar stores to keep up with digitalisation and online stores. The Brick and Mortar checkout process is a long and tedious process that requires a lot of manual intervention. 

The goal of this project is to expedite the checkout process with the **Smart Checkout System**. The Smart Checkout System enables users to scan items physically in-store using the QR code and checkout from the application without having to queue.

# Link to Docker Hub for the images 
https://hub.docker.com/repository/docker/carleb12345/esd

# Technical Overview Diagram
<img src="ReadmeFiles\overview.png">

# How to Set Up Smart Checkout System with Docker
1. Clone our GitHub Repository or download the ZIP file

    ```gh repo clone RodentOfUnusualSizee/IS4smth-ESD```

2. Open Command Prompt/Terminal and `cd` to the root folder:

3. Run ``` docker-compose up --build ``` to build and start up Smart Checkout System

4. Start the Smart Checkout System from `login.html` in `smartCheckOutSystemUI` folder using VSCode Live Server or WAMPServer.

5. Create a new account or log in.

6. View Management UI from `manage_index.html` in `managementUI` folder

# How to Set Up Smart Checkout System with Kubernetes
1. Clone our GitHub Repository or download the ZIP file

    ```gh repo clone RodentOfUnusualSizee/IS4smth-ESD```

2. Setup up your kubernetes node. (You can use minikube https://minikube.sigs.k8s.io/docs/start/)

3. Open Command Prompt/Terminal and `cd` to the root folder then `kubeDeployement`:

4. Run ``` kubectl apply -f ./ ``` to build and start up Smart Checkout System on the kubernetes cluster. The mainfest file is an instructure for the minukube node to pull the images from docker hub and set up the deployment and service clusters

5. Wait for your services to fininish running before the next step. Use your monitoring tool to check if the clusters are up (e.g minikube dashboard)

6. Start the Smart Checkout System from `login.html` in `smartCheckOutSystemUI` folder using VSCode Live Server or WAMPServer.

7. Create a new account or log in.

8. View Management UI from `manage_index.html` in `managementUI` folder


# ⚠️ READ THIS CAREFULLY! ⚠️

There are 2 shops in the Smart Checkout System. The first shop is in SMU and the second shop is in Tampines. If you are **NOT** within 5KM of the above areas, you will **NOT** be able to proceed with using the service.

To workaround this:
1. go to `location.py` in `locationMS` folder
2. Refer to **Line 42**
3. Change the `distance` variable in `if distance<5` to any higher number (5 is 5km which is the maximum distance you can be away from the store)
4. Save the file and rebuild the `location` image or simply `docker compose up --build` 

# User Scenarios
## Scenario 1 - User creates account on app
<img src="ReadmeFiles\scenario1.PNG">

## Scenario 2 - Add Item into Cart with QR Code
<img src="ReadmeFiles\scenario2.PNG">

## Scenario 3 - User checks out using the app
<img src="ReadmeFiles\scenario3.png">

## Scenario 4 - Shop Management views and manages shop from Management UI
<img src="ReadmeFiles\scenario4.png">

# Frameworks and Databases Utilised
**Services and UI**
- Python Flask
- HTML
- CSS 
- Javascript
- ASP .NET CORE WEB API (C#)

**Database**
- Google Cloud Firebase
- Microsoft SQL
- MongoDB

**Others**
- Kubernetes
- Stripe Payment API
- RabbitMQ Messaging
- Location API
- QR Code Scanner

# Stripe and Firebase accounts to verify working scenario
**Stripe**
https://dashboard.stripe.com/test/dashboard
- Stripe account: esdg9t7@gmail.com
- Stripe account password: EsdG9T7aplus!

**Firebase**
https://console.firebase.google.com/u/0/project/is213-userdata/database/is213-userdata-default-rtdb/data
- Gmail account: esdt9g7@gmail.com
- Gmail account password: esdg9t7aplus

# Contributors

**G9 Team 7**

<table style="border:0.5px solid;">
    <tr>
        <td align="center"><img src="" width="150px;" alt=""/><br /><sub><b>Brandon</b></sub></a></td>
        <td align="center"><img src="" width="150px;" alt=""/><br /><sub><b>Caleb</b></sub></a></td>
        <td align="center"><img src="" width="150px;" alt=""/><br /><sub><b>Rou</b></sub></a></td>
        <td align="center"><img src="" width="150px;" alt=""/><br /><sub><b>Gerald</b></sub></a></td>
        <td align="center"><img src="" width="150px;" alt=""/><br /><sub><b>Yan Wee</b></sub></a></td>
    </tr>
</table>
