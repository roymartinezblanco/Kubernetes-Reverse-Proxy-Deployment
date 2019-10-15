http http://127.0.0.1 -b

docker build -t python-app-server -f App-Dockerfile .

docker run -p 80:8000 python-app-server

https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/


https://matthewpalmer.net/kubernetes-app-developer/articles/guide-install-kubernetes-mac.html


https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3

https://runnable.com/docker/python/dockerize-your-python-application

docker tag 04be66021f87 rmartinezb/python-app-server:firsttry

kubectl delete services python-app-service
kubectl delete deployment python-app-server


 docker tag 04be66021f87 rmartinezb/python-app-server:firsttry

 docker push rmartinezb/python-app-server



kubectl delete deploy tiller-deploy -n kube-system

kubectl delete service tiller-deploy -n kubesystem
kubectl create serviceaccount tiller --namespace kube-system
kubectl create clusterrolebinding tiller-cluster-rule  --clusterrole=cluster-admin  --serviceaccount=kube-system:tiller

helm init --service-account tiller --override spec.selector.matchLabels.'name'='tiller',spec.selector.matchLabels.'app'='helm' --output yaml | sed 's@apiVersion: extensions/v1beta1@apiVersion: apps/v1@' | kubectl apply -f -


 kubectl create serviceaccount tiller --namespace kube-system
 kubectl create clusterrolebinding tiller-cluster-rule  --clusterrole=cluster-admin  --serviceaccount=kube-system:tiller