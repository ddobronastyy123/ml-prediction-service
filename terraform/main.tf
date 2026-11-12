terraform {
  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "~> 0.60"
    }
  }
}

provider "proxmox" {
  endpoint  = var.pm_api_url
  api_token = "${var.pm_api_token_id}=${var.pm_api_token_secret}"
  insecure  = true
}

variable "pm_api_url" {
  type = string
}

variable "pm_api_token_id" {
  type = string
}

variable "pm_api_token_secret" {
  type      = string
  sensitive = true
}

variable "ssh_public_key" {
  type = string
}


resource "proxmox_virtual_environment_vm" "db_server" {
  name      = "vm1-db"
  node_name = "beelinerouter"
  tags      = ["db", "ml-project"]

  clone {
    vm_id = 9000   # ID шаблона Ubuntu Server
  }

  cpu {
    cores = 2
  }

  memory {
    dedicated = 2048
  }

  network_device {
    bridge = "vmbr0"
  }

  initialization {
    ip_config {
      ipv4 {
        address = "10.0.2.4/24"
        gateway = "10.0.2.1"
      }
    }
    user_account {
      username = "student"
      keys     = [var.ssh_public_key]
    }
  }
}


resource "proxmox_virtual_environment_vm" "app_server" {
  name      = "vm2-app"
  node_name = "beelinerouter"
  tags      = ["app", "ml-project"]

  clone {
    vm_id = 9000
  }

  cpu {
    cores = 2
  }

  memory {
    dedicated = 4096
  }

  network_device {
    bridge = "vmbr0"
  }

  initialization {
    ip_config {
      ipv4 {
        address = "10.0.2.5/24"
        gateway = "10.0.2.1"
      }
    }
    user_account {
      username = "student"
      keys     = [var.ssh_public_key]
    }
  }
}

output "db_ip" {
  value = "10.0.2.4"
}

output "app_ip" {
  value = "10.0.2.5"
}
