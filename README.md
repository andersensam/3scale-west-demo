# 3scale-west-demo

3Scale API Management on OpenShift

## How to use this document
- This document is intended for use by Solutions Architects and specialists to get 3Scale API Management setup on an existing OpenShift 4.X cluster. All recorded steps were performed on a cluster running version 4.6.X -- your mileage may vary on different versions. 
- The setup process expects some basic knowledge of OpenShift, specifically on how to use the “oc” tool and how to set up Persistent Volumes.
- This guide will not explain how to get OpenShift setup for the first time. 

## Registering for Quay.io
- In order to pull the demo images (containing the ‘fake’ APIs), users must have created an account on Quay.io and provided the username to Samuel Andersen [samander@redhat.com](mailto:samander@redhat.com)
- [ ] To register, vist [https://quay.io](https://quay.io) and login with your existing Red Hat credentials
- [ ] A username must be selected

## Client device prerequisites
- Clients must have the `oc` tool installed and available in their `$PATH`
- [ ] Visit your OpenShift console and in the upper righthand corner, select the question mark
- [ ] Click "Command line tools"
- [ ] Download the proper package for your OS/distribution and place in your `$PATH`