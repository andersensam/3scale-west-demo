# 3scale-west-demo

3Scale API Management on OpenShift

## How to use this document
- This document is intended for use by Solutions Architects and specialists to get 3Scale API Management setup on an existing OpenShift 4.X cluster. All recorded steps were performed on a cluster running version 4.6.X -- your mileage may vary on different versions. 
- The setup process expects some basic knowledge of OpenShift, specifically on how to use the “oc” tool and how to set up Persistent Volumes.
- This guide will not explain how to get OpenShift setup for the first time. 

## Registering for Quay.io
- In order to pull the demo images (containing the ‘fake’ APIs), users must have created an account on Quay.io and provided the username to Samuel Andersen [samander@redhat.com](mailto:samander@redhat.com)
- To register, vist [https://quay.io](https://quay.io) and login with your existing Red Hat credentials
- A username must be selected

## Client device prerequisites
- Clients must have the `oc` tool installed and available in their `$PATH`
- Visit your OpenShift console and in the upper righthand corner, select the question mark
- Click "Command line tools"
- Download the proper package for your OS/distribution and place in your `$PATH`
- Login to the OpenShift cluster, copying the login token from "Copy login command", found in the upper righthand corner in the OpenShift Console

## OpenShift cluster prerequisites
- Deploying 3Scale API Management requires a few Persistent Volumes (PV) to be available
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
    - In total, there should be **4 Persistent Volumes** ready for use by the 3Scale operator
- While the following isn't *required*, it is highly **recommended**: create a new project/namespace for the demo
    - New projects can be created from the OpenShift Console or via the `oc` tool
        - If using the OpenShift Console, click "Projects" on the lefthand sidebar under the "Home" section. Click "Create Project" in the upper righthand corner
        - If using the `oc` tool, ensure you're logged into the proper OpenShift cluster, then type `oc create namespace 3scale-west-demo` for example
    - While everything deployed via the 3Scale operator is tagged, I find it easier to delete an entire namespace than try to delete resources individually

## Deploying the 3Scale API Management Operator
- Change projects to `3scale-west-demo`, or whatever project/namespace you dedicated to this deployment
- Using the lefthand menu, select OperatorHub. The 3Scale API Management operator should be the first choice. Click install in the upper lefthand corner to launch the install process
- The installation process will take a few minutes to gather requirements and spin up the pods
- You can monitor installation progress by looking at the `Routes` created by the operator. You'll know installation is complete when you see roughly **6 routes** present, including one with the format https://**3scale-admin**.apps.{OCP Subdomain}