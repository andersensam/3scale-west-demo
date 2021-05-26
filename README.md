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
- The installation process will take a few minutes to gather requirements and spin up the operator pod
- When installation is complete, click the operator, leading to a page with "Provided APIs".
- On the second row, in the middle, there is an option for "API Manager", click "Create instance"
- Provide a name and labels, if desired. The only required field is "Wildcard Domain".
    - The "Wildcard Domain" is the "apps domain" of your OpenShift cluster. If my console is located at [https://console.apps.lab.redhat.com](https://console.apps.lab.redhat.com), then my "Wildcard Domain" would be `apps.lab.redhat.com`

- Scroll to the bottom of the page and click "Create"
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

## Setting up 3scale API Manager
With the API Manager and demo APIs setup, it's time to jump into the 3scale Admin Console. We'll need to get the admin password from the OpenShift console
- Under the Workloads menu, select Secrets
    - Click the `system-seed` secret and scroll down
    - Clicking the icon on the lefthand side will copy the `ADMIN_PASSWORD` value to your clipboard
- Navigate to your 3scale Admin Console, which should be present at a URL similar to [https://3scale-admin.apps.lab.redhat.com](https://3scale-admin.apps.lab.redhat.com)
    - Login with username `admin` and the password copied from the previous step
- Follow the setup wizard, using the demo APIs we created in the previous section.
    - The "base URL" for the APIs should be something along the format of [https://3scale-demo-api-1.apps.lab.redhat.com/api](https://3scale-demo-api-1.apps.lab.redhat.com/api)
    - There are 2 methods defined within each demo instance:
        - `GET api/hello` responds with some variation of "hello", difference across the three instances
        - `GET api/check_header` as the name suggest, checks for the presence of a header: `X-Red-Hat-Auth`. If this header is not provided, the API will respond with a `403 Unauthorized` error. Any value is considered valid here. API instance 1 will provide a different message than instances 2 and 3.

## Adding additional backends
During the setup process, we added one of the API backends. This section will create additional backends and map to our sample product.
- In the main dashboard, under the lower section, click "Backends" and then click "New Backend"
- Choose a name and add whatever description you'd like
- The "Private Base URL" follows the format from the previous section. If adding the second demo API, use: [https://3scale-demo-api-2.apps.lab.redhat.com/api](https://3scale-demo-api-2.apps.lab.redhat.com/api)
- Repeat this process for whatever other API backends applicable

## Updating methods for Demo API Product
With our backends added, it's time to add methods for analytics
- Connect the new backends to the product
    - Using the top bar, switch to the API Product created during the initial setup wizard
    - On the lefthand sidebar, under the Integration menu, click Backends
    - Add the backend, defining the path to be used. In this case, the path selected will appear after the base URL generated by 3scale. Each backend requires a unique path.

- Create new methods for our backends
    - Choose a name and add a description

    - Add a new mapping rule
        - The demo APIs only support the "GET" verb
        - Use the "public path" followed by a slash and the method desired. Remember that there are two options: `/hello` and `/check_header`
            - If, for example, API instance 2 has public path `/api2`, using the `/hello` method would require pattern `/api2/hello`

        - Under "Method or Metric to increment", select the method we created in the previous step

These steps can be repeated for any other backends and/or methods you'd like to add.

## Promoting changes
As you may have noticed, the Configuration menu entry now has a warning sign next to it.
- Click into the Configuration menu
- Promote your changes to Staging and on to Production if desired.
- Validate your API methods by using the `curl` command provided.
    - Ensure that the `?user_key=` and its value are at the end of the request

        ```
        curl -k "https://api-3scale-apicast-staging.apps.lab.redhat.com:443/api2/hello?user_key=f1adf583c05b164654499fd1cd9a98b"
        ```

## Cleaning up
After having explored 3scale API Management sufficiently it's time to tear down and clean up. Luckily, clean up is easy, but does have a few 'gotchas'
- Go to the "Installed Operators" section in the lefthand menu and remove the 3scale operator
- From your terminal, use `oc` to delete all objects in the project/namespace created for the demo
    - If using the namespace `3scale-west-demo`, use the following command
        ```
        oc delete namespace 3scale-west-demo
        ```
- After object deletion has completed, we need to free up our Persistent Volumes (PVs)
    - If you do not anticipate re-deploying 3scale in the future, simply delete the PVs and remove the files from your NAS/storage
    - If you will deploy 3scale again do the following:
        - In the PersistentVolumes menu, under Storage, edit the YAML of the PVs to remove the section titled `claimRef`
        
        At first, the YAML will look something like this (**note** some fields are omitted for brevity):
        ```
        kind: PersistentVolume
        apiVersion: v1
        metadata:
          name: 3scale-1
          selfLink: /api/v1/persistentvolumes/3scale-1
          uid: d35b7b46-8c9c-4b14-ac0d-8f1d56d046cd
          resourceVersion: '3761170'
          creationTimestamp: '2021-04-20T17:18:24Z'
          annotations:
            pv.kubernetes.io/bound-by-controller: 'yes'
          finalizers:
            - kubernetes.io/pv-protection
        spec:
          capacity:
            storage: 100Gi
          nfs:
            server: 192.168.1.210
            path: /var/nfsshare/claims/1
          accessModes:
            - ReadWriteMany
          ***claimRef:
            kind: PersistentVolumeClaim
            namespace: 3scale-northwest-demo
            name: system-storage
            uid: 11558186-3bd2-430c-804a-14fd866168e4
            apiVersion: v1
            resourceVersion: '3761166'***
          persistentVolumeReclaimPolicy: Retain
          volumeMode: Filesystem
        status:
          phase: Bound
        ```

        Remove the `claimRef` section, `status`, and `phase` to result in something like this:
        ```
        kind: PersistentVolume
        apiVersion: v1
        metadata:
          name: 3scale-1
          selfLink: /api/v1/persistentvolumes/3scale-1
          uid: d35b7b46-8c9c-4b14-ac0d-8f1d56d046cd
          resourceVersion: '3761170'
          creationTimestamp: '2021-04-20T17:18:24Z'
          annotations:
            pv.kubernetes.io/bound-by-controller: 'yes'
          finalizers:
            - kubernetes.io/pv-protection
        spec:
          capacity:
            storage: 100Gi
          nfs:
            server: 192.168.1.210
            path: /var/nfsshare/claims/1
          accessModes:
            - ReadWriteMany
          persistentVolumeReclaimPolicy: Retain
          volumeMode: Filesystem
        ```
    - Repeat this process for the remaining PVs

## Feedback
Please provide any feedback on this project by pinging me on Google Chat or filing and issue here on Github. Thanks!