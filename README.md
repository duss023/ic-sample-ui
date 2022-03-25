# ic-sample-ui

Image Classifcation UI Example using Flask  

## Architecture

![Architecture](https://github.com/mmitsugi/ic-sample-api/blob/main/doc/images/architecture_ui_and_api.png)

## Prerequisites

* OpenShift 4
* OpenShift Pipeline Operator installed
* ic-sample-api installed

## Deployment steps

Set project to the project used in ic-sample-api
```bash
$ oc project ic-pipelines
```
Create pipeline
```bash
$ oc create -f pipeline/pipeline.yaml
```
Check task, clustertask, pipeline list
```bash
$ tkn task list
$ tkn clustertask list
$ tkn pipeline list
```
Run pipeline
```bash
$ tkn pipeline start build-and-deploy -w name=shared-workspace,claimName=model-pv-claim -p deployment-name=ic-sample-ui -p git-url=https://github.com/mmitsugi/ic-sample-ui.git -p git-revision=ppc64le -p IMAGE=image-registry.openshift-image-registry.svc:5000/ic-pipelines/ic-sample-ui --use-param-defaults
```

## References

* [OpenShift Pipelines Tutorial](https://github.com/openshift/pipelines-tutorial)
