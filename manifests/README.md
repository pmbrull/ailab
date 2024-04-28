# AI Lab Ubuntu setup

- [docker](https://docs.docker.com/engine/install/ubuntu/)
  - `sudo usermod -aG docker pere && newgrp docker`
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- [microk8s](https://microk8s.io/)
  - `alias k='microk8s kubectl'`
  - `sudo microk8s.kubectl config view --raw > $HOME/.kube/config`
  - `microk8s kubectl create token default` to enter the dashboard
- [ArgoCD](https://argo-cd.readthedocs.io/en/stable/getting_started/)
  - [CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/)
  - `admin`:  get pwd from from `argocd admin initial-password -n argocd` or ` k -n argocd get secrets/argocd-initial-admin-secret --template={{.data.password}} | base64 -d`
  - Connect repo from the UI ([guide](https://www.webagesolutions.com/blog/deploy-an-application-using-argocd))
  - Install [AppSource](https://blog.argoproj.io/introducing-the-appsource-controller-for-argocd-52f21d28d643)
  - Install [guestbook example](https://argo-cd.readthedocs.io/en/stable/getting_started/) from GitHub `manifests/apps/guestbook`
  - If an app gets stuck in `Deleting`, try removing the finalizers: `k -n argocd patch app <app-name> --type='json' -p='[{"op": "remove", "path": "/metadata/finalizers"}]'`
- [Nexus]
  - Deployed in ArgoCD
  - Get the initial `admin` password with: `k -n nexus exec -it nexus-6dc695df94-495jc -- bash` then `cat /nexus-data/admin.password`.
    - Updated `admin` pwd to ailab pc pwd
  - Setup docker repository [guide](https://medium.com/codemonday/setup-nexus-oss-on-docker-as-docker-registry-for-learning-748c23f0b951)
    - named `docker-private`
    - accepts HTTP at `8082`
- [BentoML Transformer Release](knowledge_graph/README.md)
- [Neo4J]
- [Knowledge Graph]
  - [Neo4J Custom Embeddings](knowledge_graph/README.md)
  - Install [sdkman](https://sdkman.io/install)
    - `sdk install java 17.0.11-amzn`
    - `sdk install maven`

# Laptop setup

## /etc/hosts

```
192.168.1.203   lima
```

## ~/.ssh/config

```
Host lima
  Hostname 192.168.1.203
  User pere
  LocalForward 9888 localhost:8080   # argocd
  LocalForward 9889 localhost:10443  # dashboard-proxy
  LocalForward 9890 localhost:8081   # nexus
  LocalForward 9891 localhost:3000   # transformer
  LocalForward 9892 localhost:7474   # neo4j http
  LocalForward 9893 localhost:7687   # neo4j bolt
```

Then `ssh lima`

# AI Lab setup

## Expose all services in systemd

1. Create script `/usr/local/bin/expose.sh`
   ```bash
   #!/bin/bash
   mkdir -p /tmp/expose.service & \
   microk8s kubectl port-forward svc/argocd-server -n argocd 8080:443 & \
   microk8s kubectl port-forward svc/nexus -n nexus 8081:8081 & \
   microk8s kubectl port-forward svc/nexus -n nexus 8082:8082 & \
   microk8s kubectl port-forward svc/transformer -n knowledge-graph 3000:3000 & \
   microk8s kubectl port-forward svc/neo-embedding -n knowledge-graph 7474:7474 & \
   microk8s kubectl port-forward svc/neo-embedding -n knowledge-graph 7687:7687 & \
   microk8s dashboard-proxy &
   ```
2. `chmod +x expose.sh`
3. Create `/etc/systemd/system/expose.service`
   ```ini
   [Unit]
   Description=Expose services
   After=network.target

   [Service]
   ExecStart=/usr/local/bin/expose.sh
   Restart=always
   User=pere
   Type=Simple

   [Install]
   WantedBy=multi-user.target
   ```
4. Reload `systemd`:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable expose.service
    sudo systemctl start expose.service
    ```

TODO: Figure this out

## `~/.bash_aliases`

```bash
alias k="microk8s kubectl"
alias gfu="git fetch upstream"
alias gf="git fetch"
alias gc="git checkout"
alias gcb='function gcb(){git fetch $2 && gc -b "$1" --no-track $2/main};gcb'
alias gcr='function gcr(){git fetch $1 && gc -B random --no-track $1/main};gcr'
alias gp="git add . && git commit -m 'nit' && git push"
```