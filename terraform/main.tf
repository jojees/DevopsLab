# main.tf
terraform {
  required_providers {
    helm = { source = "hashicorp/helm", version = "~> 2.12" }
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.25" }
  }
}

provider "kubernetes" {
  host = "https://kubernetes.default.svc" # TFC Agent uses internal K8s DNS
}

provider "helm" {
  kubernetes {
    host = "https://kubernetes.default.svc"
  }
}

# 1. Install ArgoCD
resource "helm_release" "argocd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = "argocd"
  create_namespace = true

  set {
    name  = "server.service.type"
    value = "ClusterIP"
  }
}

# 2. Bootstrap the "Root" App
# This tells ArgoCD: "Go look at my GitHub repo to manage everything else"
resource "kubernetes_manifest" "root_app" {
  depends_on = [helm_release.argocd]
  manifest = {
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"
    metadata = {
      name      = "root-app"
      namespace = "argocd"
    }
    spec = {
      project = "default"
      source = {
        repoURL        = "https://github.com/jojees/DevopsLab.git"
        targetRevision = "main"
        path           = "argocd/bootstrap"
      }
      destination = {
        server    = "https://kubernetes.default.svc"
        namespace = "argocd"
      }
      syncPolicy = {
        automated = { prune = true, selfHeal = true }
      }
    }
  }
}