# 3scale-west-demo

3scale API Management on OpenShift

## How to use this document
- This document is intended for use by Solutions Architects and specialists to get 3scale API Management setup on an existing OpenShift 4.X cluster. All recorded steps were performed on a cluster running version 4.7.X -- your mileage may vary on different versions. 
- The setup process expects some basic knowledge of OpenShift, specifically on how to use the “oc” tool and how to set up Persistent Volumes.
- This guide will not explain how to get OpenShift setup for the first time. 

## Client device prerequisites
- Clients must have the `oc` tool installed and available in their `$PATH`
- Visit your OpenShift console and in the upper righthand corner, select the question mark
- Click "Command line tools"
- Download the proper package for your OS/distribution and place in your `$PATH`
- Login to the OpenShift cluster, copying the login token from "Copy login command", found in the upper righthand corner in the OpenShift Console

## OpenShift cluster prerequisites
- Deploying 3scale API Management requires a few Persistent Volumes (PV) to be available
    - The Persistent Volume Claim (PVC) `system-storage` requires a volume with the `ReadWriteMany` access mode. An example can be found below   
        ```
        kind: PersistentVolume
        apiVersion: v1
        metadata:
        name: 3scale-1
        spec:
        capacity:
            storage: 100Gi
        nfs:
            server: 192.168.1.210
            path: /var/nfsshare/claims/1
        accessModes:
            - ReadWriteMany
        ```
        - Through the storage capacity is relatively arbitrary, I've found that provisioning a PV with less than 15Gi typically won't work
    - The PVCs `backend-redis-storage`, `system-redis-storage`, and `mysql-storage` require PVs with the `ReadWriteOnce` access mode.
        ```
        kind: PersistentVolume
        apiVersion: v1
        metadata:
        name: 3scale-2
        spec:
        capacity:
            storage: 100Gi
        nfs:
            server: 192.168.1.210
            path: /var/nfsshare/claims/2
        accessModes:
            - ReadWriteOnce
        ```
    - In total, there should be **4 Persistent Volumes** ready for use by the 3scale operator
- While the following isn't *required*, it is highly **recommended**: create a new project/namespace for the demo
    - New projects can be created from the OpenShift Console or via the `oc` tool
        - If using the OpenShift Console, click "Projects" on the lefthand sidebar under the "Home" section. Click "Create Project" in the upper righthand corner
        - If using the `oc` tool, ensure you're logged into the proper OpenShift cluster, then type `oc create namespace 3scale-west-demo` for example
    - While everything deployed via the 3scale operator is tagged, I find it easier to delete an entire namespace than try to delete resources individually

## Deploying the 3scale API Management Operator
- Change projects to `3scale-west-demo`, or whatever project/namespace you dedicated to this deployment
- Using the lefthand menu, select OperatorHub. The 3scale API Management operator should be the first choice. Click install in the upper lefthand corner to launch the install process
- The installation process will take a few minutes to gather requirements and spin up the pods
- You can monitor installation progress by looking at the `Routes` created by the operator. You'll know installation is complete when you see roughly **6 routes** present, including one with the format https://**3scale-admin**.apps.{OCP Subdomain}

## Deploying sample APIs for use within 3scale
- Use `oc` to deploy `3scale-demo-template` within your preferred namespace
    - If using namespace `3scale-west-demo`, use the following commands:
        ```
        oc project 3scale-west-demo
        oc create -f 3scale-demo-template.yml
        ```
- Using the `3scale-demo-template`, deploy the APIs and their associated routes
    - The template requires a few variables to be defined, namely `APPLICATION_NAME` and `OCP_URL`. `APPLICATION_NAME` will be used to tag resources deployed by the template. There is a default value, set to `3scale-api-demo`. You **do not** need to change this value, but can by passing an override in the next command. 

    - `OCP_URL` on the other hand **does require** a value to be set on the command line.
        - The `OCP_URL` is the "apps domain" of your OpenShift cluster. If my console is located at [https://console.apps.lab.redhat.com](https://console.apps.lab.redhat.com), then my `OCP_URL` would be `apps.lab.redhat.com`
    ```
    oc new-app 3scale-demo-template -p OCP_URL=apps.lab.redhat.com
    ```
    If wanting to set the `APPLICATION_NAME`, use
    ```
    oc new-app 3scale-demo-template -p OCP_URL=apps.lab.redhat.com -p APPLICATION_NAME=my-3scale-application
    ```
- If successful, `oc` will output that it has created a number of resources and will provide the routes exposed for the fake APIs, following the format [https://3scale-demo-api-1.apps.lab.redhat.com](https://3scale-demo-api-1-apps.lab.redhat.com)

- Test successful deployment by using curl. Note the use of `-k` to prevent curl from complaining about self-signed certificates
    ```
    curl -k https://3scale-demo-api-1.apps.lab.redhat.com/api/hello
    ```