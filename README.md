# ic-sample-ui

Image Classifcation UI Example using Flask  

## Prerequisites
redhatアカウントを作成して、sandboxが30日フリーで使える
https://developers.redhat.com/developer-sandbox


## 事前準備としてBuildConfigとDeploymentsを予め用意
以前は唐さんから説明してくれたので、ここで省略。。。。。。。

## Pipeline作成
BuildConfigの起動task作成
```bash
内容参照 pipeline/start-oc-build.yaml
```

Deploymentsの起動task作成
```bash
内容参照 pipeline/restart-deployment.yaml
```

pipeline作成
```bash
内容参照 pipeline/pipeline.yaml
```

pipelineRun作成
```bash
内容参照 pipeline/run-build-with-bc.yaml
下記パラメータの値を自分環境と合わせて差し替えが必要
  params:
    - name: buildconfig-name
      value: ic-sample-ui-build
    - name: namespace
      value: duss023-dev
    - name: deployment-name
      value: ic-sample-ui

```

## Trigger作成
TriggerBinding作成
```bash
内容参照 Trigger/TriggerBinding.yaml
```

TriggerTemplate作成
```bash
内容参照 Trigger/TriggerTemplate.yaml
下記パラメータの値を自分環境と合わせて差し替えが必要
  params:
    - name: buildconfig-name
      value: ic-sample-ui-build
    - name: namespace
      value: duss023-dev
    - name: deployment-name
      value: ic-sample-ui
```

EventListener作成
```bash
内容参照 Trigger/EventListener.yaml
```

EventListenerURL公開
```bash
oc expose svc el-github-listener
oc get route el-github-listener
```

githubにwebhook追加
```bash
１．githubのプロジェクトに下記画面を開く
Settings → Webhooks → Add webhook

２．下記のように入力
Payload URL：http://EventListener公開したURL
Content type：application/json
Secret：空
Events：Just the push event
SSL verification：Enable SSL verification
```

テスト
githubのプロジェクトを修正してcommit、podが作り直しを見えること
