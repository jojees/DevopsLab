# main.tf
terraform {
  required_providers {
    helm       = { source = "hashicorp/helm", version = "~> 2.12" }
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.25" }
    argocd     = { source = "argoproj-labs/argocd", version = "~> 7.0", core = true }
  }
}

provider "kubernetes" {
  host                   = "https://kubernetes.default.svc"
  cluster_ca_certificate = file("/var/run/secrets/kubernetes.io/serviceaccount/ca.crt")
  token                  = file("/var/run/secrets/kubernetes.io/serviceaccount/token")
}

provider "helm" {
  kubernetes {
    host                   = "https://kubernetes.default.svc"
    cluster_ca_certificate = file("/var/run/secrets/kubernetes.io/serviceaccount/ca.crt")
    token                  = file("/var/run/secrets/kubernetes.io/serviceaccount/token")
  }
}

# 1. Install ArgoCD
resource "helm_release" "argocd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = "9.4.7"
  namespace        = "argocd"
  create_namespace = true
  
  # Crucial for slow ARM nodes:
  timeout                    = 900   # Increase to 15 minutes
  wait                       = false # Don't block the TF run waiting for pods to be 'Ready'
  disable_openapi_validation = true  # Speeds up the initial API handshake
  cleanup_on_fail            = true  # Automatically rolls back if it fails again

  set {
    name  = "server.service.type"
    value = "ClusterIP"
  }

  # Optimization: Disable non-essential components to save RAM on Pi
  set {
    name  = "notifications.enabled"
    value = "false"
  }
  set {
    name  = "applicationSet.enabled"
    value = "false" # Only if you don't need app-of-apps/generators
  }

  set {
    name  = "dex.enabled"
    value = "false" # Disable if using local admin or OIDC directly
  }

  # Resource Optimization for Pi 5 (ARM64)
  # Global requests are a good start, but specific components need limits
  set {
    name  = "global.resources.requests.cpu"
    value = "50m"
  }
  set {
    name  = "global.resources.requests.memory"
    value = "128Mi"
  }
  set {
    name  = "server.resources.limits.memory"
    value = "512Mi" # The API server can spike during UI usage
  }
  set {
    name  = "repoServer.resources.limits.memory"
    value = "512Mi" # Rendering Helm charts is memory intensive
  }

  # 1. Set Memory Limits & Requests
  set {
    name  = "redis.resources.requests.memory"
    value = "64Mi"
  }
  set {
    name  = "redis.resources.limits.memory"
    value = "128Mi" # Plenty for a small Pi cluster
  }

  # Use RAM for Redis instead of slow SD card storage
  set {
    name  = "redis.persistence.enabled"
    value = "false"
  }
  # Use RAM for temporary Git repo clones
  set {
    name  = "repoServer.volumes"
    value = "[{name: 'cmp-tmp', emptyDir: {}}]"
  }

  # 2. Configure Redis Eviction Policy (CRITICAL)
  # 'allkeys-lru' ensures Redis drops old cache data when it hits the limit
  # instead of crashing or refusing new data.
  set {
    name  = "redis.extraArgs"
    value = "{--maxmemory,100mb,--maxmemory-policy,allkeys-lru}"
  }

  # 3. Disable HA for Redis (Recommended for single-node or small Pi clusters)
  # HA uses 3+ pods and significantly more RAM.
  set {
    name  = "redis-ha.enabled"
    value = "false"
  }

  set {
    name  = "controller.replicas"
    value = "1"
  }
  set {
    name  = "repoServer.replicas"
    value = "1"
  }
  set {
    name  = "server.replicas"
    value = "1"
  }

  set {
    name  = "configs.cm.timeout.reconciliation"
    value = "600s" # Increase to 5 minutes
  }
}

# data "kubernetes_secret" "argocd_admin_pwd" {
#   depends_on = [helm_release.argocd]
#   metadata {
#     name      = "argocd-initial-admin-secret"
#     namespace = "argocd"
#   }
# }

# 2. The Provider uses the Data Source
# provider "argocd" {
#   server_addr = "argocd-server.argocd.svc.cluster.local:80"
#   insecure    = true
#   username    = "admin"
#   password    = data.kubernetes_secret.argocd_admin_pwd.data["password"]
# }

# The Provider (No secret data source needed)
provider "argocd" {
  core = true
}

# 2. Bootstrap the "Root" App
# This tells ArgoCD: "Go look at my GitHub repo to manage everything else"
# resource "kubernetes_manifest" "root_app" {
#   depends_on = [helm_release.argocd]
#   manifest = {
#     apiVersion = "argoproj.io/v1alpha1"
#     kind       = "Application"
#     metadata = {
#       name      = "root-app"
#       namespace = "argocd"
#     }
#     spec = {
#       project = "default"
#       source = {
#         repoURL        = "https://github.com/jojees/DevopsLab.git"
#         targetRevision = "main"
#         path           = "argocd/bootstrap"
#       }
#       destination = {
#         server    = "https://kubernetes.default.svc"
#         namespace = "argocd"
#       }
#       syncPolicy = {
#         automated = { prune = true, selfHeal = true }
#       }
#     }
#   }
# }

resource "argocd_application" "root_app" {
  depends_on = [helm_release.argocd]
  metadata {
    name      = "root-app"
    namespace = "argocd"
  }
  spec {
    project = "default"
    source {
      repo_url        = "https://github.com/jojees/DevopsLab.git"
      target_revision = "main"
      path            = "argocd/bootstrap"
    }
    destination {
      server    = "https://kubernetes.default.svc"
      namespace = "argocd"
    }
    sync_policy {
      automated {
        prune     = true
        self_heal = true
      }
    }
  }
}